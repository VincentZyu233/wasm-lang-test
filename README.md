# wasm-lang-test

🚀 对比 C++、Go、Rust、Dart、Kotlin 五种语言在 WebAssembly 中的性能表现。

## 📊 语言分布

![Language Distribution](docs/lang-stats.svg)

这张 SVG 现在由本地 `python bump.py <version>` 自动更新，不再由 GitHub Actions 回写仓库。

## 快速开始

### 方式 1：使用已发布的 npm 包（推荐）

```bash
# 克隆项目
git clone https://github.com/VincentZyu233/wasm-lang-test.git
cd wasm-lang-test
# 安装依赖（包括已发布的 wasm 模块）
npm install
# 启动开发服务器
npm run dev
```

访问 `http://localhost:60531` 查看性能测试页面。

### 方式 2：本地编译 wasm 模块

如果要修改 wasm 模块代码，需要本地编译：

#### 前置要求

- **Rust**: `rustup` + `wasm-pack`
- **Go**: Go 1.21+
- **C++**: Emscripten

#### 编译步骤

```bash
# 编译所有 wasm 模块
npm run build:wasm
# 或单独编译
cd packages/wasm-lang-test-rust && wasm-pack build --target bundler --release
cd packages/wasm-lang-test-go && GOOS=js GOARCH=wasm go build -o wasm_exec.wasm ./cmd/main.go
cd packages/wasm-lang-test-cpp && emcc src/main.cpp -o main.js -s WASM=1 -O3
```

#### 启动 UI

```bash
npm run dev
```

## 项目结构

```
wasm-lang-test/
├── packages/
│   ├── wasm-lang-test-cpp/        # C++ WASM 模块
│   ├── wasm-lang-test-go/         # Go WASM 模块
│   └── wasm-lang-test-rust/       # Rust WASM 模块
├── ui/                            # Web UI（性能测试页面）
│   ├── index.html
│   ├── style.css
│   ├── main.js
│   └── package.json
├── .github/workflows/
│   └── build.yml                  # CI/CD 流程
└── docs/
    ├── build.md                   # 构建文档
    └── dev/20260530.cpp-go-rust.plan.md
```

## 四个测试题目

| 测试 | 特性 | 输入 | 指标 |
|------|------|------|------|
| 斐波那契 | 递归密集 | fib(35) | 执行时间 |
| 快速排序 | 内存操作 | 100,000 个数 | 排序时间 |
| 矩阵乘法 | 计算密集 | 512×512 矩阵 | 乘法时间 |
| 字符串处理 | 文本处理 | 单词频率统计 | 处理时间 |

## 发布流程

### 自动发布（GitHub Actions）

提交包含关键词的 commit：

```bash
# 先 bump 版本，并自动更新 docs/lang-stats.svg
python bump.py 0.1.8
# 仅编译
git commit -m "feat: xxx build action"
# 编译 + 发布到 npm
git commit -m "feat: xxx build publish"
git push origin main
```

### 手动发布

详见 [docs/build.md](docs/build.md)

## npm 包

已发布到 npm registry：

- [![npm](https://img.shields.io/npm/v/@wasm-lang-test/rust?color=cb3837&logo=npm)](https://www.npmjs.com/package/@wasm-lang-test/rust) `@wasm-lang-test/rust` — Rust 实现
- [![npm](https://img.shields.io/npm/v/@wasm-lang-test/go?color=cb3837&logo=npm)](https://www.npmjs.com/package/@wasm-lang-test/go) `@wasm-lang-test/go` — Go 实现
- [![npm](https://img.shields.io/npm/v/@wasm-lang-test/cpp?color=cb3837&logo=npm)](https://www.npmjs.com/package/@wasm-lang-test/cpp) `@wasm-lang-test/cpp` — C++ 实现
- [![npm](https://img.shields.io/npm/v/@wasm-lang-test/dart?color=cb3837&logo=npm)](https://www.npmjs.com/package/@wasm-lang-test/dart) `@wasm-lang-test/dart` — Dart 实现
- [![npm](https://img.shields.io/npm/v/@wasm-lang-test/kotlin?color=cb3837&logo=npm)](https://www.npmjs.com/package/@wasm-lang-test/kotlin) `@wasm-lang-test/kotlin` — Kotlin 实现

## 文档

- [构建指南](docs/build.md) - npm token 配置、CI/CD 详解
