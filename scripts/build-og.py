"""Compose the social card as pure SVG paths, then hand it to sharp.

The previous version set live text and relied on whatever fonts happened to be
installed on the machine doing the render — which meant the card came out in
Georgia and Yu Mincho, not the site's faces. Converting every string to outlines
here removes that dependency entirely: the card renders identically anywhere,
and it actually matches the site.

Reads the same upstream TTFs cached by build-fonts.py. Run via `npm run og`.
"""

import io
import urllib.request
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".fontcache"
OUT_SVG = ROOT / "scripts" / "og.svg"
UPSTREAM = "https://raw.githubusercontent.com/google/fonts/main/ofl/"

MINCHO_600 = "zenoldmincho/ZenOldMincho-SemiBold.ttf"
MINCHO_400 = "zenoldmincho/ZenOldMincho-Regular.ttf"
KAKU_400 = "zenkakugothicnew/ZenKakuGothicNew-Regular.ttf"
KAKU_500 = "zenkakugothicnew/ZenKakuGothicNew-Medium.ttf"

WASHI = "#F7F3EB"
INK = "#2B2928"
STONE = "#57524c"
VERMILION = "#C73E3A"
GOLD = "#C9A96E"
INDIGO = "#223A5E"

_fonts = {}


def load(rel: str) -> TTFont:
    if rel in _fonts:
        return _fonts[rel]
    CACHE.mkdir(exist_ok=True)
    cached = CACHE / rel.replace("/", "_")
    if not cached.exists():
        print(f"  downloading {rel}")
        with urllib.request.urlopen(UPSTREAM + rel) as response:
            cached.write_bytes(response.read())
    font = TTFont(io.BytesIO(cached.read_bytes()))
    _fonts[rel] = font
    return font


def text_path(rel, string, size, x, y, tracking=0.0, anchor="start"):
    """Return (svg_path_d, advance_width) for `string` laid out at `size` px.

    y is the baseline. Tracking is in em units, matching CSS letter-spacing.
    """
    font = load(rel)
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    hmtx = font["hmtx"]

    # Measure first so we can honour the anchor.
    total = 0.0
    for ch in string:
        name = cmap.get(ord(ch))
        if name is None:
            continue
        total += hmtx[name][0] * scale + tracking * size

    start_x = x
    if anchor == "middle":
        start_x = x - total / 2
    elif anchor == "end":
        start_x = x - total

    parts = []
    pen_x = start_x
    for ch in string:
        name = cmap.get(ord(ch))
        if name is None:
            continue
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        d = pen.getCommands()
        if d:
            # SVG y grows downward; font y grows upward.
            parts.append(
                f'<path transform="translate({pen_x:.2f} {y:.2f}) '
                f'scale({scale:.5f} {-scale:.5f})" d="{d}"/>'
            )
        pen_x += hmtx[name][0] * scale + tracking * size

    return "".join(parts), total


def main():
    W, H = 1200, 630
    body = []

    body.append(f'<rect width="{W}" height="{H}" fill="{WASHI}"/>')

    # Ghost kanji, held inside the frame so a thumbnail crop never cuts it.
    ghost, _ = text_path(MINCHO_400, "創", 360, 948, 452, anchor="middle")
    body.append(f'<g fill="{INK}" fill-opacity="0.045">{ghost}</g>')

    body.append(
        f'<rect x="48" y="48" width="{W-96}" height="{H-96}" fill="none" '
        f'stroke="{GOLD}" stroke-width="1" stroke-opacity="0.55"/>'
    )

    eyebrow, _ = text_path(KAKU_500, "BACKEND · ML · MOBILE", 21, 104, 196, tracking=0.3)
    body.append(f'<g fill="{VERMILION}">{eyebrow}</g>')

    name, _ = text_path(MINCHO_600, "Uteytithya Nuon", 82, 104, 292)
    body.append(f'<g fill="{INK}">{name}</g>')

    # The brush stroke that sits under the name in the hero.
    body.append(
        '<path d="M104 322C154 313 222 309 300 311c72 2 143 7 215 3 34-2 59-4 81-6" '
        f'stroke="{INDIGO}" stroke-opacity="0.45" stroke-width="6" '
        'stroke-linecap="round" fill="none"/>'
    )

    sub, _ = text_path(
        KAKU_400, "Backend Developer — the strength beneath the floor", 29, 104, 382
    )
    body.append(f'<g fill="{STONE}">{sub}</g>')

    body.append(f'<rect x="104" y="436" width="52" height="1" fill="{GOLD}"/>')

    phrase, _ = text_path(MINCHO_400, "縁の下の力持ち", 26, 104, 492, tracking=0.22)
    body.append(f'<g fill="{STONE}" fill-opacity="0.85">{phrase}</g>')

    # Hanko, pressed off-square in the lower right.
    seal, _ = text_path(MINCHO_600, "技", 48, 47, 66, anchor="middle")
    body.append(
        '<g transform="translate(1012 432) rotate(-4)">'
        f'<rect x="0" y="0" width="94" height="94" rx="4" fill="none" '
        f'stroke="{VERMILION}" stroke-width="3" stroke-opacity="0.9"/>'
        f'<g fill="{VERMILION}" fill-opacity="0.9">{seal}</g>'
        "</g>"
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">' + "".join(body) + "</svg>"
    )
    OUT_SVG.write_text(svg, encoding="utf-8")
    print(f"  wrote {OUT_SVG.relative_to(ROOT)} ({len(svg)/1024:.0f} KB of outlines)")


if __name__ == "__main__":
    main()
