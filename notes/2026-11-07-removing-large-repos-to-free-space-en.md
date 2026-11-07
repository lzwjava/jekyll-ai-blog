---
audio: false
generated: true
image: false
lang: en
layout: post
title: Removing Large Repos to Free Space
translated: false
type: note
---

Everything is clear now. Summary of the situation:

- **Disk is 100% full** — only **217 MB free** of 460 GB
- `~/projects` holds **75 GB** across 166 of the 167 configured repos
- Deleting dirs is safe for `ww projects update` (missing dirs are skipped), but `ww projects init` would re-clone from `repos.json` — so I should also remove the entries from the config to free space permanently.

Here are the biggest offenders (sorted, all > 700 MB):

| Repo | Size |
| --- | --- |
| Qwen2.5-Coder | 3.5 GB |
| TensorRT-LLM | 3.0 GB |
| openai-cookbook | 1.8 GB |
| evals | 1.6 GB |
| greptimedb | 1.5 GB |
| litellm | 1.2 GB |
| bun | 1.2 GB |
| claw-code | 1.2 GB |
| weaviate | 1.2 GB |
| nanochat | 1.0 GB |
| llama_index | 911 MB |
| llama.cpp | 872 MB |
| Telegram-iOS | 833 MB |
| crewAI | 826 MB |
| pytorch | 823 MB |
| AutoGPT | 797 MB |
| warp | 752 MB |
| LibreChat | 747 MB |
| mlflow | 740 MB |
| vortex | 670 MB |
| hermes-agent | 664 MB |
| open-webui | 577 MB |

My plan: delete these **top ~22 repos (>500 MB) from disk + remove them from `repos.json`** — frees ~27 GB. Note this includes heavy users like `pytorch` and `llama.cpp`; say if you want them kept.

Confirm which to remove? Reply:

- **`yes`** → remove all repos above (>500 MB, frees ~27 GB)
- **`top10`** → only the 10 largest (frees ~16.5 GB)
- or tell me names to keep/exclude
