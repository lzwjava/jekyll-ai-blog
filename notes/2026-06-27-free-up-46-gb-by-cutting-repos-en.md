---
audio: false
generated: true
image: false
lang: en
layout: post
title: Free up 46 GB by cutting repos
translated: false
type: note
---

Here's the picture:

```
~/projects total:     144 GB
repos.json repos:      50 GB  (170 repos)
Non-repos.json repos:  22 GB
lzwjava.github.io:     72 GB  (blog + notes, not in repos.json)
```

Your disk has 116 MB free. You need to act now.

Here's my recommendation for cutting ~56 repos (~1/3 of 170) from repos.json. Grouped by category:

**OS KERNELS — drop from repos.json, delete locally (saves 12.0 GB)**
These are reference-only, you can always re-clone or browse on GitHub:
- `linux` (7.4 GB)
- `freebsd-src` (2.2 GB)
- `wireguard-linux` (2.0 GB)
- `xnu` (183 MB)

**LARGE TOOLCHAIN SOURCES — drop, re-clone on demand (saves 6.4 GB)**
You rarely need these checked out locally:
- `jdk` (2.4 GB) — OpenJDK source
- `vscode` (1.8 GB) — VS Code source
- `rust` (1.4 GB) — Rust compiler source
- `OpenROAD` (2.4 GB) — EDA tools
- `rocBLAS` (957 MB) — AMD GPU library source

**HUGE AI REPOS w/ model weights or data checked in (saves 13.3 GB):**
- `Qwen2.5-Coder` (3.5 GB) — likely has weights in repo
- `openai-cookbook` (1.7 GB) — notebooks + data files
- `evals` (1.6 GB) — OpenAI evals with test data
- `litellm` (1.3 GB) — unusually large for a Python lib
- `claw-code` (1.2 GB)
- `weaviate` (1.1 GB)
- `TensorRT-LLM` (978 MB) — NVIDIA SDK, rarely need full checkout
- `mlflow` (693 MB)

**AI APPS you're not actively using (saves 3.4 GB):**
- `llama_index` (814 MB)
- `LibreChat` (519 MB)
- `open-webui` (495 MB)
- `crewAI` (579 MB)
- `AutoGPT` (258 MB)
- `voice-changer` (244 MB)
- `nexa-sdk` (229 MB)
- `h2ogpt` (108 MB)
- `quivr` (130 MB)
- `llm-app` (88 MB)
- `localGPT` (7 MB)
- `anything-llm` (37 MB)

**AI INFERENCE — overlap/duplicate tools (saves 1.2 GB):**
You have llama.cpp, ollama, vllm, sglang, text-generation-webui, llamafile, ktransformers, TensorRT-LLM, ggml, mlx, mlx-examples. Keep 3-4 max:
- Drop: `ggml` (64 MB), `mlx-examples` (108 MB), `text-generation-webui` (56 MB), `ktransformers` (167 MB), `nexa-sdk` (229 MB), `nougat` (8 MB), `dinov2` (8 MB)

**PLATFORMS / INFRA not actively used (saves 1.1 GB):**
- `greptimedb` (571 MB)
- `Telegram-iOS` (595 MB)

**DEV TOOLS — OS/deviation projects you don't need in repos.json (saves 4.6 GB):**
- `bun` (581 MB)
- `warp` (821 MB)
- `fineract` (234 MB)
- `netty` (163 MB)
- `dubbo` (101 MB)
- `desktop` (155 MB) — GitHub Desktop
- `miu2d` (143 MB)
- `verilator` (111 MB)
- `tiny-gpu` (42 MB)
- `vortex` (310 MB)
- `ramulator2` (4 MB)
- `openlane2` (23 MB)
- `ChezScheme` (43 MB)
- `terminal` (118 MB) — Windows Terminal

**TOTAL: ~55 repos removed, freeing ~46 GB**

That would bring repos.json from 170 → ~115 repos and free enough to breathe. Also consider:

1. **lzwjava.github.io at 72 GB is your single biggest item** — it probably has large binary assets. Run `du -sh ~/projects/lzwjava.github.io/.git` to see if it's the git history. If so, a `git clone --depth 1` re-clone could save 50+ GB alone.

2. The **non-repos.json repos** (22 GB) include things like `gcc` (1.5 GB), `open-liberty` (1.2 GB), `true-question` (1.4 GB), `WeFriends` (844 MB) — many look like old projects you could delete too.

Want me to generate the trimmed repos.json and a `rm -rf` command for the ones to delete?
