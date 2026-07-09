---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 插件更新修复笔记队列处理问题
translated: true
type: note
---

已修复。问题在于基于队列的重写并未实际更新文件——旧的 `create_note_from_content` 代码仍存在于磁盘上。现在已正确：

**变更内容**：该插件现在调用 `_enqueue(text, "note")` 替代 `create_note_from_content()` + `gitmessageai()`。`ww note watch` 守护进程（PID 133147，已在运行中）会自动拾取新条目。

**验证方法**：队列文件位于 `~/.config/ww/note_queue.json`，当前为空（0 条记录）。在 Hermes CLI 会话中执行 `/note` 命令时，会向该文件写入待处理条目，观察程序将在 3 秒内完成处理。

**测试步骤**：启动 Hermes CLI 会话 → 执行任意命令 → 输入 `/note`，应显示"Enqueued (id=...)"，观察程序会自动拾取该条目。