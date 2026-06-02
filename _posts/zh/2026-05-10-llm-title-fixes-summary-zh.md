---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型标题修正总结
translated: true
type: note
---

好的，以下是三个修复的总结：

**问题：** LLM 忽略了“仅回复标题”的指令，返回了 1518 个字符的分析，而不是一个 6 个单词的标题。代码随后因 `ValueError` 崩溃。

**修复（跨 2 个文件的 3 处更改）：**

1. **`create_note_utils.py` -- 在 API 调用中设置 `max_tokens=60`：** 这是关键的修复。之前没有设置 `max_tokens`，因此模型可以自由地长篇大论。60 个 token 对于 6 个单词来说绰绰有余，但会截断过长的解释。

2. **`create_note_utils.py` -- 重试逻辑（尝试 3 次）：** 不再在第一次标题过长时崩溃，而是最多重试 3 次并发出警告。只有在重试耗尽后才抛出 `ValueError`。

3. **`create_note_from_clipboard.py` -- 更强的提示词：** 将冗长的指令改为简洁的提示词，结尾为 `\n\nTitle:` -- 这促使模型仅用标题完成，对许多模型来说比命令式指令效果更好。
