---
audio: false
generated: true
image: false
lang: zh
layout: post
title: /title 命令详解
translated: true
type: note
---

以下是 `/title` 工作原理的完整说明：

```
提问："/title"命令如何工作？它什么时候设置，什么时候不设置？
      在多个窗口中如何知道当前会话的标题？

回答：

=== /title 命令 ===

`/title <name>` 为当前会话设置一个人类可读的标签。
`/title`（不带参数）显示当前会话 ID 和标题。

=== 标题何时被设置 ===

当你运行 /title 时，有两种情况：

1. 会话已存在于数据库中（你已发送至少一条消息）：
   -> 标题通过 session_db.set_session_title() 立即设置
   -> 你会看到："Session title set: <name>"

2. 会话尚未存在（全新窗口，未发送任何消息）：
   -> 标题被排队为 `_pending_title`
   -> 你会看到："Session title queued: <name> (will be saved on first message)"
   -> 在你发送第一条消息时，agent 循环调用 _ensure_db_session()，
      创建数据库行，然后应用排队的标题
   -> 你会看到："Session title applied: <name>"

如果你恢复一个会话（`/resume <id>`），标题会显示在
恢复确认中：↻ Resumed session <id> "<title>" (N messages)

=== 终端标签页标题显示什么 ===

这里是关键的混淆点：

- TUI 模式（--tui）：终端标签页标题设置为：
    "<marker> <model> · <short cwd>"
  例如："◆ openrouter/anthropic/claude-sonnet-4 · ~/projects/hermes-agent"
  它不显示会话标题。它显示的是模型名称。

- 经典 CLI（无 --tui）：根本不发送任何终端标题转义序列。
  终端标签页显示你的 shell 设置的内容。

所以如果你打开 5 个窗口，终端标签页都显示相同的内容（模型名称 + 当前工作目录），使得它们无法区分。

=== 如何区分不同窗口 ===

1. /title（无参数）—— 显示此窗口的会话 ID 和标题
2. /status —— 显示会话 ID、模型、提供商、消息数量
3. /sessions —— 列出最近的会话及其标题和 ID
4. /resume —— 也显示一个包含标题的会话表格

会话标题存储在 SQLite 数据库中，因此一旦设置，即使重启也会持久存在。

=== 针对 5-6 个窗口的实用建议 ===

当你打开一个新窗口并知道它的用途时，立即运行：

  /title debugging-auth-bug
  /title refactor-cli-module
  /title gpu-training-experiment

然后当你迷失时，/title 或 /sessions 会告诉你哪个窗口是哪个。标题甚至在第一次消息之前就会被排队，所以可以立即安全地设置。

注意：终端标签页标题（在 iTerm2/Terminal.app 中）不会随之改变——它始终显示模型名称。会话标题是 Hermes 内部的，通过 /title 和 /sessions 可见。
```

需要我改进这个说明吗？例如，我可以让 TUI 的终端标签页标题实际显示会话标题而不是（或除了）模型名称——这将直接解决你的“5-6 个窗口”问题。只需在 `ui-tui/src/app/useMainApp.ts` 中做一个小改动即可。
