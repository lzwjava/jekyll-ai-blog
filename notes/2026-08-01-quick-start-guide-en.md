---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quick Start Guide
translated: false
type: note
---

You're all set — `tb` v0.2.18 is installed (matching this repo), Docker is running, and you have `DEEPSEEK_API_KEY` / `OPENROUTER_API_KEY` in your environment. Here's how to run the benchmark with this repo.

## Important detail: tasks location

This repo's latest commit renamed `tasks/` → `original-tasks/` (see commit `2af0e44`), but the CLI still defaults `--dataset-path` to `tasks`. So you **must** always pass `--dataset-path` explicitly:

```bash
cd /mnt/data/terminal-bench

# 1) Smoke test with ONE task first (recommended)
tb run \
  --dataset-path original-tasks \
  --agent terminus \
  --model deepseek/deepseek-chat \
  -t "3d-model-format-legacy" \
  --n-concurrent 1

# 2) Run multiple tasks by ID or glob
tb run \
  --dataset-path original-tasks \
  --agent terminus \
  --model deepseek/deepseek-chat \
  -t "3d-*" \
  --n-concurrent 4

# 3) Run ALL 241 tasks in this repo
tb run \
  --dataset-path original-tasks \
  --agent terminus \
  --model deepseek/deepseek-chat \
  --n-concurrent 4
```

## Key flags explained

| Flag | What it does |
|---|---|
| `--dataset-path` | Point at this repo's tasks (`original-tasks`) — required here |
| `--agent` | `terminus` (built-in agent), `naive`, `oracle`, `claude-code`, `aider`, `codex`, etc. |
| `--model` | LiteLLM naming: `deepseek/deepseek-chat`, `deepseek/deepseek-reasoner`, `openrouter/anthropic/claude-sonnet-4-...`, `openai/gpt-4o`, ... |
| `-t / --task-id` | Specific task ID or glob pattern; repeatable; omit to run all |
| `-e / --exclude-task-id` | Exclude tasks |
| `--n-concurrent` | Parallel trials (default 4) |
| `--n-attempts` | Attempts per task (default 1) |
| `--no-rebuild` | Skip rebuilding Docker images on re-runs (faster) |
| `--run-id` | Custom run name (default: timestamp) |
| `--output-path` | Results dir (default: `runs/`) |

## No-LLM sanity check (optional)

Want to verify the harness works without spending tokens? Use the **oracle** agent, which just runs the reference solution — no model/API key needed:

```bash
tb run --dataset-path original-tasks --agent oracle -t "3d-model-format-legacy"
```

## Viewing results

```bash
tb runs list               # all runs in ./runs
tb runs summarize <run-id> # pass/fail summary + scores
tb runs status <run-id>    # progress (completed / not-started)
```

Results land in `runs/<run-id>/` (JSON per trial, logs, etc.).

## Tips

- Start with 1 task + `--n-concurrent 1` to confirm the Docker image builds and the model call works before launching a full run.
- Each task builds its own Docker image on first run — a full 241-task run takes a while and lots of disk; use `--n-concurrent` to balance speed vs. rate limits.
- To download a published dataset instead of using the local folder (e.g., leaderboard set `terminal-bench-core==0.1.1`), use `--dataset terminal-bench-core==0.1.1` and `tb datasets list` to see what's available.

Want me to kick off a single-task test run now to verify the whole pipeline works?