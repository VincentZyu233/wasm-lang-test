#!/usr/bin/env python3
"""
Generate animated SVG showing language byte distribution.
"""

import os
import json
from pathlib import Path
from collections import defaultdict

# Language file extensions
LANG_EXTENSIONS = {
    '.rs': 'Rust',
    '.cpp': 'C++',
    '.go': 'Go',
    '.dart': 'Dart',
    '.kt': 'Kotlin',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.md': 'Markdown',
}

IGNORE_DIRS = {'.git', 'node_modules', '.github', 'build', 'dist', 'target', '.gradle'}
IGNORE_FILES = {'.gitignore', '.npmrc', 'package-lock.json'}


def count_bytes_by_language(root_dir):
    """Count bytes for each language."""
    stats = defaultdict(int)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove ignored directories
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


def generate_svg(stats):
    """Generate animated SVG pie chart."""
    total = sum(stats.values())
    if total == 0:
        return ""

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']

    # Calculate angles
    angles = []
    current_angle = 0
    for lang, size in stats.items():
        percentage = (size / total) * 100
        angle = (size / total) * 360
        angles.append((lang, size, percentage, current_angle, angle))
        current_angle += angle

    # SVG header
    svg = f'''<svg viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
      }}
      .lang-segment {{ animation: fadeIn 0.5s ease-in-out forwards; }}
      .lang-label {{ font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; }}
      .lang-percent {{ font-family: Arial, sans-serif; font-size: 11px; }}
    </style>
  </defs>

  <!-- Title -->
  <text x="200" y="30" text-anchor="middle" style="font-size: 20px; font-weight: bold;">Language Distribution</text>
  <text x="200" y="50" text-anchor="middle" style="font-size: 12px; fill: #666;">by bytes</text>
'''

    # Draw pie segments
    for i, (lang, size, percentage, start_angle, angle) in enumerate(angles):
        color = colors[i % len(colors)]
        delay = i * 0.1

        # Convert to radians
        start_rad = (start_angle - 90) * 3.14159 / 180
        end_rad = (start_angle + angle - 90) * 3.14159 / 180

        # Calculate path
        x1 = 200 + 80 * (3.14159 / 180) * (start_angle - 90) / (3.14159 / 180)
        y1 = 250 + 80 * (3.14159 / 180) * (start_angle - 90) / (3.14159 / 180)
        x2 = 200 + 80 * (3.14159 / 180) * (start_angle + angle - 90) / (3.14159 / 180)
        y2 = 250 + 80 * (3.14159 / 180) * (start_angle + angle - 90) / (3.14159 / 180)

        large_arc = 1 if angle > 180 else 0

        # Simplified: use circle segments
        svg += f'''  <circle cx="200" cy="250" r="80" fill="{color}" opacity="0.8"
    style="animation: fadeIn 0.5s ease-in-out {delay}s both;" />
'''

    # Legend
    legend_y = 350
    for i, (lang, size, percentage, _, _) in enumerate(angles):
        color = colors[i % len(colors)]
        x = 20 + (i % 2) * 200
        y = legend_y + (i // 2) * 25

        svg += f'''  <rect x="{x}" y="{y}" width="12" height="12" fill="{color}" />
  <text x="{x + 18}" y="{y + 10}" class="lang-label">{lang}</text>
  <text x="{x + 18}" y="{y + 22}" class="lang-percent">{percentage:.1f}% ({size:,} bytes)</text>
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
