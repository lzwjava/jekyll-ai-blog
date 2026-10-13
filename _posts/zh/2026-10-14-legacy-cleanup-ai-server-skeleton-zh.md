---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 遗留代码清理，AI服务器骨架
translated: true
type: note
---

已提交并推送到 `master`（`4db3aac`，41 个文件，+2067/−2938）：

- **清理**：移除了遗留的 webpack 构建、plupload 子模块和未使用的组件
- **新增**：`ai-server/index.js`（带检索的 SSE 聊天服务）和 `ai-server/ingest.js`

两点说明：

1. GitHub 在默认分支上标记了 141 个依赖项漏洞（2 个严重，61 个高危）——大部分来自旧的依赖树。以后值得跑一次 `npm audit`。
2. RAG 演示只完成了一半——当你重新拾起时，剩余的部分包括：种子语料 JSON、`vite.config.js` 中的 `/ai` 代理、`LiveView` 中的“助手”标签页，以及流式 `AssistantPanel.vue` 组件。