---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Copilot Agent Runs Commands Locally in Terminal
translated: false
type: note
---

**Question:** When using VS Code Copilot in agent mode to run a command, is that command actually executed in the VS Code terminal, and can we check the progress in the embedded terminal?

**Answer:**

Yes, that's correct.

In **GitHub Copilot agent mode** in VS Code (the local interactive agent accessed via the Chat view or Copilot Edits view by selecting "Agent" mode), when the agent needs to execute terminal commands (e.g., `npm install`, `dotnet test`, `cargo build`, starting a dev server, etc.), it runs them in VS Code's **integrated terminal**.

Key points about how this works:

- The agent typically uses the **default terminal profile** (or sometimes creates a new terminal instance).
- Commands are executed in your local environment (on your machine), not in a remote/cloud sandbox.
- The agent often requires your confirmation before running a terminal command (unless you enable auto-approve in settings).
- You can observe the command execution and its output directly in the VS Code integrated terminal panel.
- In the Copilot chat interface, the agent usually shows the command it ran (or wants to run), and provides options like "Show Output" (inline) or "Show Terminal" to jump to the full terminal view.
- Progress, errors, build output, test results, etc., appear in real time in that terminal — just like any normal command you type yourself.
- The agent can read back the terminal output to understand success/failure and iterate (fix bugs, adjust commands, etc.).

This is different from the separate **GitHub-hosted Copilot coding agent** (which runs in the cloud via GitHub Actions and does not use your local VS Code terminal).

So yes — when using agent mode in VS Code and Copilot proposes/runs commands, you can (and should) watch the embedded terminal to follow what's happening, see live output, and intervene if needed.

**References:**

- [Introducing GitHub Copilot agent mode (preview)](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)
- [Use tools in chat - Terminal commands](https://code.visualstudio.com/docs/copilot/chat/chat-tools)
- [Agent mode 101: All about GitHub Copilot's powerful mode](https://github.blog/ai-and-ml/github-copilot/agent-mode-101-all-about-github-copilots-powerful-mode)
