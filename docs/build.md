# wasm-lang-test 构建指南

## 概述

本项目对比 C++、Go、Rust 三种语言在 WebAssembly 中的性能表现。三个 wasm 模块发布到 npm，Web UI 在本地开发和维护。

## 项目结构

```
wasm-lang-test/
├── packages/
│   ├── wasm-lang-test-cpp/        # @wasm-lang-test/cpp
│   ├── wasm-lang-test-go/         # @wasm-lang-test/go
│   └── wasm-lang-test-rust/       # @wasm-lang-test/rust
├── ui/                            # Web UI（本地开发）
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── .github/workflows/
│   └── build.yml                  # CI/CD 流程
└── docs/
    └── build.md                   # 本文档
```

## 快速开始

### 1. 本地开发

#### 克隆项目
```bash
git clone https://github.com/your-org/wasm-lang-test.git
cd wasm-lang-test
```

#### 安装依赖
```bash
npm install
```

#### 编译 wasm 模块
```bash
npm run build:wasm
```

#### 启动 UI 开发服务器
```bash
npm run dev
```

访问 `http://localhost:5173` 查看性能测试页面。

### 2. 发布流程（仅 wasm 模块）

#### 步骤 1：配置 npm Token

1. 访问 [npm 官网](https://www.npmjs.com)
2. 登录账户，进入 **Account Settings** → **Tokens**
3. 点击 **Generate New Token** → 选择 **Automation**
4. 复制生成的 token

#### 步骤 2：配置 GitHub Secrets

1. 进入 GitHub 仓库 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 名称：`NPM_TOKEN`
4. 值：粘贴上面复制的 npm token
5. 点击 **Add secret**

#### 步骤 3：更新版本号

编辑 `package.json`，更新版本号：

```json
{
  "version": "0.1.0"
}
```

#### 步骤 4：提交并推送

```bash
# 更新版本号
npm version patch  # 或 minor/major

# 提交包含 [wasm] 关键词的 commit
git commit -m "feat: update wasm modules [wasm]"
git push origin main
```

**重要**：提交信息必须包含 `[wasm]` 关键词才能触发发布流程。

## CI/CD 流程详解

### 触发条件

- 推送到 `main` 分支
- 修改 `packages/` 目录下的文件
- 提交信息包含 `[wasm]` 关键词（触发发布）
- 手动触发 `workflow_dispatch`

### 编译阶段（并行）

#### Rust 编译
- 使用 `wasm-pack` 编译
- 输出：`pkg/` 目录（包含 `.wasm`、`.js`、`.d.ts`）
- 时间：~2-3 分钟

#### Go 编译
- 使用 `GOOS=js GOARCH=wasm` 编译
- 输出：`wasm_exec.wasm`
- 时间：~1-2 分钟

#### C++ 编译
- 使用 Emscripten 编译
- 输出：`main.wasm` 和 `main.js`
- 时间：~3-5 分钟

### 发布阶段

**条件**：所有编译成功 + 提交信息包含 `[wasm]`

1. **准备包**
   - 为每个模块生成 `package.json`
   - 设置版本号、描述、入口文件

2. **发布到 npm**
   - 发布 `@wasm-lang-test/rust`
   - 发布 `@wasm-lang-test/go`
   - 发布 `@wasm-lang-test/cpp`
   - 使用 `--provenance` 标志进行签名

3. **同步到 GitHub Packages**
   - 发布到 `npm.pkg.github.com`
   - 使用 `GITHUB_TOKEN` 自动认证

4. **创建 Release**
   - 生成 GitHub Release
   - 标签：`v{version}`
   - 包含安装说明和签名信息

## npm 包详情

### @wasm-lang-test/rust
```json
{
  "name": "@wasm-lang-test/rust",
  "version": "0.1.0",
  "description": "Rust WASM benchmark module",
  "main": "wasm_lang_test_rust.js",
  "types": "wasm_lang_test_rust.d.ts"
}
```

### @wasm-lang-test/go
```json
{
  "name": "@wasm-lang-test/go",
  "version": "0.1.0",
  "description": "Go WASM benchmark module",
  "main": "wasm_exec.wasm"
}
```

### @wasm-lang-test/cpp
```json
{
  "name": "@wasm-lang-test/cpp",
  "version": "0.1.0",
  "description": "C++ WASM benchmark module",
  "main": "main.wasm"
}
```

## 使用已发布的包

### 安装
```bash
npm install @wasm-lang-test/rust @wasm-lang-test/go @wasm-lang-test/cpp
```

### 在代码中使用

#### Rust 模块
```javascript
import init, { fibonacci } from '@wasm-lang-test/rust';

await init();
const result = fibonacci(35);
```

#### Go 模块
```javascript
import wasmModule from '@wasm-lang-test/go';

const go = new Go();
const result = await WebAssembly.instantiate(wasmModule);
```

#### C++ 模块
```javascript
import Module from '@wasm-lang-test/cpp';

const instance = await Module();
const result = instance._fibonacci(35);
```

## 故障排除

### 发布失败：401 Unauthorized

**原因**：npm token 无效或过期

**解决**：
1. 重新生成 npm token
2. 更新 GitHub Secrets 中的 `NPM_TOKEN`

### 发布失败：Package already exists

**原因**：版本号已存在

**解决**：
```bash
npm version patch  # 增加版本号
git push origin main
```

### 编译失败：Command not found

**原因**：缺少编译工具

**解决**：
- Rust：确保安装了 `wasm-pack`
- Go：确保 Go 版本 ≥ 1.21
- C++：确保安装了 Emscripten

## 性能签名

所有发布的包都使用 `--provenance` 标志进行签名，包含以下信息：

- **Built and signed on GitHub Actions**
- 构建时间戳
- 提交 SHA
- 工作流程 ID

验证签名：
```bash
npm audit signatures
```

## 版本管理

### 版本号规则

遵循 [Semantic Versioning](https://semver.org/):

- **MAJOR**：不兼容的 API 变更
- **MINOR**：向后兼容的功能添加
- **PATCH**：向后兼容的 bug 修复

### 更新版本

```bash
# Patch 版本（0.1.0 → 0.1.1）
npm version patch

# Minor 版本（0.1.0 → 0.2.0）
npm version minor

# Major 版本（0.1.0 → 1.0.0）
npm version major
```

## 监控构建

### 查看构建日志

1. 进入 GitHub 仓库 **Actions** 标签
2. 选择最新的 workflow run
3. 点击具体的 job 查看详细日志

### 常见日志位置

- **编译日志**：各个 build-* job 的输出
- **发布日志**：publish-npm job 的输出
- **Release 创建**：最后的 Create Release step

## 最佳实践

1. **提交信息规范**
   - 使用 `[wasm]` 标记发布相关的 commit
   - 示例：`feat: optimize matrix multiplication [wasm]`

2. **版本号管理**
   - 每次发布前更新版本号
   - 保持三个模块版本号同步

3. **本地测试**
   - 本地编译验证无误后再推送
   - 在 Web UI 中测试已发布的包

4. **文档**
   - 更新 CHANGELOG
   - 记录性能改进或 bug 修复

## 相关资源

- [npm 官方文档](https://docs.npmjs.com/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Rust WASM 指南](https://rustwasm.org/)
- [Go WASM 指南](https://github.com/golang/go/wiki/WebAssembly)
- [Emscripten 文档](https://emscripten.org/docs/)
