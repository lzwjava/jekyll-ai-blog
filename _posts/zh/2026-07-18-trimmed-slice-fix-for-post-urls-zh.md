---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修正裁剪切片后的文章URL
translated: true
type: note
---

**Bug 和修复总结**

文件：`_layouts/post.html:90-100`

**根本原因：** 在现有的 `replace` 过滤器从 `base_name` 中去除语言后缀（`-en`、`-zh`、`-hant`）后，一个多余的后处理块使用 `length - 3`（或针对 `hant` 的 `length - 5`）对**已经干净的名称**重新进行切片，导致从开头多切掉了 3 个字符。

对于 `2026-02-15-web-analytics-zh.md`：

1. `replace` 产生 `web-analytics`（正确）
2. 后切片：`base_name[:15]` → `web-analyt`（错误，只剩 12 个字符）
3. 选择的 URL 变为 `/web-analyt-zh` —— 返回 404

**修复：** 移除了整个后切片算术块。`replace` 步骤已经产生了正确的值，不需要其他任何操作。

应用该修复后，所有语言配对都能生成正确的 URL（已验证）。
