---
audio: false
generated: true
image: false
lang: en
layout: post
title: Terminal-Bench 2.1 Overview and Leaderboard
translated: false
type: note
---

Question: What is Terminal-Bench 2.1, and what's the current model leaderboard?

Answer:

**What it is:** Terminal-Bench 2.1 is a revision of 2.0 — it evaluates agent-model systems on 89 technical tasks completed through a command-line interface, covering software engineering, ML, security, data processing, scientific computing, and system administration. It's not a new task set, just a fix: 28 of the 89 tasks had issues (broken external deps, too-tight resource budgets, instructions that didn't match tests), and after the fixes no task is unsolved.

Harness/methodology: all models are benchmarked using the Terminus 2 harness, results are pass@1, and a model must pass all pytests on a task to get any credit.

**Leaderboard (July 2026):**

| Model | Score |
|---|---|
| GPT-5.6 Sol (OpenAI) | 0.888 |
| Kimi K3 (Moonshot, top open-source) | 0.883 |
| GLM-5.2 (Zhipu, cheapest in top-10%) | 0.827 |

LLM Stats tracks 15 models on this benchmark, with average score 0.8 and leader at 0.888 (GPT-5.6 Sol). 0 verified results, 15 self-reported.

The biggest mover from 2.0→2.1: Claude Code with Opus 4.6 improved by 12.1 percentage points — makes sense given the task fixes disproportionately unblocked previously-unsolvable env issues.

Note: this is all self-reported by labs, not independently verified — worth checking Artificial Analysis if you want a third-party cross-check before trusting a specific number for a model you care about.

**If you want to run it yourself:**
```bash
git clone https://github.com/harbor-framework/terminal-bench
cd terminal-bench
# harbor is the new framework for 2.x
# --dataset-name terminal-bench-2.1 in the harness config
```

References:
- [Terminal-Bench 2.1 — Snorkel AI](https://snorkel.ai/leaderboard/terminal-bench-2-1/)
- [Terminal-Bench 2.1 Leaderboard — LLM Stats](https://llm-stats.com/benchmarks/terminal-bench-2.1)
- [Terminal-Bench v2.1 — Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-v2-1)
- [harbor-framework/terminal-bench — GitHub](https://github.com/harbor-framework/terminal-bench)
- [Terminal-Bench 2.1 — vals.ai](https://www.vals.ai/benchmarks/terminal-bench-2-1)