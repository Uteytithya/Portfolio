"""Subset and self-host the two site fonts.

Google's CJK webfonts are split into ~120 unicode-range slices. The English page
alone renders ~55 scattered Japanese characters, which drags in nearly every
slice: 1.35 MB across 118 requests. Because this site is fully static, the exact
glyph set is knowable, so we ship one small woff2 per weight instead.

Coverage is deliberately wider than "what dist happens to contain today":

  * Latin, Latin-1 and general punctuation in full, so English copy can be
    edited freely without regenerating anything.
  * Hiragana and katakana in full — only a few hundred glyphs, and it means any
    kana rewrite is safe too.
  * Every CJK ideograph found in the built HTML, plus the characters hard-coded
    in components, which is the only part that needs a re-run.

So: re-run `npm run fonts` after adding *new kanji*. Everything else is covered.

Usage:  npm run build   (builds dist first)
        npm run fonts   (reads dist/, writes public/fonts/)
"""

import io
import re
import sys
import unicodedata
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = ROOT / "public" / "fonts"
CACHE = ROOT / ".fontcache"

UPSTREAM = "https://raw.githubusercontent.com/google/fonts/main/ofl/"

# Only the weights the stylesheets actually ask for. Zen Kaku has no 600 (it
# steps 500 -> 700) and nothing on the site requests 700, so it ships two.
FACES = [
    ("Zen Old Mincho", 400, "zenoldmincho", "ZenOldMincho-Regular.ttf"),
    ("Zen Old Mincho", 500, "zenoldmincho", "ZenOldMincho-Medium.ttf"),
    ("Zen Old Mincho", 600, "zenoldmincho", "ZenOldMincho-SemiBold.ttf"),
    ("Zen Kaku Gothic New", 400, "zenkakugothicnew", "ZenKakuGothicNew-Regular.ttf"),
    ("Zen Kaku Gothic New", 500, "zenkakugothicnew", "ZenKakuGothicNew-Medium.ttf"),
]

LICENSES = [("zenoldmincho", "OFL.txt"), ("zenkakugothicnew", "OFL.txt")]


# Everything set in the display face. Kept in sync with the `font-family:
# 'Zen Old Mincho'` rules in src/ — if you add one there, add its class here or
# the glyphs it needs will be missing from the subset.
DISPLAY_CLASSES = {
    "font-display",
    "header-kanji",
    "footer-kanji",
    "kanji-ghost",
    "seal-glyph",
    "card-index",
    "hero-rail",
    "marquee-item",
    "nav-hamburger",
    "about-quote",
    "notfound-code",
    "notfound-title-ja",
}

# .prose-quiet h2/h3 are display too, but only by virtue of their ancestor.
PROSE_CLASS = "prose-quiet"
PROSE_TAGS = {"h2", "h3"}

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class TextExtractor(HTMLParser):
    """Splits visible text by which of the two faces will render it.

    A browser resolves this from computed styles; here it is reconstructed from
    the class stack, which is why DISPLAY_CLASSES has to track the stylesheets.
    The result is cross-checked against a real browser run — see the README note
    in this file's docstring.
    """

    SKIP = {"script", "style"}

    def __init__(self):
        super().__init__()
        self.display = set()
        self.body = set()
        self._stack = []          # (tag, classes) for open elements
        self._skip_depth = 0

    # -- helpers -------------------------------------------------------
    def _in_display(self, tag):
        for _, classes in self._stack:
            if classes & DISPLAY_CLASSES:
                return True
        if tag in PROSE_TAGS or any(t in PROSE_TAGS for t, _ in self._stack):
            if any(PROSE_CLASS in c for _, c in self._stack):
                return True
        return False

    def _add(self, text, display):
        target = self.display if display else self.body
        target.update(ch for ch in text if ch.strip())

    # -- parser hooks --------------------------------------------------
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set((attrs.get("class") or "").split())
        if tag in self.SKIP:
            self._skip_depth += 1
        # Text carried in attributes renders in the body face (alt text is not
        # painted, but title/aria-label can surface in tooltips).
        for key in ("alt", "aria-label", "title"):
            if attrs.get(key):
                self._add(attrs[key], display=False)
        if tag not in VOID:
            self._stack.append((tag, classes))
            # An element that is itself display-classed covers its own text.
            if classes & DISPLAY_CLASSES:
                pass

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        # self-closing: nothing pushed for void tags, so nothing to pop

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip_depth:
            self._skip_depth -= 1
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data):
        if self._skip_depth or not data.strip():
            return
        tag = self._stack[-1][0] if self._stack else ""
        self._add(data, display=self._in_display(tag))


