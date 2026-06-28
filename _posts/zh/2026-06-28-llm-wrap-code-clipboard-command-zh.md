---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM封装代码剪贴板命令
translated: true
type: note
---

完成。以下是已实现的内容：

**修改了 3 个文件：**

1. `ww/note/create_note_utils.py` — 新增 `wrap_code_snippets(content)` 函数，调用 LLM 将代码用带有语言提示的三反引号 Markdown 代码块包裹。非代码内容保持不变。

2. `ww/note/note_queue.py` — 更新 `enqueue_clipboard()` 方法，接受可选的 `text` 和 `code` 参数。当 `code=True` 时，在队列条目中存储 `"code": true`。

3. `ww/main.py` — 在 `note` 命令中添加 `--code` 参数处理：
   - 读取剪贴板 → 调用 `wrap_code_snippets()` LLM → 以 `code=True` 入队
   - 在重复检查之前执行（内容在入队时已被包裹）
   - 与 `ww note watch` 兼容，因为它像其他条目一样进入队列

**同时更新了：**
- 帮助文本：`ww note --code            用 LLM 包裹剪贴板中的代码，然后入队`
- Zsh 自动补全：为 `ww note` 添加 `--code` 和 `--sync` 参数

**流程：**
```
ww note --code
  → 读取剪贴板
  → LLM 将代码包裹在 ``` 代码块中
  → 入队（带上 code=true 标记）
  → ww note watch 消费条目 → 创建笔记 → 提交 → 推送
```