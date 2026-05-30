#!/usr/bin/env python3
"""Generate a GitHub-friendly SVG showing language byte distribution."""

import base64
import io
import os
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
from html import escape

LANG_EXTENSIONS = {
    ".rs": "Rust",
    ".cpp": "C++",
    ".go": "Go",
    ".dart": "Dart",
    ".kt": "Kotlin",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
}

LANG_COLORS = {
    "Rust": "#dea584",
    "C++": "#f34b7d",
    "Go": "#00ADD8",
    "Dart": "#00B4AB",
    "Kotlin": "#A97BFF",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".github",
    "build",
    "dist",
    "target",
    ".gradle",
    "pkg",
}
IGNORE_FILES = {".gitignore", ".npmrc", "package-lock.json"}

SVG_WIDTH = 520
BAR_HEIGHT = 30
BAR_PADDING = 2
FONT_FAMILY = "'LXGW WenKai Mono', 'Inter', 'Segoe UI', monospace"


def count_bytes_by_language(root_dir):
    stats = defaultdict(int)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for filename in filenames:
            if filename in IGNORE_FILES:
                continue
            ext = Path(filename).suffix.lower()
            if ext not in LANG_EXTENSIONS:
                continue
            filepath = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(filepath)
                lang = LANG_EXTENSIONS[ext]
                stats[lang] += size
            except OSError:
                pass
    return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))


def format_bytes(bytes_val):
    if bytes_val >= 1_000_000:
        return f"{bytes_val / 1_000_000:.1f} MB"
    if bytes_val >= 1_000:
        return f"{bytes_val / 1_000:.1f} KB"
    return f"{bytes_val} B"


def subset_font_to_ascii(ttf_path):
    try:
        from fontTools.subset import Subsetter
        from fontTools.ttLib import TTFont
        from fontTools.ttLib.woff2 import compress as woff2_compress

        font = TTFont(str(ttf_path))
        subsetter = Subsetter()
        subsetter.populate(unicodes=list(range(0x0020, 0x007F)))
        subsetter.subset(font)

        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        buf.seek(0)
        woff2_data = buf.read()
        font.close()

        b64 = base64.b64encode(woff2_data).decode("ascii")
        return b64
    except ImportError as e:
        print(f"  ⚠ font subsetting skipped: {e}", file=sys.stderr)
        return None


def build_font_face_css(ttf_path):
    b64 = subset_font_to_ascii(ttf_path)
    if not b64:
        return ""

    return f"""    @font-face {{
      font-family: 'LXGW WenKai Mono';
      font-style: normal;
      font-weight: 400;
      src: url(data:font/woff2;base64,{b64});
    }}
    @font-face {{
      font-family: 'LXGW WenKai Mono';
      font-style: normal;
      font-weight: 600;
      src: url(data:font/woff2;base64,{b64});
    }}
    @font-face {{
      font-family: 'LXGW WenKai Mono';
      font-style: normal;
      font-weight: 700;
      src: url(data:font/woff2;base64,{b64});
    }}"""


def generate_svg(stats, root_dir):
    total = sum(stats.values())
    if total == 0:
        return ""

    top_bar_y = 90
    top_bar_height = 13
    content_start_y = top_bar_y + top_bar_height + 16
    row_h = BAR_HEIGHT + BAR_PADDING
    footer_offset = 22
    height = content_start_y + len(stats) * row_h + footer_offset

    font_path = root_dir / "assets" / "fonts" / "LXGWWenKaiMono-Regular.ttf"
    font_face = build_font_face_css(font_path) if font_path.exists() else ""

    if not font_path.exists():
        print("  ⚠ font file not found, using system fallback", file=sys.stderr)

    parts = []

    parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{height}" viewBox="0 0 {SVG_WIDTH} {height}">
