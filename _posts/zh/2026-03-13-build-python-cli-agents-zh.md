---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 像 Codex 一样构建 Python CLI 代理
translated: true
type: note
---

问题：Python 可以用来构建类似于 Claude Code 或 OpenAI Codex 的 CLI 工具吗？

回答：

**是的，当然可以。** Python 是构建类似于 Claude Code 或 Codex 的 AI 驱动 CLI 编码代理的最佳语言之一。事实上，许多流行的开源替代品和这些工具的教育克隆版完全使用 Python 构建。

---

## Claude Code / Codex 的工作原理是什么？

在构建自己的工具之前，了解这些工具实际做什么会很有帮助。一旦理解了核心概念，构建编码代理就变得出奇简单——你不需要 PhD 或代理框架，只需要 Python 和清晰的思考。主要机制包括：

1. **代理循环** — LLM 接收用户输入，决定调用哪些工具，执行它们，然后循环返回。
2. **工具** — 读取文件、编写代码、运行 shell 命令、执行测试。
3. **内存/上下文管理** — 处理大型代码库，而不会溢出 LLM 的上下文窗口。
4. **系统提示 / 指令** — 指导模型的行为。

最小代理模式如下所示：

```
User --> messages[] --> LLM --> response
                            | stop_reason == "tool_use"?
                           / \
                          yes  no
                          |    |
                    execute   return text
                    tools
                    append results
                    loop back --> messages[]
```

每个 AI 编码代理都需要这个循环。生产级代理会添加策略、权限和生命周期层。

---

## 如何在 Python 中构建一个

### Core Libraries You Need

| 库 | 用途 |
|---|---|
| `anthropic` / `openai` | LLM API 调用 |
| `click` 或 `typer` | CLI 参数解析 |
| `rich` | 终端 UI（颜色、旋转器） |
| `subprocess` | 执行 shell 命令 |
| `pathlib` | 文件系统操作 |

### Minimal Working Example

```python
import anthropic
import subprocess

client = anthropic.Anthropic()

tools = [
    {
        "name": "run_bash",
        "description": "Execute a bash command",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "Read a file's contents",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    }
]

def run_agent(user_prompt: str):
    messages = [{"role": "user", "content": user_prompt}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # If no tool calls, print final answer and exit
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(block.text)
            break

        # Execute tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "run_bash":
                    result = subprocess.run(
                        block.input["command"],
                        shell=True, capture_output=True, text=True
                    )
                    output = result.stdout or result.stderr
                elif block.name == "read_file":
                    with open(block.input["path"]) as f:
                        output = f.read()

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output
                })

        # Append assistant response and tool results, then loop
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    import sys
    run_agent(" ".join(sys.argv[1:]))
```

像这样运行：`python agent.py "list all Python files and count lines in main.py"`

---

## 为完整 CLI 工具添加的关键组件

### 1. 合适的 CLI 接口（使用 `typer`）

```python
import typer
app = typer.Typer()

@app.command()
def main(prompt: str, model: str = "claude-sonnet-4-20250514"):
    run_agent(prompt, model)

if __name__ == "__main__":
    app()
```

### 2. 文件读写/编辑工具

赋予代理写入文件的能力，而不仅仅是读取。这是任何编码代理的核心——没有写入权限，它只能建议，而无法实现。

### 3. 上下文管理

LLM 的上下文窗口有限，即使能容纳整个代码库，也不要不加区分地倾倒数百个文件，那会浪费且令人困惑。代理会花费大部分推理能力来判断什么是相关的。解决方案包括让模型 grep 特定符号、构建文件索引，或使用 embeddings。

### 4. 沙箱 / 安全性

在执行 shell 命令之前，对其进行验证。你可以使用 Docker 容器或限制代理可写入的目录。

### 5. 流式输出（用于用户体验）

使用 Anthropic SDK 的 `client.messages.stream()`，让用户实时看到输出，而不是等待。

---

## 实际世界的 Python 项目示例

- **learn-claude-code** (GitHub: shareAI-lab) 是一个 Python 参考实现，通过 12 个渐进式会话从简单循环构建到隔离的自主执行，打造 Claude Code 风格的代理。
- **Aider** 可通过 `pip install aider-chat` 安装，支持 100+ 种语言，具有智能代码库映射和自动 git 提交。
- **claude-code-builder** 是一个 AI 驱动的 Python CLI 工具，使用 Claude Agent SDK 自动化整个软件开发生命周期，从规范到部署。

---

## 使用 Anthropic 的官方 Agent SDK

Agent SDK 提供了与 Claude Code 本身相同的工具、代理循环和上下文管理。它可作为脚本和 CI/CD 的 CLI 使用，或作为 Python 和 TypeScript 包提供完全的程序化控制。

```bash
pip install claude-agent-sdk
```

---

## 总结

| 功能 | Python 能力 |
|---|---|
| LLM API 调用 | ✅ `anthropic`、`openai` SDK |
| CLI 接口 | ✅ `typer`、`click`、`argparse` |
| 文件系统工具 | ✅ `pathlib`、`os` |
| Shell 执行 | ✅ `subprocess` |
| 丰富的终端 UI | ✅ `rich` 库 |
| 流式输出 | ✅ SDK 流式支持 |
| MCP 服务器集成 | ✅ 通过 `mcp` Python SDK |

Python 完全有能力构建生产级的 AI CLI 工具。Claude Code 和 Codex 相对于 Python 构建工具的优势仅在于与各自模型提供商的更深集成，但凭借当今的开放 SDK，这个差距非常小。

参考资料：

- [Build a Coding Agent from Scratch: Python Tutorial](https://www.siddharthbharath.com/build-a-coding-agent-python-tutorial/)
- [learn-claude-code (GitHub)](https://github.com/shareAI-lab/learn-claude-code)
- [Anthropic Agent SDK - Run Claude Code Programmatically](https://code.claude.com/docs/en/headless)
- [claude-code-builder (GitHub)](https://github.com/krzemienski/claude-code-builder)
- [Top 10 Open-Source CLI Coding Agents 2025](https://dev.to/forgecode/top-10-open-source-cli-coding-agents-you-should-be-using-in-2025-with-links-244m)
