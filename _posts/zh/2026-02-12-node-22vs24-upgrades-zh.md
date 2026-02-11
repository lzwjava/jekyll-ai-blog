---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Node 22 与 24 关键升级指南
translated: true
type: note
---

**Question:** 比较 Node.js 22 和 Node.js 24。

**Answer:**

Node.js 22 和 Node.js 24 都是偶数版本的 **LTS** (Long-Term Support) 版本，Node.js 22 是之前的稳定 LTS（发布于 2024 年 4 月左右），而 Node.js 24 将在 2025 年 10 月成为当前的 LTS（发布于 2025 年 5 月，LTS 周期从 2025 年 10 月左右持续到 2028 年 4 月）。

Node.js 24 在性能（大多数情况下）、现代 JavaScript 特性、security 默认设置以及 developer experience 方面带来了显著改进，同时也引入了一些在迁移过程中需要注意的 breaking changes。

### 关键对比表

| 维度 | Node.js 22 | Node.js 24 | 胜出者 / 备注 |
|-------------------------|-----------------------------------------|--------------------------------------------------|---------------------------------------------|
| **发布与支持** | LTS (活跃至 2026 年 4 月) | LTS (活跃至 2028 年 4 月) | Node.js 24 (更长的支持周期) |
| **V8 Engine** | V8 12.4 | V8 13.6 | Node.js 24 (更新的 JS 特性 + 性能) |
| **性能** | 稳健的基准 | 通用 JS/HTTP 负载通常快 15–30%；某些 native addon 案例（如 SQLite）可能出现回归 | 大多数情况下 Node.js 24 更好，可能存在性能回归 |
| **内置 fetch** | 可用 (基于 Undici) | Undici 7.0 → 更好的 HTTP/2, HTTP/3, connection pooling, 性能更好 | Node.js 24 |
| **Test Runner** | 稳定 | 稳定 + 更多默认值与改进 | Node.js 24 (更成熟) |
| **Permission Model** | Experimental | Stable (使用 `--allow-*` 标志控制 fs, net 等) | Node.js 24 (生产级安全) |
| **OpenSSL** | 3.0 / 3.x 系列 | OpenSSL 3.5 (默认 security level 2) | Node.js 24 (更严格的 crypto 默认设置) |
| **新 JS 特性** | ES2024 左右 | Float16Array, Error.isError, 全局 URLPattern, explicit resource management (`using`) 等 | Node.js 24 |
| **npm** | npm 10 | npm 11 (性能 + 安全改进) | Node.js 24 |
| **Breaking Changes** | — | 更严格的 fetch/AbortSignal, Buffer 行为, Windows path 修复, stream/pipe 错误现在会抛出, crypto 变更 | Node.js 22 (迁移问题较少) |
| **推荐用于生产环境** | 2026 年初的稳健保守选择 | 当前推荐的 LTS (截至 2026 年 2 月) | Node.js 24 (当前最佳 LTS) |

### 升级到 Node.js 24 的主要优势
- 更长的支持周期。
- 更好的通用 runtime 性能和内存使用（得益于 V8 13.6）。
- 生产就绪的安全特性（稳定的 permissions model，更严格的 OpenSSL 默认设置）。
- 与现代 web platform 对齐（增强的 fetch，全局 URLPattern，更新的 typed arrays）。
- 面向未来（大多数新的生态系统库将针对最近的 Node 版本）。

### 潜在缺点 / 迁移注意事项
- 包含数个 **breaking changes**（详见官方 v22 至 v24 迁移指南）。
- 在特定的 native modules / addons 中可能存在罕见的性能回归（例如某些 SQLite 绑定）。
- 需要测试更严格的验证和 crypto 行为。

总体而言，截至 2026 年 2 月，Node.js 24 是大多数新项目以及从 Node.js 22 升级生产负载的推荐版本，前提是您已经处理好了迁移步骤。

**参考资料：**

- [Node.js v22 到 v24 迁移指南](https://nodejs.org/en/blog/migrations/v22-to-v24)
- [Node.js 24.0.0 发布公告](https://nodejs.org/en/blog/release/v24.0.0)
- [Node.js 24 LTS 公告](https://nodejs.org/blog/release/v24.11.0)
- [Node.js 24 vs 22 特性与升级讨论](https://javascript.plainenglish.io/node-js-24-vs-22-in-2025-whats-new-what-breaks-and-how-to-upgrade-safely-10725e1b7247)