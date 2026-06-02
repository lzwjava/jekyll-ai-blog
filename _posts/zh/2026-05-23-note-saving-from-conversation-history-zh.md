---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 对话历史笔记保存
translated: true
type: note
---

已完成。以下是实现的内容：

**对 2 个文件的 3 项更改：**

1. `hermes_cli/commands.py` — 在 `copy` 命令旁添加了 `CommandDef("note", ...)`
2. `cli.py` — 在 `process_command()` 中添加了调度 `elif canonical == "note":`
3. `cli.py` — 在 `_handle_copy_command()` 之后添加了 `_handle_note_command()` 方法（58 行）

**工作原理：**

`/note` 命令的作用与 `ww note` 相同 — 调用 `ww` 包中的 `create_note_from_content()` — 但不从剪贴板读取，而是直接从 `self.conversation_history` 获取最后一条助手的响应。

**用法：**

```
/note                        # 将最后一条响应保存为笔记（使用 LLM 生成标题）
/note 3                      # 保存第 3 条助手响应
/note --title "My Title"     # 使用自定义标题保存（跳过 LLM 标题生成）
/note --dir ~/my-notes       # 保存到自定义目录（默认：$BASE_PATH/notes）
/note 2 --title "Foo" --dir ~/notes
```

**关键细节：**
- 使用 `ww` 的 `create_note_from_content()` — 生成 front matter、slug，如果未提供 `--title` 则调用 LLM 生成标题
- 如果未安装 `ww` 则优雅降级（`pip install -e ~/projects/ww`）
- 笔记默认保存到 `$BASE_PATH/notes/`（与 `ww note` 相同），或通过 `--dir` 指定任意目录
- 不执行 git 操作、MathJax 修复或浏览器打开 — 仅创建文件。完整的 `ww note` 流程（git pull、push、mathjax）保留在 `ww` CLI 中

**测试方法：** 重启 Hermes，在获得响应后运行 `/note`。`ww` 包已安装在你的虚拟环境中。
