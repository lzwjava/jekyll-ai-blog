---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python 中的 @ 提及自动补全
translated: true
type: note
---


**问题：** Claude Code 和 OpenAI Codex 如何实现带有自动完成下拉菜单的 `@` 符号文件提及，以及我如何在 Python 中复制这个功能，因为我当前的基于 `readline` 的方法似乎有限？

**回答：**

## 为什么你的 `readline` 方法感觉困难

你的当前代码使用 Python 的 `readline` 模块，通过 `tab: complete` 来处理，这仅能处理**Tab 键触发的词边界完成**。它没有任何以下概念：

- 监视特定触发字符，如 `@`
- 内联显示**弹出下拉菜单**
- 在句子中间进行模糊/部分文件路径匹配

这是核心限制——`readline` 是为 shell 风格的完成而设计的，而不是丰富的内联提及触发。

---

## Claude Code 的实现方式

Claude Code 是一个 Node.js/TypeScript TUI 应用程序。其 `@` 自动完成使用基于 Rust 的模糊查找器在核心引擎中实现，而不是简单的 readline 钩子。从其问题跟踪器观察到的关键行为：

- 自动完成扫描相对于 git 仓库根目录的文件，而不仅仅是当前工作目录。
- `@` 字符会触发下拉菜单，随着你输入建议文件——这是一个由终端 UI 层渲染的完整 TUI 弹出窗口。
- 在 VS Code 中，按 `Option+K` / `Alt+K` 会插入带有文件路径和行号的 `@` 提及，例如 `@app.ts#5-10`。

关键架构点：Claude Code 渲染自己的终端 UI（像一个迷你编辑器），因此它可以完全控制每个按键，并渲染弹出菜单，而无需依赖 shell 的 readline。

---

## 正确的 Python 工具：`prompt_toolkit`

`prompt_toolkit` 是一个用于构建强大交互式命令行和终端应用程序的库——它可以作为 GNU readline 的非常高级的纯 Python 替代品，也可以用于构建全屏应用程序。

可以通过传递 `completer` 参数来添加自动完成——`Completer` 抽象基类的实例——并且 `complete_while_typing=True` 会使下拉菜单在你输入时自动出现，而无需 Tab。

以下是使用 `prompt_toolkit` 实现 `@` 触发文件自动完成的完整示例：

```python
import os
import glob
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion

class AtFileCompleter(Completer):
    """Triggers file suggestions after @ character."""

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        # Find the last @ in the current input
        at_pos = text.rfind("@")
        if at_pos == -1:
            return  # No @ found, no completions

        # Everything after the @ is the file prefix to match
        prefix = text[at_pos + 1:]

        # Don't trigger if there's a space after @
        if " " in prefix:
            return

        # Glob for matching files
        pattern = f"{prefix}*"
        matches = glob.glob(pattern) + glob.glob(os.path.join("**", pattern), recursive=True)

        seen = set()
        for path in sorted(matches)[:20]:  # limit to 20 results
            if path in seen:
                continue
            seen.add(path)
            # Completion replaces only the text after @
            yield Completion(
                path,
                start_position=-len(prefix),
                display=path,
                display_meta="file" if os.path.isfile(path) else "dir"
            )

def main():
    session = PromptSession(
        completer=AtFileCompleter(),
        complete_while_typing=True,   # popup appears as you type, no Tab needed
    )

    messages = []
    print("Type your message. Use @filename to reference files.\n")

    while True:
        try:
            user_input = session.prompt("> ")
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.strip() == ".exit":
            break

        # TODO: parse @mentions out of user_input before sending to LLM
        messages.append({"role": "user", "content": user_input})
        print(f"[Sending: {user_input}]\n")

if __name__ == "__main__":
    main()
```

---

## 关键概念解释

| 概念 | `readline` | `prompt_toolkit` |
| --- | --- | --- |
| 触发字符 | 仅 Tab | 任意字符（`@`、`/` 等） |
| 弹出下拉菜单 | 无 | 有，内联渲染 |
| 模糊匹配 | 无 | 有（通过 `FuzzyCompleter` 包装器） |
| 输入时完成 | 无 | 有（`complete_while_typing=True`） |
| 跨平台 | 仅 macOS/Linux | Windows + macOS + Linux |
| 多行输入 | 困难 | 内置 |

---

## 输入后解析 `@mentions`

一旦用户提交消息，你需要提取文件引用并注入内容：

```python
import re

def resolve_at_mentions(text):
    """Find all @file references and return (cleaned_text, file_contents_dict)."""
    mentions = re.findall(r"@(\S+)", text)
    file_contents = {}
    for path in mentions:
        if os.path.isfile(path):
            with open(path) as f:
                file_contents[path] = f.read()
    return text, file_contents
```

然后，你可以将文件内容前置到 LLM 消息上下文中，就像 Claude Code 在发送到 API 前解析 `@` 提及时所做的那样。

---

## 总结

Claude Code 的 `@` 提及用户体验感觉精致的原因，是因为它构建了自己的 **TUI 层**（使用 Rust/Ink 在 Node.js 中），而不是依赖 shell 的 readline。在 Python 中，`prompt_toolkit` 提供了相同的能力——触发字符感知的完成、下拉菜单、模糊匹配和跨平台支持——并且是 IPython、pgcli 和 mycli 等工具用于此类丰富终端自动完成的標準库。

**参考资料：**

- [prompt_toolkit documentation – Asking for input](https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html)
- [prompt_toolkit on PyPI](https://pypi.org/project/prompt-toolkit/)
- [Claude Code @ autocomplete – GitHub Issues](https://github.com/anthropics/claude-code/issues/1818)
- [Claude Code VS Code Extension Docs](https://code.claude.com/docs/en/vs-code)
