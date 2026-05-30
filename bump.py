#!/usr/bin/env python3
"""
版本号管理脚本

用途：
- 自动更新所有配置文件中的版本号
- 支持 patch、minor、major 三种版本更新
- 一次性更新所有相关文件

使用方法：
  python bump.py patch   # 0.1.0 -> 0.1.1
  python bump.py minor   # 0.1.0 -> 0.2.0
  python bump.py major   # 0.1.0 -> 1.0.0
"""

import sys
import re
import json
from pathlib import Path


def parse_version(version_str):
    """解析版本号字符串为 (major, minor, patch)"""
    parts = version_str.split('.')
    return tuple(map(int, parts[:3]))


def format_version(major, minor, patch):
    """格式化版本号为字符串"""
    return f"{major}.{minor}.{patch}"


def bump_version(version_str, bump_type):
    """根据类型更新版本号"""
    major, minor, patch = parse_version(version_str)

    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")

    return format_version(major, minor, patch)


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

    # 匹配 version = "0.1.0" 格式
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

    # 匹配 version: 0.1.0 格式
    content = re.sub(
        r'version:\s*[^\n]*',
        f'version: {new_version}',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated {filepath}")


def main():
    if len(sys.argv) != 2:
        print("用法: python bump.py [patch|minor|major]")
        sys.exit(1)

    bump_type = sys.argv[1].lower()
    if bump_type not in ['patch', 'minor', 'major']:
        print("错误: 只支持 patch、minor、major")
        sys.exit(1)

    # 获取当前版本
    root = Path(__file__).parent
    package_json = root / 'package.json'

    with open(package_json, 'r', encoding='utf-8') as f:
        current_data = json.load(f)

    current_version = current_data['version']
    new_version = bump_version(current_version, bump_type)

    print(f"\n📦 版本更新: {current_version} → {new_version} ({bump_type})\n")

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
