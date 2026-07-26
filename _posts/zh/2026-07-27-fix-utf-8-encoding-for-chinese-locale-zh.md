---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复中文区域设置的UTF-8编码
translated: true
type: note
---

所有三个修复已正确应用。以下是所做的更改总结：

**问题：** 在Windows中文区域设置（gbk/cp936）下，`Path.read_text()` 默认使用系统编码而非UTF-8，导致读取队列JSON文件时出现 `'gbk' codec can't decode byte 0x94` 错误。

**应用的修复：**

1. **`ww/note/note_queue.py` — `_load_queue()`（第28行）：** 将 `qf.read_text()` 改为 `qf.read_text(encoding="utf-8")`，使JSON加载明确使用UTF-8。

2. **`ww/note/note_queue.py` — `_save_queue()`（第33行）：** 将 `tmp.write_text(...)` 改为 `tmp.write_text(..., encoding="utf-8")`，确保文件也以UTF-8写入（与读取保持一致）。

3. **`ww/note/note_watcher.py`（第88行）：** 在监听器的变更检测循环中，将 `qf.read_text()` 改为 `qf.read_text(encoding="utf-8")`。