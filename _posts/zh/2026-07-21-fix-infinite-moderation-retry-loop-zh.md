---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复无限审核重试循环
translated: true
type: note
---

语法清晰。以下是修复的内容：

**问题**：`ww/gen_video/video.py` 中的 `_openrouter_image` 存在无限制的递归重试循环——当一条图像提示被内容审核拦截时，函数会清理该提示并调用自身。若清理后的版本同样被拦截，则会无限重试（在按下 Ctrl-C 之前，您已看到约 40 多次重试）。

**修复**：添加了 `retry_count` 参数（默认值为 0）和 `MAX_RETRIES = 3` 的上限。在连续 3 次失败后，程序会打印 "Moderation blocked after 3 retries — giving up" 并返回 `[]`，从而使场景转而使用暗色占位图片，而非无限循环。同时修复了首次补丁尝试导致的文件结构损坏（原函数被嵌套在 `_openrouter_chat` 内部）。现在两个函数均作为独立的模块级函数存在于正确位置。
