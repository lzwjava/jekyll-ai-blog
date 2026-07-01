---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Node.js 25 破坏与修复
translated: true
type: note
---

**问题：** 为什么在 Node.js v25.3.0 上 `@sourcegraph/amp` 会崩溃并报错 `TypeError: Cannot read properties of undefined (reading 'prototype')`，如何修复？

**答案：**

## 根本原因

这是一个**已知的 Node.js v25 兼容性问题**，不是您的代码 bug。错误发生是因为像 `@sourcegraph/amp` 这样的工具的依赖链中包含依赖已弃用的 `SlowBuffer` API 的包，该 API 在 Node.js v25.0.0 中被移除（标记为“End-of-Life”），符合 **DEP0030**。

具体来说，`SlowBuffer.prototype` 在 Node.js v25+ 中不再存在，因此当打包代码尝试访问它的 `.prototype` 时，会得到 `undefined` 并抛出错误。

这个问题影响了生态系统中许多 CLI 工具——CLI 抛出 `TypeError: Cannot read properties of undefined (reading 'prototype')` 错误，因为 Node.js 25 移除了对 `SlowBuffer` 的支持。

---

## 解决方案

### ✅ 选项 1：降级 Node.js（推荐——最快的修复）

切换到仍支持 `SlowBuffer` 的 Node.js LTS 版本：

```bash
# Using nvm
nvm install 22
nvm use 22

# Or install Node.js v22 LTS from nodejs.org
```

Node.js **v20** 或 **v22** (LTS) 是最稳定的选择，完全兼容 `@sourcegraph/amp`。

---

### ✅ 选项 2：使用 Node 版本管理器固定版本

如果您使用 `nvm`，在项目中添加 `.nvmrc` 文件：

```bash
echo "22" > .nvmrc
nvm use
```

---

### ✅ 选项 3：等待 `@sourcegraph/amp` 更新

上游包需要更新其传递依赖——特别是 JWT/认证链中使用的 `buffer-equal-constant-time` 或类似依赖 `SlowBuffer` 的库。正确的修复是更新这些传递依赖，使用 `crypto.timingSafeEqual()` 而不是 `SlowBuffer.prototype.equal`。检查 Sourcegraph/Amp GitHub 仓库以获取更新版本。

---

## 总结表格

| Node.js 版本 | 与 `@sourcegraph/amp` 兼容？ |
| --- | --- |
| v18 (LTS) | ✅ 是 |
| v20 (LTS) | ✅ 是 |
| v22 (LTS) | ✅ 是 |
| v25+ | ❌ 否（SlowBuffer 已移除） |

**TL;DR：** 降级到 Node.js v20 或 v22 LTS。您的 Node v25.3.0 是崩溃的直接原因。

**参考资料：**

- [Node.js v25 破坏性变更 - SlowBuffer 移除 (Claude Code 问题)](https://github.com/anthropics/claude-code/issues/9628)
- [Salesforce CLI 上的相同问题](https://github.com/forcedotcom/cli/issues/3460)
