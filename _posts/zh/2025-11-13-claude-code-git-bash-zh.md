---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Claude代码在Windows上使用Git Bash
translated: true
type: note
---

是的，根据最新动态，Claude Code（Anthropic推出的AI编程工具）在Windows系统上确实会触发`git-bash.exe`来执行shell命令。该工具通常使用Git Bash作为命令执行环境，特别是在未配置WSL的原生Windows系统中。这可能导致命令执行时弹出终端窗口，目前已有相关配置方案、扩展插件（如VS Code中的扩展）和故障排查步骤，用于确保Git Bash能被正确检测和使用。

具体表现为：

- 在原生Windows安装环境中，Claude Code依赖Git Bash提供类Unix兼容性来处理脚本和命令
- 若被设为默认终端（例如在VS Code、Cursor等集成开发工具中），执行任务时会启动`git-bash.exe`
- 现有已知故障报告和解决指南涉及Git安装路径中的空格字符或路径识别问题

若遇到相关问题，建议依次检查：

1. 系统PATH环境变量配置
2. Git是否正确安装
3. 集成开发环境中的终端配置文件

参考链接：
[Claude Code原生Windows环境Bash输出不可见 - Reddit](https://www.reddit.com/r/ClaudeAI/comments/1m06s2l/claude_code_native_windows_bash_output_not_seen/)
[BUG Claude Code的VS Code扩展无法检测Git Bash - GitHub](https://github.com/anthropics/claude-code/issues/8674)
[Windows系统Claude Code安装故障排查 - Medium](https://medium.com/%40tomhag_17/troubleshooting-claude-code-installation-on-windows-from-tty-errors-to-success-1f44af03c9f2)
[无需WSL在Windows运行Claude Code - 博客](https://blog.shukebeta.com/2025/06/25/running-claude-code-on-windows-without-wsl/)
[AI代理Claude 4在默认终端为Git Bash时仍使用PowerShell执行命令 - 论坛](https://forum.cursor.com/t/ai-agent-claude-4-runs-commands-in-powershell-even-when-default-terminal-is-git-bash/137164)
[2025年Windows完整安装Claude Code指南 - Itecsonline](https://itecsonline.com/post/how-to-install-claude-code-on-windows)
[BUG Claude Code无法解析含空格的Git Bash路径 - GitHub](https://github.com/anthropics/claude-code/issues/4507)
[无需WSL在Windows安装Claude Code分步指南 - YouTube](https://www.youtube.com/watch?v=LtnxvLZjxAI)
[Windows用户必知的47个Claude Code WSL技巧 - Medium](https://medium.com/%40joe.njenga/47-claude-code-wsl-tricks-every-windows-user-should-know-5d42aaee2d93)
[Windows 11系统安装Claude Code指南：基于WSL2环境配置 - Claude AI](https://claude.ai/public/artifacts/03a4aa0c-67b2-427f-838e-63770900bf1d)
