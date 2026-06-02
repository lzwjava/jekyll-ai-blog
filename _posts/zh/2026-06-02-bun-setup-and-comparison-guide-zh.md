---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Bun 设置与比较指南
translated: true
type: note
---

**问：** 什么是 Bun？如何在 Bun 中设置自定义证书和注册源？它与 npm 相比如何？

**答：**

## 什么是 Bun？

Bun 是一个用 Zig 编写的全能 JavaScript 运行时 + 包管理器 + 打包器 + 测试运行器，它基于 JavaScriptCore（Safari 的引擎）而非 V8。核心设计目标：开箱即快，用一个二进制文件替代 Node.js/npm/webpack/jest。

**单个二进制文件中的核心组件：**
- 运行时（`bun run`）
- 包管理器（`bun install`，`bun add`）
- 打包器（`bun build`）
- 测试运行器（`bun test`）
- TypeScript/JSX 转译器（无需配置）

---

## Bun vs npm — 直接对比

| 特性 | Bun | npm |
|---|---|---|
| 编程语言 | Zig | JavaScript/C++ |
| JS 引擎 | JavaScriptCore | V8 |
| 安装速度 | 约快 10–25 倍（二进制锁文件，并行获取） | 基准线 |
| 锁文件 | `bun.lockb`（二进制） | `package-lock.json`（JSON） |
| 工作区支持 | 是 | 是 |
| TypeScript | 原生支持，零配置 | 需要 `ts-node` 或编译步骤 |
| `.env` 加载 | 内置 | 需要 `dotenv` |
| 测试运行器 | 内置（`bun test`，兼容 Jest） | 需要 Jest/Vitest |
| 打包器 | 内置 | 需要 webpack/esbuild/rollup |
| Node.js 兼容性 | 较高（约 95%）但非 100% | 100%（它就是 Node） |
| 成熟度 | 约 2023–2024 稳定版，仍在完善中 | 十年历史，久经考验 |

**安装速度**得益于：二进制锁文件（无需解析 JSON）、硬链接替代复制、并行 HTTP/2 获取，以及 Zig 对系统调用的紧密使用。

---

## 设置自定义注册源

### 全局（所有包）
```bash
bun config set registry https://your-registry.example.com
```

或者编辑 `~/.bunfig.toml`：
```toml
[install]
registry = "https://your-registry.example.com"
```

### 作用域注册源（例如 `@myorg`）
在 `bunfig.toml`（项目目录或 `~/.bunfig.toml`）中：
```toml
[install.scopes]
"@myorg" = { registry = "https://npm.myorg.internal", token = "YOUR_TOKEN" }
```

### 带认证（npm 风格的 token）
```toml
[install]
registry = "https://your-registry.example.com"

[install.registry]
token = "YOUR_NPM_TOKEN"
# 或者：
# username = "user"
# password = "pass"
```

---

## 设置自定义证书（SSL/TLS）

这是企业环境（例如你的银行内部代理使用自签名 CA）的痛点。

### 方案 1 — `bunfig.toml` 中的 `caFile`
```toml
[install]
caFile = "/path/to/your-ca-bundle.pem"
```

### 方案 2 — 系统信任存储
Bun 在 Linux/macOS 上遵循系统的 CA 存储。将你的证书添加到系统存储：

```bash
# Ubuntu
sudo cp your-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain your-ca.crt
```

### 方案 3 — `NODE_EXTRA_CA_CERTS`（Node 兼容环境变量）
```bash
export NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.pem
bun install
```
Bun 为了兼容性会识别此环境变量。

### 方案 4 — 禁用 TLS 验证（仅开发环境，切勿用于生产）
```toml
[install]
tlsRejectUnauthorized = false
```

---

## 完整的 `bunfig.toml` 示例（企业环境）

```toml
[install]
registry = "https://nexus.internal.bank.com/repository/npm-proxy/"
caFile = "/etc/ssl/certs/bank-internal-ca.pem"

[install.scopes]
"@bank-internal" = {
  registry = "https://nexus.internal.bank.com/repository/npm-private/",
  token = "YOUR_NEXUS_TOKEN"
}
```

---

## npm 等效命令速查表

```bash
# npm                          → bun
npm install                    → bun install
npm install express            → bun add express
npm install -D vitest          → bun add -d vitest
npm run dev                    → bun dev  (或 bun run dev)
npm config set registry <url>  → bun config set registry <url>
npx ts-node index.ts           → bun index.ts
npm test                       → bun test
```

---

## 你是否应该从 npm 切换到 Bun？

考虑到你的环境（AI CLI 工具、Node 脚本、银行代理环境）：

- **本地开发建议切换** — `bun install` 速度明显更快，TypeScript 开箱即用，`.env` 自动加载
- **CLI 工具建议切换** — `bun build --compile` 可以生成单文件可执行程序
- **企业环境需谨慎** — 证书/代理设置需要 `caFile` 或系统存储；某些原生插件无法保证 100% 兼容 Node.js
- **生产基础设施暂不建议** — 如果你在银行容器化部署 Node.js 服务，Node 在 100% 兼容性上仍然更安全
