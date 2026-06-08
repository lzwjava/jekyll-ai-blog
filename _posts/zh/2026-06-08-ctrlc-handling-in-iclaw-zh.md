---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Iclaw中的Ctrl+C处理
translated: true
type: note
---

一切正常。以下是 3 处更改的总结：

**1. `iclaw/exec_tool.py` — 在 exec_command 中捕获 KeyboardInterrupt**  
当 Ctrl+C 在 `subprocess.run()` 期间触发时，现在会捕获 `KeyboardInterrupt` 并返回 `"Error: Command interrupted by user."`，而不是向上冒泡导致 iclaw 退出。

**2. `iclaw/main.py` 第 149 行 — 在提示符处按 Ctrl+C 不会退出**  
将 `EOFError`（Ctrl+D → 退出并显示 "Goodbye!"）与 `KeyboardInterrupt`（Ctrl+C → 仅清空该行并继续 REPL）分开处理。

**3. `iclaw/main.py` 第 626 行 — 在聊天/工具调用循环中按 Ctrl+C 取消当前回合**  
在进入聊天块之前保存 `msg_count_before = len(messages)`。当触发 `KeyboardInterrupt` 时，回滚该回合中添加的所有消息（`del messages[msg_count_before:]`），打印 "Interrupted."，并返回提示符。此更改覆盖了 API 调用、web_search、edit、浏览器工具等场景中的 Ctrl+C，而不仅仅是 exec。

关键点：`KeyboardInterrupt` 是 `BaseException`，而非 `Exception`，因此第 629 行已有的 `except Exception` 处理程序从未捕获到它——它总是向上冒泡到 REPL 循环并导致 iclaw 退出。
