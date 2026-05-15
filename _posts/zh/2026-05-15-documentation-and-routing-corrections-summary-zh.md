---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 文档与路由修正摘要
translated: true
type: note
---

一切正常。以下是问题摘要及修复内容：

**发现的问题（文档问题，非代码缺陷）：**

1. `ww image screenshot` 与顶层命令 `ww screenshot` 重复 — 相同模块、相同功能。根据您对顶层命令的偏好，`image screenshot` 路径已冗余。

2. `ww image screenshot-linux` 没有顶层快捷方式，但应添加一个（`ww screenshot-linux`）。

3. 帮助文本中提到 `--delay`（暗示为标志参数），但代码中将其作为**位置参数** `[DELAY]` 使用。

**所做修改：**

- **main.py 帮助文本**：从 Image 部分移除 `ww image screenshot` 和 `ww image screenshot-linux`。在 Screenshot 部分添加 `ww screenshot-linux`。
- **main.py 路由**：从 `image` 组处理器中移除 `screenshot` 和 `screenshot-linux`。添加顶层 `screenshot-linux` 路由（位于现有 `screenshot` 旁）。
- **README.md**：将截图条目从 Image 表格移至 Screenshot 表格，分别为 `ww screenshot [DELAY]` 和 `ww screenshot-linux`。