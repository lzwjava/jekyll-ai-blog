---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代理会话和屏幕重置命令
translated: true
type: note
---

来自 Hermes Agent 文档：

- `/reset`（别名 `/new`）：启动一个新会话。清除对话历史记录，让你从头开始，但保持终端屏幕不变。

- `/clear`：清除屏幕并启动一个新会话。本质上相当于 `/reset` 加上清除终端显示。

两者都会创建新会话。唯一的区别是 `/clear` 还会擦除可见的终端输出，让你从一个干净的屏幕开始。

注意：工具更改（启用/禁用工具集）会在 `/reset` 时生效——它们不会在对话过程中生效，因为那样会破坏提示缓存。
