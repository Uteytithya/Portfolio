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

# The card speaks the same language as the site it links to. A social preview
# showing a design the site no longer has is worse than no preview at all.
VOID = "#0B0C0E"
STEEL = "#15181C"
BONE = "#E6E8EA"
ASH = "#A6ADB5"
EDGE = "#2A2E34"
VOLT = "#E8DC55"
SIGNAL = "#4DD8E8"

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

    body.append(f'<rect width="{W}" height="{H}" fill="{VOID}"/>')

    # The engineering grid, as on the page itself.
    for gx in range(96, W, 96):
        body.append(f'<rect x="{gx}" y="0" width="1" height="{H}" fill="{EDGE}" fill-opacity="0.5"/>')
    for gy in range(96, H, 96):
        body.append(f'<rect x="0" y="{gy}" width="{W}" height="1" fill="{EDGE}" fill-opacity="0.5"/>')

    # Hairline frame, with brackets on two corners.
    body.append(
        f'<rect x="48" y="48" width="{W-96}" height="{H-96}" fill="none" '
        f'stroke="{EDGE}" stroke-width="1"/>'
    )
    body.append(
        f'<g stroke="{VOLT}" stroke-width="3" fill="none">'
        '<path d="M64 100 V64 H100"/>'
        f'<path d="M{W-64} {H-100} V{H-64} H{W-100}"/>'
        "</g>"
    )

    # Eyebrow, with the diamond marker the hero uses.
    body.append(f'<rect x="104" y="150" width="9" height="9" fill="{VOLT}" transform="rotate(45 108.5 154.5)"/>')
    eyebrow, _ = text_path(KAKU_400, "BACKEND / ML / MOBILE", 19, 132, 161, tracking=0.22)
    body.append(f'<g fill="{VOLT}">{eyebrow}</g>')

    # The name, in caps on two lines.
    for i, line in enumerate(("UTEYTITHYA", "NUON")):
        nm, _ = text_path(KAKU_500, line, 86, 104, 262 + i * 92)
        body.append(f'<g fill="{BONE}">{nm}</g>')

    # Registration rule: a measured line with a marked origin.
    body.append(f'<rect x="104" y="394" width="52" height="3" fill="{VOLT}"/>')
    body.append(f'<rect x="156" y="395" width="300" height="1" fill="{EDGE}"/>')

    sub, _ = text_path(
        KAKU_400, "Backend developer — the strength beneath the floor", 25, 104, 452
    )
    body.append(f'<g fill="{ASH}">{sub}</g>')

    loc, _ = text_path(KAKU_400, "Phnom Penh", 17, 104, 500, tracking=0.14)
    body.append(f'<g fill="{SIGNAL}">{loc}</g>')

    # Unit stamp, chamfered like every plate on the site.
    seal, _ = text_path(KAKU_500, "技", 46, 47, 64, anchor="middle")
    body.append(
        '<g transform="translate(1000 428)">'
        f'<path d="M0 0 H80 L94 14 V94 H14 L0 80 Z" fill="{STEEL}" stroke="{VOLT}" stroke-width="2"/>'
        f'<g fill="{VOLT}">{seal}</g>'
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
