---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Claude Code Uses Git Bash on Windows
translated: false
type: note
---

Yes, based on recent developments, Claude Code (an AI coding tool from Anthropic) on Windows does trigger `git-bash.exe` to run shell commands. It often uses Git Bash as the environment for executing commands, especially in native Windows setups without WSL. This can result in pop-up terminals for command execution, and there are known configurations, extensions (like in VS Code), and troubleshooting steps related to ensuring Git Bash is properly detected and used.

For example:
- In native Windows installations, Claude Code relies on Git Bash for Unix-like compatibility to handle scripts and commands.
- If set as the default terminal (e.g., in integrated tools like VS Code or Cursor), it will launch `git-bash.exe` for tasks.
- There are reported bugs and guides for handling path issues or spaces in the Git installation directory that affect this integration.

If you're encountering issues, check your system PATH, ensure Git is installed correctly, and verify the terminal profile in your IDE.

References:
[Claude Code Native Windows Bash output not seen - Reddit](https://www.reddit.com/r/ClaudeAI/comments/1m06s2l/claude_code_native_windows_bash_output_not_seen/)
[BUG Claude Code VS Code Extension Fails to Detect Git Bash on GitHub](https://github.com/anthropics/claude-code/issues/8674)
[Troubleshooting Claude Code Installation on Windows - Medium](https://medium.com/%40tomhag_17/troubleshooting-claude-code-installation-on-windows-from-tty-errors-to-success-1f44af03c9f2)
[Running Claude Code on Windows Without WSL - Blog](https://blog.shukebeta.com/2025/06/25/running-claude-code-on-windows-without-wsl/)
[AI Agent Claude 4 runs commands in PowerShell even when default is Git Bash - Forum](https://forum.cursor.com/t/ai-agent-claude-4-runs-commands-in-powershell-even-when-default-terminal-is-git-bash/137164)
[How To Install Claude Code on Windows Complete Guide 2025 - Itecsonline](https://itecsonline.com/post/how-to-install-claude-code-on-windows)
[BUG Claude Code fails to resolve Git Bash path with space - GitHub](https://github.com/anthropics/claude-code/issues/4507)
[Install Claude Code on Windows Without WSL Step-by-Step Guide - YouTube](https://www.youtube.com/watch?v=LtnxvLZjxAI)
[47 Claude Code WSL Tricks Every Windows User Should Know - Medium](https://medium.com/%40joe.njenga/47-claude-code-wsl-tricks-every-windows-user-should-know-5d42aaee2d93)
[Claude Code Installation Guide for Windows 11 Setting Up with WSL2 - Claude AI](https://claude.ai/public/artifacts/03a4aa0c-67b2-427f-838e-63770900bf1d)
