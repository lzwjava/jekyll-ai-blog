---
audio: false
generated: true
image: false
lang: zh
layout: post
title: YAML反引号错误修复
translated: true
type: note
---

所有测试均通过。以下是我发现的问题及修复方法：

**根本原因** — 两个博客文件的 YAML 前置元数据 `title` 字段中包含了反引号 `` `ll uno` ``。未加引号的反引号是无效的 YAML 标记（YAML 解析器将 `` ` `` 视为无法启动任何标记的字符），这导致前置元数据解析静默失败，而测试发现了这个问题。

**已修复的文件：**

- `_posts/en/2026-07-13-ll-uno-arduino-serial-monitor-en.md`
- `_posts/zh/2026-07-13-ll-uno-arduino-serial-monitor-zh.md`

**修复方法：** 将标题值用双引号括起来，内部使用单引号：`title: "'ll uno' Arduino Serial Monitor"` — 这是有效的 YAML，并保留了 `ll uno` 周围代码格式的意图。