<defs>
  <style>
{font_face}
    .bg {{ fill: #0d1117; rx: 10; }}
    .header {{ font-family: {FONT_FAMILY}; font-size: 16px; font-weight: 600; fill: #64b5f6; }}
    .subtitle {{ font-family: {FONT_FAMILY}; font-size: 11px; fill: #8b949e; }}
    .lang-name {{ font-family: {FONT_FAMILY}; font-size: 11px; fill: #e6edf3; }}
    .lang-pct {{ font-family: {FONT_FAMILY}; font-size: 11px; fill: #8b949e; }}
    .bar-label {{ font-family: {FONT_FAMILY}; font-size: 11px; font-weight: 600; fill: #0d1117; }}
    .bar-bg {{ fill: #161b22; rx: 4; }}
    .top-bar-bg {{ fill: #161b22; rx: 6; }}
    @keyframes fadeInRight {{ from {{ opacity: 0; transform: translateX(-8px); }} to {{ opacity: 1; transform: translateX(0); }} }}
    @keyframes fadeInDown {{ from {{ opacity: 0; transform: translateY(-10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .row {{ animation: fadeInRight 0.6s ease forwards; opacity: 0; }}
    .title-anim {{ animation: fadeInDown 0.8s ease forwards; opacity: 0; }}
  </style>
</defs>

<rect class="bg" width="{SVG_WIDTH}" height="{height}" rx="10"/>

<text class="header title-anim" x="22" y="28">📊 wasm-lang-test · Code Distribution</text>
<text class="subtitle title-anim" style="animation-delay: 0.2s;" x="22" y="44">Total {format_bytes(total)} ({total:,} bytes)</text>
<text class="subtitle title-anim" style="animation-delay: 0.3s;" x="22" y="58">Auto update: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")} UTC</text>
<text class="subtitle title-anim" style="animation-delay: 0.4s;" x="22" y="72">Tracked: {", ".join(LANG_EXTENSIONS.keys())}</text>
''')

    clipped = SVG_WIDTH - 44
    parts.append(f'''<clipPath id="top-bar-clip">
  <rect x="22" y="{top_bar_y}" width="{clipped}" height="{top_bar_height}" rx="6"/>
</clipPath>
<rect class="top-bar-bg" x="22" y="{top_bar_y}" width="{clipped}" height="{top_bar_height}"/>
<g clip-path="url(#top-bar-clip)">
''')
    offset_x = 22.0
    for i, (lang, size) in enumerate(stats.items()):
        w = clipped * (size / total)
        delay = 0.3 + i * 0.05
        color = LANG_COLORS.get(lang, "#8b949e")
        parts.append(
            f'  <rect x="{offset_x:.1f}" y="{top_bar_y}" width="0" height="{top_bar_height}" fill="{color}">\n'
            f'    <animate attributeName="width" from="0" to="{w:.1f}" dur="0.6s" begin="{delay:.2f}s" fill="freeze"/>\n'
            f"  </rect>\n"
        )
        offset_x += w
    parts.append("</g>\n")

    max_pct = stats[list(stats.keys())[0]] / total * 100
    prog_x = 111.111
    prog_w = SVG_WIDTH - prog_x - 55
    row_h_total = BAR_HEIGHT + BAR_PADDING

    for i, (lang, size) in enumerate(stats.items()):
        y = content_start_y + i * row_h_total
        pct = size / total * 100
        fill_w = max(prog_w * pct / max_pct, 1)
        delay = 0.4 + i * 0.1
        color = LANG_COLORS.get(lang, "#8b949e")
        center_y = y + BAR_HEIGHT / 2

        parts.append(f'''<g class="row" style="animation-delay: {delay:.1f}s;">
  <circle cx="32" cy="{center_y:.0f}" r="6" fill="{color}"/>
  <text class="lang-name" x="46" y="{center_y + 4:.0f}" dominant-baseline="central">{escape(lang)}</text>
  <rect class="bar-bg" x="{prog_x:.0f}" y="{y + 4:.0f}" width="{prog_w:.0f}" height="{BAR_HEIGHT - 8:.0f}"/>
  <rect x="{prog_x:.0f}" y="{y + 4:.0f}" width="0" height="{BAR_HEIGHT - 8:.0f}" rx="4" fill="{color}" opacity="0.85">
    <animate attributeName="width" from="0" to="{fill_w:.1f}" dur="0.8s" begin="{delay:.1f}s" fill="freeze"/>
  </rect>
  <text class="bar-label" x="{prog_x + 8:.0f}" y="{center_y + 1:.0f}" dominant-baseline="central">{format_bytes(size)}</text>
  <text class="lang-pct" x="{prog_x + prog_w + 8:.0f}" y="{center_y + 1:.0f}" dominant-baseline="central">{pct:.1f}%</text>
</g>
''')

    footer_y = content_start_y + len(stats) * row_h_total + 16
    parts.append(
        f'<text class="subtitle" x="{SVG_WIDTH - 22}" y="{footer_y:.0f}" text-anchor="end">Unit: bytes</text>\n'
    )
    parts.append("</svg>\n")

    return "".join(parts)


def main():
    root = Path(__file__).parent.parent
    stats = count_bytes_by_language(str(root))

    if not stats:
        print("No source files found")
        return

    svg = generate_svg(stats, root)

    svg_path = root / "docs" / "lang-stats.svg"
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg, encoding="utf-8")

    print(f"\n✅ Generated {svg_path}")
    print("\nLanguage Statistics:")
    total = sum(stats.values())
    for lang, size in stats.items():
        pct = (size / total) * 100
        print(f"  {lang}: {size:,} bytes ({pct:.1f}%)")


if __name__ == "__main__":
    main()
