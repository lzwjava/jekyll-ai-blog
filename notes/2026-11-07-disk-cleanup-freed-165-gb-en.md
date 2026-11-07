---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disk cleanup freed 16.5 GB
translated: false
type: note
---

Done. Summary:

**Removed (disk + `repos.json` + `NAME_TO_REPO` mapping):**

| Repo | Was |
|---|---|
| Qwen2.5-Coder | 3.4 GB |
| TensorRT-LLM | 2.9 GB |
| openai-cookbook | 1.8 GB |
| evals | 1.6 GB |
| greptimedb | 1.4 GB |
| litellm | 1.2 GB |
| bun | 1.2 GB |
| claw-code | 1.2 GB |
| weaviate | 1.1 GB |
| nanochat | 1.0 GB |

**~16.5 GB freed** — 217 MB → **22 GB free** on the disk.

**Verified:**
- `repos.json` valid, now 157 repos; none of the 10 remain
- `projects_init.py` compiles, all 10 mapping entries removed
- `ww projects update --list` works → 157 repos
- `ww projects update` still safe (missing dirs are skipped)

Want me to commit this? (Reminder: use `SKIP=bandit git commit` per AGENTS.md since the bandit hook is misconfigured.)
