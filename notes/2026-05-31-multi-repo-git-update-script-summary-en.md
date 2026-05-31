---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Repo Git Update Script Summary
translated: false
type: note
---

The command works — llama.cpp is just a large repo that takes a while to pull. Here's the summary:

```
Done! Here's what was built:

FILES MODIFIED:
  ~/projects/ww/ww/git/git_update.py   — rewritten with config-based repo list
  ~/projects/ww/ww/projects/repos.json — 60 repos in 8 categories (new file)
  ~/projects/ww/main.py                — updated help text
  ~/.zsh/completions/_ww               — updated completion text

COMMANDS:
  ww projects update              # pull all 60 repos (default)
  ww projects update --list       # show repos by category
  ww projects update @ai-agents   # pull only a category
  ww projects update llama.cpp    # pull a single repo
  ww projects update @ai-models pytorch  # mix categories + names

CATEGORIES (60 repos total):
  ai-models      (13) — DeepSeek, Qwen, GPT-2, CLIP, Whisper, llama3, Kimi...
  ai-training    (14) — pytorch, Megatron-LM, nanoGPT, llm.c, bitsandbytes...
  ai-inference    (5) — llama.cpp, sglang, ktransformers, dinov2, nougat
  ai-apps         (7) — open-webui, dify, ComfyUI, stable-diffusion-webui...
  ai-agents       (4) — hermes-agent, codex, claw-code, gpt-researcher
  dev-tools       (8) — git, rust, jdk, react, vscode, terminal, alacritty, uv
  infra-network   (5) — openwrt, searxng, shadowsocks-rust, greptimedb, netty
  web-platforms   (4) — jekyll, kramdown, huggingface_hub, Telegram-iOS

CRON JOB:
  weekly-repo-update — runs every Sunday 9:00 AM (job: d3991577b9ca)
  Next run: 2026-06-07

To edit repos:  vim ~/projects/ww/ww/projects/repos.json
To add repos:   just add the dir name under any category
```

References:
- [git_update.py](/Users/lzwjava/projects/ww/ww/git/git_update.py)
- [repos.json](/Users/lzwjava/projects/ww/ww/projects/repos.json)