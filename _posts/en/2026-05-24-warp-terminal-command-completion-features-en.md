---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp Terminal Command Completion Features
translated: false
type: note
---

Yeah, Warp's command completion is genuinely solid. A few things that stand out:

1. **Fish-style autosuggestions** — It shows ghost text completions as you type, pulling from your history and known commands. Very snappy.

2. **Tab completions with descriptions** — It doesn't just list completions, it adds context (like what a flag does), similar to `fish` shell but with a richer UI.

3. **AI command search** — You can hit `Ctrl+K` or `Cmd+K` and describe what you want in natural language, and it suggests the actual command. This is the "AI-native" part that sets it apart.

4. **Warp Drive** — Shared team workflows and saved commands, though that's more of a team feature.

Compared to other terminals:
- **iTerm2/Alacritty** — basically zero built-in completion, relies entirely on your shell (zsh/fish)
- **Fig** (now Amazon Q) — Was doing similar completion overlays but got acquired
- **Warp** — Built it into the terminal itself, so it works regardless of shell config

The tradeoff is that Warp is Electron-based (actually Rust + Electron), so it's heavier than Alacritty or Kitty. And it requires a login/account, which rubs some people the wrong way.

Are you currently using Warp, or evaluating it for your workflow? I see you have a `warp` project directory — is that related to Warp terminal or something else?