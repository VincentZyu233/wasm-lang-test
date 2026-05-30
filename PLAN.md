<!--
  PLAN.md - Universal AI Assistant Project Guide

  This file provides project-specific guidance for all AI assistants (Claude, Gemini, GPT, etc.).
  All AI tools should read this file before starting work.

  Related AI Configuration Files:
  - [CLAUDE.md](./CLAUDE.md) - Claude-specific configuration
  - [GEMINI.md](./GEMINI.md) - Gemini-specific configuration
  - [.github/workflows/build.md](./.github/workflows/build.md) - CI/CD build guide
-->

# wasm-lang-test Project Plan

## 🎯 Project Overview

Performance comparison of C++, Go, Rust, Dart, and Kotlin in WebAssembly.

## 📋 Version Management (REQUIRED)

**Important**: Update version number before any code changes.

### Version Update Method

```bash
# Direct version specification
python bump.py 0.1.2
python bump.py --version 0.1.2
python bump.py -v 0.1.2
```

### Auto-Updated Files

- `package.json` (root)
- `ui/package.json`
- `packages/wasm-lang-test-rust/Cargo.toml`
- `packages/wasm-lang-test-dart/pubspec.yaml`

### Standard Workflow

```bash
# 1. Modify code
# 2. Update version
python bump.py 0.1.2

# 3. Commit
git add -A
git commit -m "feat: description build publish"
git push origin main
```

## 🔑 CI/CD Keywords

### Commit Message Keywords

- `build action` - Build only (no publish)
- `build publish` - Build + publish to npm

Example:
```bash
git commit -m "feat: optimize matrix multiplication build publish"
```

## 📁 Project Structure

```
wasm-lang-test/
├── packages/
│   ├── wasm-lang-test-cpp/
│   ├── wasm-lang-test-go/
│   ├── wasm-lang-test-rust/
│   ├── wasm-lang-test-dart/
│   └── wasm-lang-test-kotlin/
├── ui/                    # Web UI (not published to npm)
├── .github/workflows/
│   └── build.yml         # CI/CD configuration
├── docs/
├── bump.py               # Version management script
├── PLAN.md               # This file (universal guide)
├── CLAUDE.md             # Claude-specific config
├── GEMINI.md             # Gemini-specific config
└── README.md
```

## 🧪 Four Benchmark Tests

1. **Fibonacci** - Recursion-intensive (fib(35))
2. **Quick Sort** - Memory operations (100,000 numbers)
3. **Matrix Multiplication** - Compute-intensive (512×512)
4. **String Processing** - Text processing (word frequency)

## 📦 NPM Packages

Published to npm registry:

- `@wasm-lang-test/rust`
- `@wasm-lang-test/go`
- `@wasm-lang-test/cpp`
- `@wasm-lang-test/dart`
- `@wasm-lang-test/kotlin`

## 🚀 Development Workflow

### Modifying WASM Modules

```bash
# 1. Edit source code
# 2. Test locally
npm run build:wasm

# 3. Update version
python bump.py 0.1.2

# 4. Commit
git add -A
git commit -m "feat: optimization build publish"
git push
```

### Modifying UI

```bash
# 1. Edit ui/ directory
# 2. Start dev server
npm run dev

# 3. Update version
python bump.py 0.1.2

# 4. Commit
git add -A
git commit -m "feat: ui improvements build action"
git push
```

## 📝 Code Standards

### HTML/CSS/JS

- Add detailed file header comments (30+ lines)
- JSDoc comments for all functions/classes
- Use English comments for clarity

### Other Languages

- Follow language-specific standards
- Add necessary algorithm comments

## 🔗 Important Files

- `docs/build.md` - Build and publish guide
- `docs/dev/20260530.cpp-go-rust.plan.md` - Project planning
- `README.md` - Quick start guide
- `.gitignore` - Git ignore rules

## ⚠️ FAQ

### Q: Forgot to update version?

A: Use `git amend` to modify the last commit, then re-run `bump.py`.

### Q: How to test WASM modules locally?

A:
```bash
npm install
npm run build:wasm
npm run dev
```

### Q: How to manually publish to npm?

A: See "Manual Publishing" section in `docs/build.md`.

## 📞 Contact

GitHub: https://github.com/VincentZyu233/wasm-lang-test

---

**Last Updated**: 2026-05-30
**Current Version**: 0.1.2
