---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Safari内存使用报告摘要
translated: true
type: note
---

以下是 Safari 的内存使用情况：

| Process | RAM |
| --- | --- |
| **Safari** (main) | **339.5 MB** |
| Safari Platform Support Helper x3 | 20.7 / 23.8 / 23.8 MB |
| Safari History | 21.8 MB |
| Safari SandboxBroker | 26.5 MB |
| SafariBookmarksSyncAgent | 13.5 MB |
| Safari SearchHelper | 11.0 MB |
| Others (widget, import, agent, etc.) | 4-7 MB each |

TabsKiller 运行在其中一个 **SafariPlatformSupport.Helper** 进程（约 20-24 MB 的那些）中——Safari 将所有 Web 扩展托管在那里。该扩展本身几乎不增加额外开销，因为它仅仅包含：

- 后台页面：标签页事件监听器（`onCreated`、`onUpdated`、`onActivated`、`onRemoved`）
- 弹出页面：设置界面（仅在打开时占用内存）
- 无定时器、无网络请求、无 DOM 操作

该扩展已在运行中——既然您说它只保留 10 个标签页，那么 `checkToClose()` 逻辑会在每个标签页事件上执行。您可以通过查看浏览器控制台或打开弹出页面来验证您的最大标签页设置。
