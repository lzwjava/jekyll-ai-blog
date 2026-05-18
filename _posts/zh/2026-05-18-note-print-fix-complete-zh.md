---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 笔记打印修复完成
translated: true
type: note
---

修复已经正确完成。当前状态如下：

- `gitmessageai.py`：已移除 `_print_note_urls` 调用以及两个死函数（`_print_note_urls`、`_get_github_repo_url`）。不再出现 "Note created at" 内容。
- `note_workflow.py` 第166行：剩余的唯一一个 print 保持不变。每次调用只触发一次。

因此现在 `ww note create` 只会精确打印一行 `[info] Note created at ...`，而不是两行。死代码 `import re` 和 `argparse`（曾未使用？）——实际上 `argparse` 仍被 `__main__` 块使用。仅移除了作为死代码的 `import re`。

`note_workflow.py` 第166/168/170行具有互斥的 try/except 结构——只有一个分支会执行，因此那里也不会产生重复输出。