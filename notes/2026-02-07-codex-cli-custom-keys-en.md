---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Configuring Codex CLI With Custom Keys
translated: false
type: note
---

**Question:** How to use my own key with Codex CLI and how to use the OpenRouter API with it?

**Answer:**

**Codex CLI** is OpenAI's open-source terminal-based coding agent (released around 2025). It acts like an interactive AI that can read your codebase, suggest/edit files, run commands, and iterate on tasks — all from your terminal.

It supports multiple providers (including OpenAI and third-parties like OpenRouter) via configuration.

### 1. Installation (macOS/Linux recommended; Windows experimental)

```bash
# Requires Node.js ≥ 18
npm install -g @openai/codex
```

Alternative install methods (Rust binary, brew, etc.) → check official docs.

### 2. Using your own OpenAI key (official / default way)

**Option A – Easiest (interactive login)**

Run once:

```bash
codex
```

→ Browser opens → sign in with ChatGPT account (Plus/Pro/... includes access)
or choose "Use API key" and paste your OpenAI API key from https://platform.openai.com/api-keys

**Option B – Headless / script-friendly (env variable)**

```bash
export OPENAI_API_KEY="sk-..."
codex
```

It caches the token after first use.

### 3. Using OpenRouter API (third-party models, often cheaper / more options)

Codex CLI supports custom providers via `~/.codex/config.toml` (created automatically after first run).

**Recommended config for OpenRouter (2026 working setup):**

Edit (or create) the file:

```toml
# ~/.codex/config.toml

model = "anthropic/claude-4-sonnet"          # or deepseek/deepseek-r1, qwen/qwen2.5-coder-32b, google/gemini-2.5-pro, etc.
model_provider = "openrouter"                # ← important: must match the section name below

[model_providers.openrouter]
name = "OpenRouter"
base_url = "https://openrouter.ai/api/v1"
env_key = "OPENROUTER_API_KEY"               # ← reads from this env var
# Optional extra headers (sometimes needed)
# headers = { "HTTP-Referer" = "https://your-site.com", "X-Title" = "Codex CLI" }
```

Then set your key:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
codex
```

Or make it permanent (zsh/bash):

```bash
echo 'export OPENROUTER_API_KEY="sk-or-v1-..."' >> ~/.zshrc
source ~/.zshrc
```

**Quick test command (non-interactive):**

```bash
codex "Explain the architecture of this project"
```

or start interactive session and just type natural language requests.

### 4. Popular models to try via OpenRouter in Codex CLI (Feb 2026)

- `deepseek/deepseek-r1` or `deepseek/deepseek-v3-0324` — best price/performance coding
- `anthropic/claude-4-sonnet` or `claude-3.7-sonnet` — highest quality
- `qwen/qwen2.5-coder-32b-instruct` — very strong & cheap
- `google/gemini-2.5-pro` — huge context, multimodal
- `openai/o3-mini` or `openai/o1` — strong reasoning

Just change the `model = "..."` line and restart `codex`.

### 5. Useful flags / modes

```bash
codex --suggest                # only propose changes, never apply automatically
codex --approval-policy never  # auto-apply (careful!)
codex --sandbox-mode workspace-write  # safer file writing
codex "fix bug in login flow"  # one-shot
```

**Tip:** Many users report better reliability + lower cost with OpenRouter + strong open models vs default OpenAI in Codex CLI.

If you run into "model_not_found" → double-check `model_provider` matches the `[model_providers.xxx]` section name exactly.

**References:**

- [https://developers.openai.com/codex/cli](https://developers.openai.com/codex/cli)
- [https://github.com/openai/codex](https://github.com/openai/codex)
- [https://openrouter.ai/docs](https://openrouter.ai/docs)
- [https://openrouter.ai/models](https://openrouter.ai/models)
