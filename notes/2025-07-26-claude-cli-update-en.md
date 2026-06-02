---
audio: false
generated: true
lang: en
layout: post
title: Updating Claude Code CLI
translated: false
type: note
---

Hi! It looks like you're dealing with the Claude Code CLI tool from Anthropic. Based on the output you pasted, it seems like it already attempted an auto-update to version 1.0.61, but if that's not working or you need to manually update, here's how:

To update the Claude Code CLI:
- Open your terminal.
- Run the command: `claude update`
This built-in command should fetch and install the latest version.

If the update fails (e.g., due to permissions or network issues), you can try reinstalling it via npm (assuming you have Node.js and npm installed):
- Run: `npm install -g @anthropic-ai/claude-code`

After updating, you might need to log in again by running `claude /login` (or sometimes `claude login`, depending on the version). If you're still seeing errors, check your internet connection, ensure your API key is valid, or refer to the official troubleshooting docs.

For more details on commands, you can run `claude --help` as you did, which should show options in the updated version.

[CLI reference - Anthropic API](https://docs.anthropic.com/en/docs/claude-code/cli-reference)
[How to Set Up and Use the Claude CLI Tool Like a Pro](https://medium.com/@riccardo.bernardi.advisor/unlocking-claude-pros-power-how-to-set-up-and-use-the-claude-cli-tool-like-a-pro-against-github-d29f8f682a03)
[GitHub - anthropics/claude-code](https://github.com/anthropics/claude-code)
[Claude Code overview - Anthropic API](https://docs.anthropic.com/en/docs/claude-code/overview)
