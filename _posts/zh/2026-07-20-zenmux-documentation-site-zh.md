---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ZenMux 文档站点
translated: true
type: note
---

这是 **ZenMux 文档站点** — [docs.zenmux.ai](https://docs.zenmux.ai) 的源代码仓库。

**ZenMux** 是一个 LLM API 聚合服务（统一的多模型 AI 提供商网关）。该仓库使用 **VitePress** 构建其文档站点，并包含以下特性：

- **双语** — 以中文优先的工作流，自动翻译为英文
- **自定义 VitePress 插件** — 带标签的 API 示例（`api-request` 容器）、通过 LZ-String 压缩的页面数据、基于区域设置的路径重写
- **AI 驱动的翻译流水线** — 利用 ZenMux API 自身（通过 `openai/gpt-5`）将 `zh/` 翻译为 `en/` 的脚本
- **GitHub Pages 部署** — `pnpm run build` 输出到 `docs/` 目录，推送到 `main` 分支时自动部署
- **自定义域名** — docs.zenmux.ai