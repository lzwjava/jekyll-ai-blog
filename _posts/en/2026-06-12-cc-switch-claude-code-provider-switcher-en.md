---
audio: false
generated: true
image: false
lang: en
layout: post
title: cc-switch Claude Code Provider Switcher
translated: false
type: note
---

**Question:** What is cc-switch in the Claude Code ecosystem?

**Answer:**

cc-switch is a third-party, open-source provider/config switcher for Claude Code (and other AI CLIs) — not an Anthropic product or a built-in Claude Code command. It's a cross-platform desktop assistant for Claude Code, Codex, OpenCode, OpenClaw, Gemini CLI & Hermes Agent, built by farion1231.

**The problem it solves:** Claude Code reads its backend config (base URL, API key, model) from `~/.claude/settings.json` / env vars like `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN`. If you bounce between Anthropic official, DeepSeek, OpenRouter, GLM, Kimi, etc., you're hand-editing JSON or juggling shell exports. cc-switch turns that env-var dance into one-click switching — it manages multiple provider profiles, persists them to ~/.claude/settings.json, and lets you switch backends without touching shell config.

**Key features:**

v3.16.1 manages 7 AI CLIs via a system tray app, ships with ~50 third-party provider presets (DeepSeek, Zhipu GLM, MiniMax, Kimi, Qwen/Bailian, AWS Bedrock, NVIDIA NIM, OpenRouter, plus relay services) — most presets just need an API key since endpoint URL and protocol are pre-filled. It also handles MCP servers, skills, prompts, local proxy routes, usage statistics, and supports WebDAV sync across devices. In proxy mode, requests flow Claude Code → localhost:8080 → CC-Switch Proxy → upstream API, and a "Claude Rectifier" feature (v3.10.0+) fixes compatibility issues with third-party APIs.

**For your workflow specifically:** since you're heavy on deepseek-v4 and MiMo via OpenRouter-style providers, this is directly relevant. Two paths:

1. GUI: `farion1231/cc-switch` desktop app (Tauri-based, runs fine on your M2 Air)
2. Terminal-first (more your style): `SaladDay/cc-switch-cli` — a TUI + CLI fork, interactive TUI for daily switching, plain CLI for scripts and repeatable workflows

The underlying mechanic is trivial though — you could replicate the core in a 20-line shell function if you don't want another tool:

```bash
# ~/.zshrc — poor man's cc-switch
ccs() {
  case "$1" in
    deepseek)
      export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
      export ANTHROPIC_AUTH_TOKEN="<API_KEY>"
      export ANTHROPIC_MODEL="deepseek-chat" ;;
    official)
      unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_MODEL ;;
  esac
  claude
}
```

What cc-switch adds over this: profile persistence in `settings.json` (so non-shell launches work), the local proxy with protocol adaptation (OpenAI-style responses → Anthropic Messages format), config backup before each write, and multi-CLI management. Run `/status` inside Claude Code after switching to verify the active base URL and model.

One caveat: the project is heavily sponsored by API relay/reseller services (visible all over the README), which is worth knowing when evaluating preset endpoints — vet any relay before routing keys through it.

**References:**

- [farion1231/cc-switch (GitHub)](https://github.com/farion1231/cc-switch)
- [SaladDay/cc-switch-cli (GitHub)](https://github.com/saladday/cc-switch-cli)
- [CC-Switch beginner guide (apiyi)](https://help.apiyi.com/en/cc-switch-beginner-guide-en.html)
- [Claude Code backend switching guide (ofox)](https://ofox.ai/blog/claude-code-switch-tutorial-2026/)
