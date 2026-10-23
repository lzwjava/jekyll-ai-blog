---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复移动导航的换行与布局
translated: true
type: note
---

已修复。对 `index.html` 的两处更改：

1. 在 `.site-nav a` 上添加 **`white-space: nowrap`** — 这可以防止 "Work with me" 在导航被压缩时在按钮内换行成多行。

2. **移动端头部布局**（在 `@media (max-width: 620px)` 块中）— 在小屏手机上，头部现在换行到第二行：
   - `.header-inner` 使用 `flex-wrap: wrap` 且 `height: auto`，而不是固定的 60px 高度
   - `.site-nav` 移动到自己的整行（`order: 3; width: 100%`），位于 wordmark 和语言/主题工具下方，右对齐

因此，在移动端，导航链接（Research / Services / About / **Work with me**）位于单独的一行，CTA 保持在一行内，而不会被压缩到 wordmark 和工具旁边的多行中。