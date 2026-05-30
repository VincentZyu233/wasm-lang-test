#!/usr/bin/env python3
"""
Generate animated SVG showing language byte distribution.
"""

import os
import math
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Language file extensions (exclude markdown, yaml, json)
LANG_EXTENSIONS = {
    '.rs': 'Rust',
    '.cpp': 'C++',
    '.go': 'Go',
    '.dart': 'Dart',
    '.kt': 'Kotlin',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
}

# Language colors (GitHub style)
LANG_COLORS = {
    'Rust': '#dea584',
    'C++': '#f34b7d',
    'Go': '#00ADD8',
    'Dart': '#00B4AB',
    'Kotlin': '#A97BFF',
    'JavaScript': '#f1e05a',
    'TypeScript': '#3178c6',
}

IGNORE_DIRS = {'.git', 'node_modules', '.github', 'build', 'dist', 'target', '.gradle', 'pkg'}
IGNORE_FILES = {'.gitignore', '.npmrc', 'package-lock.json'}


def count_bytes_by_language(root_dir):
    """Count bytes for each language."""
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
    """Format bytes to human readable."""
    if bytes_val >= 1_000_000:
        return f"{bytes_val / 1_000_000:.1f} MB"
    if bytes_val >= 1_000:
        return f"{bytes_val / 1_000:.1f} KB"
    return f"{bytes_val} B"


def generate_svg(stats):
    """Generate animated SVG bar chart."""
    total = sum(stats.values())
    if total == 0:
        return ""

    bar_height = 32
    bar_padding = 2
    row_height = bar_height + bar_padding
    content_start_y = 120
    height = content_start_y + len(stats) * row_height + 40
    svg_width = 480

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{height}" viewBox="0 0 {svg_width} {height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Mono:wght@400;600&display=swap');
      .bg {{ fill: #0d1117; }}
      .title {{ font-family: 'Noto Sans Mono', monospace; font-size: 16px; font-weight: 600; fill: #64b5f6; }}
      .subtitle {{ font-family: 'Noto Sans Mono', monospace; font-size: 11px; fill: #8b949e; }}
      .lang-name {{ font-family: 'Noto Sans Mono', monospace; font-size: 14px; fill: #e6edf3; }}
      .lang-pct {{ font-family: 'Noto Sans Mono', monospace; font-size: 13px; fill: #8b949e; }}
      .bar-bg {{ fill: #161b22; }}
      @keyframes fadeInRight {{ from {{ opacity: 0; transform: translateX(-8px); }} to {{ opacity: 1; transform: translateX(0); }} }}
      @keyframes fadeInDown {{ from {{ opacity: 0; transform: translateY(-10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
      .row {{ animation: fadeInRight 0.6s ease forwards; opacity: 0; }}
      .title-anim {{ animation: fadeInDown 0.8s ease forwards; opacity: 0; }}
    </style>
  </defs>

  <rect class="bg" width="{svg_width}" height="{height}"/>

  <text class="title title-anim" x="20" y="30">📊 wasm-lang-test · Code Distribution</text>
  <text class="subtitle title-anim" style="animation-delay: 0.2s;" x="20" y="48">Total: {format_bytes(total)}</text>
  <text class="subtitle title-anim" style="animation-delay: 0.3s;" x="20" y="68">Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</text>
'''

    # Calculate max percentage for bar scaling
    max_percent = max((size / total * 100) for size in stats.values()) if stats else 0

    # Draw each language row
    for i, (lang, size) in enumerate(stats.items()):
        y = content_start_y + i * row_height
        percentage = (size / total) * 100
        delay = 0.4 + i * 0.1
        color = LANG_COLORS.get(lang, '#8b8b8b')

        # Bar width calculation (relative to max)
        bar_width = 280 * (percentage / max_percent) if max_percent > 0 else 0

        svg += f'''  <g class="row" style="animation-delay: {delay:.1f}s;">
    <circle cx="30" cy="{y + bar_height / 2}" r="6" fill="{color}"/>
    <text class="lang-name" x="44" y="{y + bar_height / 2 + 4}">{lang}</text>
    <rect class="bar-bg" x="160" y="{y + 4}" width="280" height="{bar_height - 8}" rx="4"/>
    <rect x="160" y="{y + 4}" width="0" height="{bar_height - 8}" rx="4" fill="{color}" opacity="0.85">
      <animate attributeName="width" from="0" to="{bar_width}" dur="0.8s" begin="{delay}s" fill="freeze"/>
    </rect>
    <text class="lang-pct" x="450" y="{y + bar_height / 2 + 4}" text-anchor="end">{percentage:.1f}%</text>
  </g>
'''

    svg += '</svg>'
    return svg


def main():
    root = Path(__file__).parent.parent
    stats = count_bytes_by_language(str(root))

    if not stats:
        print("No source files found")
        return

    svg = generate_svg(stats)

    # Write SVG
    svg_path = root / 'docs' / 'lang-stats.svg'
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg)

    print(f"✅ Generated {svg_path}")
    print("\nLanguage Statistics:")
    total = sum(stats.values())
    for lang, size in stats.items():
        pct = (size / total) * 100
        print(f"  {lang}: {size:,} bytes ({pct:.1f}%)")


if __name__ == '__main__':
    main()