def always_keep() -> set:
    """Ranges kept in full so ordinary copy edits never need a rebuild.

    Latin and kana are cheap — a few hundred simple outlines — so both faces
    carry them entirely. Kanji are the expensive part and are included only
    where actually used, which is why new kanji require a re-run.
    """
    keep = set()
    keep |= {chr(c) for c in range(0x20, 0x7F)}       # ASCII
    keep |= {chr(c) for c in range(0xA0, 0x100)}      # Latin-1 supplement
    keep |= {chr(c) for c in range(0x2000, 0x2070)}   # general punctuation
    keep |= {chr(c) for c in range(0x3000, 0x3040)}   # CJK punctuation
    keep |= {chr(c) for c in range(0x3040, 0x30A0)}   # hiragana
    keep |= {chr(c) for c in range(0x30A0, 0x3100)}   # katakana
    keep |= set("←↑→↓●○◦・—–…※〜")
    return keep


def glyphs_from_dist():
    """Returns (display_set, body_set) of characters actually rendered."""
    if not DIST.exists():
        sys.exit("dist/ not found — run `npm run build` first.")
    display, body = set(), set()
    pages = 0
    for path in DIST.rglob("*.html"):
        parser = TextExtractor()
        parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
        display |= parser.display
        body |= parser.body
        pages += 1
    print(f"  scanned {pages} built pages")
    return display, body


def fetch(rel: str) -> bytes:
    CACHE.mkdir(exist_ok=True)
    cached = CACHE / rel.replace("/", "_")
    if cached.exists():
        return cached.read_bytes()
    print(f"  downloading {rel}")
    with urllib.request.urlopen(UPSTREAM + rel) as response:
        data = response.read()
    cached.write_bytes(data)
    return data


def main():
    print("Collecting glyphs")
    display_used, body_used = glyphs_from_dist()
    base = always_keep()

    # The display face renders headings and a handful of decorative kanji; the
    # body face renders everything else. Giving each only what it needs is what
    # keeps the three Mincho weights from dominating the payload.
    display_set = {c for c in (display_used | base) if c.isprintable()}
    body_set = {c for c in (body_used | base) if c.isprintable()}

    def cjk_count(s):
        return sum(1 for c in s if unicodedata.category(c) == "Lo" and ord(c) > 0x3100)

    print(f"  display face: {len(display_set):4d} chars ({cjk_count(display_set)} kanji)")
    print(f"  body face:    {len(body_set):4d} chars ({cjk_count(body_set)} kanji)")

    OUT.mkdir(parents=True, exist_ok=True)
    per_family = {
        "Zen Old Mincho": "".join(sorted(display_set)),
        "Zen Kaku Gothic New": "".join(sorted(body_set)),
    }

    total_before = 0
    total_after = 0
    faces_css = []

    for family, weight, folder, filename in FACES:
        text = per_family[family]
        raw = fetch(f"{folder}/{filename}")
        total_before += len(raw)

        font = TTFont(io.BytesIO(raw))
        options = subset.Options()
        options.flavor = "woff2"
        options.desubroutinize = True
        options.layout_features = ["kern", "liga", "clig", "calt", "palt", "vert", "vrt2"]
        options.name_IDs = ["*"]          # keep the OFL-required name records
        options.notdef_outline = True
        options.drop_tables += ["DSIG"]

        subsetter = subset.Subsetter(options=options)
        subsetter.populate(text=text)
        subsetter.subset(font)

        slug = family.lower().replace(" ", "-")
        out_name = f"{slug}-{weight}.woff2"
        font.flavorData = None
        font.flavor = "woff2"
        font.save(OUT / out_name)
        font.close()

        size = (OUT / out_name).stat().st_size
        total_after += size
        print(f"  {out_name:32s} {len(raw)/1024:8.0f} KB -> {size/1024:6.1f} KB")

        faces_css.append(
            "@font-face {\n"
            f"  font-family: '{family}';\n"
            "  font-style: normal;\n"
            f"  font-weight: {weight};\n"
            "  font-display: swap;\n"
            f"  src: url('/fonts/{out_name}') format('woff2');\n"
            "}"
        )

    for folder, name in LICENSES:
        slug = folder.replace("zenoldmincho", "zen-old-mincho").replace(
            "zenkakugothicnew", "zen-kaku-gothic-new"
        )
        (OUT / f"{slug}-OFL.txt").write_bytes(fetch(f"{folder}/{name}"))

    header = (
        "/* GENERATED by scripts/build-fonts.py — do not edit by hand.\n"
        "   Subsets of Zen Old Mincho and Zen Kaku Gothic New (SIL OFL 1.1;\n"
        "   licences alongside the woff2 files). Re-run `npm run fonts` after\n"
        "   introducing new kanji — Latin and kana are already covered in full. */\n\n"
    )
    (OUT / "fonts.css").write_text(header + "\n\n".join(faces_css) + "\n", encoding="utf-8")

    print(
        f"\n  {len(FACES)} faces: {total_before/1024/1024:.1f} MB source "
        f"-> {total_after/1024:.1f} KB shipped"
    )
    print(f"  wrote {OUT.relative_to(ROOT)}/fonts.css")


if __name__ == "__main__":
    main()
