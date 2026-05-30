<!--
  PLAN.md - AI 助手通用项目规划文件

  本文件为所有 AI 助手（Claude、Gemini、GPT 等）提供项目特定的指导和规范。
  所有 AI 工具应在开始工作前读取此文件。
-->

# wasm-lang-test 项目规划

## 🎯 项目概述

对比 C++、Go、Rust、Dart、Kotlin 五种语言在 WebAssembly 中的性能表现。

## 📋 版本管理规范（必读）

**重要**：所有代码修改前必须先更新版本号。

### 版本更新方式

```bash
# 直接指定版本号
python bump.py 0.1.2
python bump.py --version 0.1.2
python bump.py -v 0.1.2
```

### 自动更新的文件

- `package.json` (根目录)
- `ui/package.json`
- `packages/wasm-lang-test-rust/Cargo.toml`
- `packages/wasm-lang-test-dart/pubspec.yaml`

### 标准工作流

```bash
# 1. 修改代码
# 2. 更新版本号
python bump.py 0.1.2

# 3. 提交
git add -A
git commit -m "feat: description build publish"
git push origin main
```

## 🔑 CI/CD 关键词

### 提交信息关键词

- `build action` - 仅编译（不发布）
- `build publish` - 编译 + 发布到 npm

示例：
```bash
git commit -m "feat: optimize matrix multiplication build publish"
```

## 📁 项目结构

```
wasm-lang-test/
├── packages/
│   ├── wasm-lang-test-cpp/
│   ├── wasm-lang-test-go/
│   ├── wasm-lang-test-rust/
│   ├── wasm-lang-test-dart/
│   └── wasm-lang-test-kotlin/
├── ui/                    # Web UI（不发布到 npm）
├── .github/workflows/
│   └── build.yml         # CI/CD 配置
├── docs/
├── bump.py               # 版本管理脚本
├── PLAN.md               # 本文件（通用规划）
├── CLAUDE.md             # Claude 特定配置
├── GEMINI.md             # Gemini 特定配置
└── README.md
```

## 🧪 四个测试题目

1. **斐波那契** - 递归密集型 (fib(35))
2. **快速排序** - 内存操作 (100,000 个数)
3. **矩阵乘法** - 计算密集型 (512×512)
4. **字符串处理** - 文本处理 (单词频率)

## 📦 npm 包

发布到 npm registry：

- `@wasm-lang-test/rust`
- `@wasm-lang-test/go`
- `@wasm-lang-test/cpp`
- `@wasm-lang-test/dart`
- `@wasm-lang-test/kotlin`

## 🚀 开发工作流

### 修改 WASM 模块

```bash
# 1. 编辑源代码
# 2. 本地编译测试
npm run build:wasm

# 3. 更新版本
python bump.py 0.1.2

# 4. 提交
git add -A
git commit -m "feat: optimization build publish"
git push
```

### 修改 UI

```bash
# 1. 编辑 ui/ 目录
# 2. 启动开发服务器
npm run dev

# 3. 更新版本
python bump.py 0.1.2

# 4. 提交
git add -A
git commit -m "feat: ui improvements build action"
git push
```

## 📝 代码规范

### HTML/CSS/JS

- 添加详细的文件头注释（30+ 行）
- 每个函数/类都有 JSDoc 注释
- 使用中文注释说明功能

### 其他语言

- 遵循各语言的标准规范
- 添加必要的注释说明算法

## 🔗 重要文件

- `docs/build.md` - 构建和发布指南
- `docs/dev/20260530.cpp-go-rust.plan.md` - 项目规划
- `README.md` - 快速开始指南
- `.gitignore` - Git 忽略规则

## ⚠️ 常见问题

### Q: 忘记更新版本号怎么办？

A: 使用 `git amend` 修改最后一个 commit，然后重新运行 `bump.py`。

### Q: 如何本地测试 WASM 模块？

A:
```bash
npm install
npm run build:wasm
npm run dev
```

### Q: 如何手动发布到 npm？

A: 详见 `docs/build.md` 中的"手动发布"部分。

## 📞 联系方式

GitHub: https://github.com/VincentZyu233/wasm-lang-test

---

**最后更新**: 2026-05-30
**当前版本**: 0.1.2
