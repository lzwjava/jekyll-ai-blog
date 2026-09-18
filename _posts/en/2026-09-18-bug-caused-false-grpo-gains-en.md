---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bug Caused False GRPO Gains
translated: false
type: note
---

Saved and verified. Here's the state of things — and the earlier contradiction resolved into the actual headline finding.

## Saved

| File | What it is |
| --- | --- |
| `/mnt/data/zz/eval_grpo_adapter.py` | Unified base-vs-adapter eval. `--mode indist/ood`, `--greedy`, `--show-samples`, `--save-json`. Replaces the two throwaway scripts. |
| `/mnt/data/zz/grpo-rl/headroom.py` | Per-category base accuracy, with a `saturated / little headroom / GOOD / too hard` verdict per category. |
| `/mnt/data/zz/grpo-rl/run2.sh` | Run-2 config: `--difficulty harder`, `--format-warmup 512`, 1 epoch. |
| `/mnt/data/zz/grpo-rl/train_grpo.py` | +`--difficulty`, `+--format-warmup`, `+--warmup-lr`, best-checkpoint tracking, and the extraction fix. |

All syntax-checked and exercised on GPU. `--format-warmup` verified: format reward **0.00 → 0.30** (max) in 8 steps, peak 2.12 GB. `run2.sh` is wired but **not launched**.

## The contradiction resolved into the real finding

My 79% "harder" check used `headroom.py`'s extraction; the 83% figure came from `eval_grpo_adapter.py`, which still had run 1's **buggy** rule. Same 64 greedy prompts, base model, both rules:

```
OLD rule (what run 1 trained on):  53/64 = 82.8%
NEW rule (fixed):                  64/64 = 100.0%
stray </think> with no number after it: 11/64
answers rescued by the fix:            11
```

**Run 1's entire measured gain was the bug.** 82.8% → 100% is exactly the 11 stray-tag completions, and the base model is already at 100% on the training distribution. GRPO taught it to stop emitting a stray `</think>` — a token habit created by the reward function — and nothing about arithmetic. My earlier "it specifically stopped botching `(a+b)*c`" was wrong; those were the same 11 artifacts.

Worse, `rewards/reward_format/mean` was 0.0 the whole run, so it never even learned the intended format. It just stopped closing a tag it never opened.

## `headroom.py` results — everything is saturated

```
=== Qwen/Qwen2.5-1.5B - greedy, 10 problems/category ===
add2      10/10  100%    add3   10/10  100%    sub3  10/10  100%
mul1      10/10  100%    mul2    9/10   90%    twoterm 10/10 100%
threeterm 10/10  100%
Best training tiers: NONE - everything is saturated or too hard
```

So the base model already handles 2-digit products and 3-term expressions. **Greedy saturation does not by itself prove there's no gradient** — GRPO samples at T=1.0, and what matters is whether the G=4 samples of one prompt get *different* rewards. My probe was the wrong instrument for that. But it does mean `run2.sh`'s "harder" tier buys much less than I claimed in its comments, and `eval_grpo_adapter.py` can no longer show improvement on synthetic arithmetic under greedy decoding.

## What I'd do before launching run 2

Two cheap measurements decide it:

1. `headroom.py --gsm8k 24` — word problems are the one place a 1.5B base is likely genuinely weak, and they make `<think>` actually meaningful.
2. A T=1.0 group-variance probe: for `standard` vs `harder` vs GSM8K, sample G=4 per prompt and report mean reward and `frac_reward_zero_std` — the number that was 82% by the end of run 1. That is the real go/no-go for whether there's gradient to be had.

Want me to run those two? And note the T=1.0 probe is ~5–10 min of GPU, so tell me if you'd rather I keep probes short.
