---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 升级Claude代码至最新版本
translated: true
type: note
---

要将 Claude Code 从 v2.0.0 升级到最新版本，请根据您的安装类型选择以下方法之一（所有版本默认支持自动更新，这些更新将在下次启动工具时应用；您可以通过设置 `DISABLE_AUTOUPDATER=1` 来禁用自动更新）：

### 通过 Claude Code 内置命令
在终端中运行手动更新命令：
```
claude update
```
这将自动应用最新版本。[1][2]

### 通过 npm（如果已全局安装）
如果最初是通过 npm 安装的，请使用以下命令更新：
```
npm update -g @anthropic-ai/claude-code
```
或者强制安装最新版本：
```
npm install -g @anthropic-ai/claude-code@latest
```
[3][4]

### 通过原生二进制文件（Beta 安装程序）
对于原生安装，重新运行安装程序脚本以获取最新版本：
```
# macOS/Linux/WSL
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Windows PowerShell
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest
```
[1]

**验证：** 升级后，使用 `claude --version` 检查您的版本，确认已更新（例如，更新到当前稳定版本）。如果遇到问题，请确保 npm 是最新的（`npm install -g npm@latest`）。设置和配置在更新过程中会保留。[1][3][4]

引用：
[1] https://docs.claude.com/en/docs/claude-code/setup
[2] https://www.reddit.com/r/ClaudeAI/comments/1lvbijz/claude_code_updates_from_version_1045_to_1044/
[3] https://www.reddit.com/r/ClaudeAI/comments/1l8gbfo/dont_forget_to_update_your_claude_cli_it_makes_a/
[4] https://www.claudelog.com/faq/
