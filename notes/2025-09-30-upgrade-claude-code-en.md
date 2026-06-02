---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Upgrading Claude Code to Latest Version
translated: false
type: note
---

To upgrade Claude Code from v2.0.0 to the latest version, use one of the following methods based on your installation type (all versions support auto-updates by default, which apply the next time you start the tool; you can disable them by setting `DISABLE_AUTOUPDATER=1`):

### Via Claude Code's Built-In Command
Run the manual update command in your terminal:
```
claude update
```
This applies the latest version automatically. [1][2]

### Via npm (If Installed Globally)
If you originally installed via npm, update with:
```
npm update -g @anthropic-ai/claude-code
```
Or force-install the latest:
```
npm install -g @anthropic-ai/claude-code@latest
```
[3][4]

### Via Native Binary (Beta Installer)
For native installations, re-run the installer script for the latest version:
```
# macOS/Linux/WSL
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Windows PowerShell
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest
```
[1]

**Verification:** After upgrading, check your version with `claude --version` to confirm it's updated (e.g., to the current stable release). If you encounter issues, ensure npm is up to date (`npm install -g npm@latest`). Settings and configurations are preserved across updates. [1][3][4]

Citations:
[1] https://docs.claude.com/en/docs/claude-code/setup
[2] https://www.reddit.com/r/ClaudeAI/comments/1lvbijz/claude_code_updates_from_version_1045_to_1044/
[3] https://www.reddit.com/r/ClaudeAI/comments/1l8gbfo/dont_forget_to_update_your_claude_cli_it_makes_a/
[4] https://www.claudelog.com/faq/
