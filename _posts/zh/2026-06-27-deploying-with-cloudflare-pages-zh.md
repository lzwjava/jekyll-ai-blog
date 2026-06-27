---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Cloudflare Pages进行部署
translated: true
type: note
---

未安装。您可以选择以下任一方式：

**选项A：Cloudflare Dashboard（最简单）**
1. 前往 Cloudflare Pages → 创建项目
2. 连接您的 GitHub 仓库 `lzwjava/sec-edgar-gpt`
3. 设置：
   - 构建命令：（留空）
   - 构建输出目录：`website`
4. 部署

**选项B：安装 wrangler 并通过 CLI 部署**
```
npm install -g wrangler
wrangler pages deploy website --project-name=sec-edgar-gpt
```

选项A更简单 — 只需在 dashboard 中将输出目录设置为 `website`。