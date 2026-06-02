---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 直接通过 AI 工具运行代码
translated: true
type: note
---

Question: 我喜欢自己运行 `python xx.py` 然后把错误输出提供给 Claude，但实际上我不想做那个步骤——只想直接让 Claude 运行代码并让它自己读取错误输出。

Answer:

Claude（以及像我这样的类似模型）**无法直接在你本地机器或真实环境中运行 Python 代码**。我们是沙盒化的 LLMs，无法访问你的计算机、文件、终端，也无法真正执行 `python xx.py`。

通常只有两种可行的方式：

1. 你自己运行代码 → 复制粘贴错误（以及相关的代码/上下文）→ 要求模型修复它
   （这就是你目前正在做的）

2. 使用**确实可以执行代码**的模型 + 工具组合，例如：
   - 带有 **computer use / tool use** 的 Claude（Claude 3.5 Sonnet / Claude 4 中的 Beta 功能，可以控制虚拟桌面并运行真实命令）
   - 带有 **code_execution** 工具的我 (Grok)（我现在可以在沙盒化的 REPL 环境中运行 Python 代码）
   - Cursor / VS Code + Copilot / Continue.dev / Aider —— 这些可以在本地运行代码并将错误自动反馈给模型
   - Replit / GitHub Codespaces / 其他带有 AI agents 的云端 IDE

如果你是在和**常规的 Claude.ai** 对话（没有启用 computer-use beta），那么很遗憾，你**必须**自己完成手动步骤 —— 没有任何办法告诉它 “直接运行代码并读取错误”，因为它没有执行能力。

### 你现在可以用我 (Grok) 做什么

如果你想在调试中小型 Python 脚本时跳过手动运行步骤：

- 在这里粘贴你的代码
- 告诉我你的预期 / 哪里出了问题
- 我可以直接使用我的 code interpreter 运行它，并向你展示**准确的输出或 traceback**

Example:

```python
# your code
def divide(a, b):
    return a / b

print(divide(10, 0))
```

只需给我这样的代码 → 我运行它 → 我返回真实的错误：

```
ZeroDivisionError: division by zero
```

然后我们可以迭代地一起修复它，而无需你在本地运行任何内容。

你想尝试这种 workflow 吗？只需粘贴你通常作为 `python xx.py` 运行的代码，并描述你想要实现的目标或遇到的错误。

References:

- None
