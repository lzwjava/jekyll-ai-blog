---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM Overrides 各版本支持指南
translated: true
type: note
---

你说得大部分都对！让我来澄清一下 npm 版本及其对 `overrides` 的支持情况：

**npm 和 `overrides` 支持：**

- **npm 6**: 不支持 `overrides` ❌
- **npm 7**: 不支持 `overrides` ❌
- **npm 8.3.0+**: 第一个支持 `overrides` 的版本 ✅
- **npm 8.1**: 不支持 `overrides`（正如你所指出的）

**Node.js 版本及其内置的 npm：**

- **Node 14**: 附带 npm 6.x（不支持 `overrides`）
- **Node 16**: 根据具体版本附带 npm 7.x - 8.x
  - 大多数 Node 16 版本附带 npm 7.x 或早期的 npm 8.x（8.3 之前）
  - 只有较晚的 Node 16 patch 版本才包含 npm 8.3+
- **Node 18**: 附带 npm 8.19.x 或更高版本（支持 `overrides`） ✅

**结论：**

你需要 **npm 8.3.0 或更高版本** 才能使 `overrides` 生效。最稳妥的方法是：

- 使用 Node 18+（这能保证 npm 8.3+）
- 或者在 Node 16 上手动升级 npm 到 8.3+：`npm install -g npm@8.3.0`

所以，没错，你的理解是正确的——Node 18 是开箱即用支持 `overrides` 的可靠选择！
