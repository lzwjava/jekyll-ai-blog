---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 笔记队列实现与问题
translated: true
type: note
---

好的，我已经阅读了所有注释代码。以下是实际情况：

**笔记模块有两个路径：**

1. **`ww note`**（无标志）→ `enqueue_clipboard()` — 读取剪贴板，添加到 `~/.config/ww/note_queue.json`，立即返回。这确实是队列路径。

2. **`ww note --sync`** → `note_workflow.main()` — 旧路径：检查未提交内容、拉取、创建笔记、修复 MathJax、提交并推送、打开浏览器。这不是队列方式——它是一个完整的同步流水线。

**队列处理：**

- `ww note process` → 从队列中取出待处理条目，创建笔记，提交并推送
- `ww note watch` → 后台守护进程，每 2 秒轮询一次队列文件并自动处理

**当前状态：** 队列文件位于 `~/.config/ww/note_queue.json`，且为空（`[]`）。

所以队列在代码中是实现了的。你具体说的不工作是指哪一方面？是：

1. `ww note` 实际上没有入队（剪贴板读取失败，或回退到旧路径）？
2. 监视器没有运行，导致入队的笔记从未被处理？
3. 摘要文档在某个具体细节上有误？
4. 其他问题？

你能说明一下你当前看到的实际行为与你期望的有什么不同吗？
