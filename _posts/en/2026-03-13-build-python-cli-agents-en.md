---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build Python CLI Agents Like Codex
translated: false
type: note
---

Question: Can Python be used to build a CLI tool similar to Claude Code or OpenAI Codex?

Answer:

**Yes, absolutely.** Python is one of the best languages for building AI-powered CLI coding agents like Claude Code or Codex. In fact, many popular open-source alternatives and educational clones of these tools are built entirely in Python.

---

## What Makes Claude Code / Codex Work?

Before building your own, it helps to understand what these tools actually do. Building a coding agent is surprisingly straightforward once you understand the core concepts — you don't need a PhD or an agent framework, just Python and clear thinking. The core mechanics are:

1. **An agent loop** — the LLM receives user input, decides which tools to call, executes them, and loops back.
2. **Tools** — read files, write code, run shell commands, execute tests.
3. **Memory/context management** — handle large codebases without overflowing the LLM's context window.
4. **A system prompt / instructions** — guides the model's behavior.

The minimal agent pattern looks like this:

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
Every AI coding agent needs this loop. Production agents add policy, permissions, and lifecycle layers.

---

## How to Build One in Python

### Core Libraries You Need

| Library | Purpose |
|---|---|
| `anthropic` / `openai` | LLM API calls |
| `click` or `typer` | CLI argument parsing |
| `rich` | Terminal UI (colors, spinners) |
| `subprocess` | Execute shell commands |
| `pathlib` | File system operations |

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

Run it like: `python agent.py "list all Python files and count lines in main.py"`

---

## Key Components to Add for a Full CLI Tool

### 1. Proper CLI Interface (using `typer`)
```python
import typer
app = typer.Typer()

@app.command()
def main(prompt: str, model: str = "claude-sonnet-4-20250514"):
    run_agent(prompt, model)

if __name__ == "__main__":
    app()
```

### 2. File Read/Write/Edit Tools
Give the agent the ability to write to files, not just read them. This is the core of any coding agent — without write access, it can only suggest, not implement.

### 3. Context Management
LLMs have a limited context window, and even if you could fit an entire codebase, indiscriminately dumping hundreds of files would be wasteful and confusing. The agent would spend most of its reasoning power figuring out what's relevant. Solutions include letting the model grep for specific symbols, building a file index, or using embeddings.

### 4. Sandboxing / Safety
Before executing shell commands, validate them. You can use Docker containers or restrict which directories the agent can write to.

### 5. Streaming Output (for UX)
Use `client.messages.stream()` with Anthropic SDK so users see output in real time rather than waiting.

---

## Real-World Python Projects That Did This

- **learn-claude-code** (GitHub: shareAI-lab) is a Python reference implementation that builds a Claude Code-style agent from scratch across 12 progressive sessions, from a simple loop to isolated autonomous execution.
- **Aider** is installable via `pip install aider-chat` and supports 100+ languages with intelligent codebase mapping and automatic git commits.
- **claude-code-builder** is an AI-powered Python CLI tool that automates the entire software development lifecycle using the Claude Agent SDK, from specification to deployment.

---

## Using Anthropic's Official Agent SDK

The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code itself. It's available as a CLI for scripts and CI/CD, or as Python and TypeScript packages for full programmatic control.

```bash
pip install claude-agent-sdk
```

---

## Summary

| Feature | Python Capability |
|---|---|
| LLM API calls | ✅ `anthropic`, `openai` SDKs |
| CLI interface | ✅ `typer`, `click`, `argparse` |
| File system tools | ✅ `pathlib`, `os` |
| Shell execution | ✅ `subprocess` |
| Rich terminal UI | ✅ `rich` library |
| Streaming output | ✅ SDK streaming support |
| MCP server integration | ✅ Via `mcp` Python SDK |

Python is fully capable of building production-grade AI CLI tools. The only thing Claude Code and Codex have over a Python-built tool is deeper integration with their respective model providers, but with the open SDKs available today, that gap is very small.

References:

- [Build a Coding Agent from Scratch: Python Tutorial](https://www.siddharthbharath.com/build-a-coding-agent-python-tutorial/)
- [learn-claude-code (GitHub)](https://github.com/shareAI-lab/learn-claude-code)
- [Anthropic Agent SDK - Run Claude Code Programmatically](https://code.claude.com/docs/en/headless)
- [claude-code-builder (GitHub)](https://github.com/krzemienski/claude-code-builder)
- [Top 10 Open-Source CLI Coding Agents 2025](https://dev.to/forgecode/top-10-open-source-cli-coding-agents-you-should-be-using-in-2025-with-links-244m)