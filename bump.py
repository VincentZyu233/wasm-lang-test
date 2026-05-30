#!/usr/bin/env python3
"""
版本号管理脚本

用途：
- 自动更新所有配置文件中的版本号
- 一次性更新所有相关文件

使用方法：
  python bump.py 0.1.2          # 直接设置版本号
  python bump.py --version 0.1.2
  python bump.py -v 0.1.2
"""

import sys
import re
import json
import argparse
from pathlib import Path


def parse_version(version_str):
    """解析版本号字符串为 (major, minor, patch)"""
    parts = version_str.split('.')
    return tuple(map(int, parts[:3]))


def format_version(major, minor, patch):
    """格式化版本号为字符串"""
    return f"{major}.{minor}.{patch}"


def update_json_file(filepath, new_version):
    """更新 JSON 文件中的版本号"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['version'] = new_version

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

    print(f"✓ Updated {filepath}")


def update_toml_file(filepath, new_version):
    """更新 TOML 文件中的版本号"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r'version\s*=\s*"[^"]*"',
        f'version = "{new_version}"',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated {filepath}")


def update_yaml_file(filepath, new_version):
    """更新 YAML 文件中的版本号"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r'version:\s*[^\n]*',
        f'version: {new_version}',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description='版本号管理脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  python bump.py 0.1.2
  python bump.py --version 0.1.2
  python bump.py -v 0.1.2
        '''
    )

    parser.add_argument(
        'version',
        nargs='?',
        help='目标版本号 (例: 0.1.2)'
    )
    parser.add_argument(
        '--version', '-v',
        dest='version_flag',
        help='目标版本号 (例: 0.1.2)'
    )

    args = parser.parse_args()

    # 获取版本号
    new_version = args.version or args.version_flag

    if not new_version:
        parser.print_help()
        sys.exit(1)

    # 验证版本号格式
    try:
        parse_version(new_version)
    except (ValueError, IndexError):
        print(f"错误: 无效的版本号格式 '{new_version}'")
        print("正确格式: X.Y.Z (例: 0.1.2)")
        sys.exit(1)

    # 获取当前版本
    root = Path(__file__).parent
    package_json = root / 'package.json'

    with open(package_json, 'r', encoding='utf-8') as f:
        current_data = json.load(f)

    current_version = current_data['version']

    print(f"\n📦 版本更新: {current_version} → {new_version}\n")

    # 需要更新的文件列表
    files_to_update = [
        (root / 'package.json', 'json'),
        (root / 'ui' / 'package.json', 'json'),
        (root / 'packages' / 'wasm-lang-test-rust' / 'Cargo.toml', 'toml'),
        (root / 'packages' / 'wasm-lang-test-dart' / 'pubspec.yaml', 'yaml'),
    ]

    # 更新所有文件
    for filepath, file_type in files_to_update:
        if not filepath.exists():
            print(f"⚠ 文件不存在: {filepath}")
            continue

        if file_type == 'json':
            update_json_file(filepath, new_version)
        elif file_type == 'toml':
            update_toml_file(filepath, new_version)
        elif file_type == 'yaml':
            update_yaml_file(filepath, new_version)

    print(f"\n✅ 版本号已更新为 {new_version}")
    print(f"\n下一步: git add -A && git commit -m 'chore: bump version to {new_version}'")


if __name__ == '__main__':
    main()
