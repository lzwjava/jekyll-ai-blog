---
audio: false
generated: true
image: false
lang: en
layout: post
title: GRPO Negative Result Analysis
translated: false
type: note
---

This is **run 1** of your GRPO experiment — the one that saved to `./grpo_qwen15b_math/final` (checkpoints 750/760, `epoch: 2`, 760 steps). I pulled the full `trainer_state.json` to interpret it. Here's what those numbers actually say.

## What the experiment was

RL, not supervised fine-tuning: take the **base** Qwen2.5-1.5B (no SFT, no instruct tune), generate 4 completions per arithmetic prompt, and reward them with:
- `reward_format` — max +0.3 for a well-formed `<think>…</think>` block
- `reward_correctness` — +1.0 correct / −0.5 wrong / −0.7 no answer

The goal was to get chain-of-thought arithmetic to emerge in a base model. Config: 760 steps, ~1h45m (8.3 s/step), 40 eval prompts, 31 evals.

## Reading the headline numbers

| Metric | Value | Meaning |
|---|---|---|
| `train_loss` | −0.0090 | **Not a cross-entropy loss.** It's the GRPO policy-gradient surrogate; near zero here = advantages are ~zero, i.e. *no signal*, not "converged well." |
| `eval_reward` | 0.9238 | Mean reward over eval groups. But since format = 0, this is *purely* correctness. |
| `eval_rewards/reward_format/mean` | **0.0 (std 0.0)** | 🚩 The behavior you were trying to teach **never happened** — in every one of the 760 training steps and every eval. |
| `eval_frac_reward_zero_std` | **0.85** | 🚩 85% of prompt groups gave all 4 generations the *same* reward → zero advantage → no gradient. Only 15% of groups taught anything. |
| `eval_kl` | 0.030 | The policy barely moved from the reference. beta=0.02 + dead advantages ≈ frozen model. |
| `eval_entropy` | 0.449 (from ~1.0 at step 25) | Exploration collapsed; the policy became deterministic/peaked. |
| `eval_clip_ratio/*` | all 0 | PPO clipping never triggered — a symptom of microscopic updates, not a bug. |
| `eval_completions/*` | mean 48, max 97, clipped 0, terminated = total | Generations are short and all end with EOS; nothing hit the 384 cap. It learned to answer *briefly and directly*. |

Those final generations confirm it: `(7 + 5) * 3 = 36` and `1834 + 596 = 2430` are both correct with step-by-step prose — but **no `<think>` tags**, because it was never taught the protocol.

(Also: `eval_num_tokens: 6.554e5` is cumulative over all 31 evals, not one eval — ≈ tokens/completion × completions × evals. And `eval_samples_per_second 0.64 × 62.5s = 40` confirms the eval set size.)

## What the experiment actually means

**It's a scientifically clean negative result — the pipeline works, the capability did not increase.**

1. **The task had no headroom.** The standard synthetic mix is already ~83% solved by the untouched base model. So within each group of 4 samples, rewards are usually identical → `zero_std` climbs to 0.85 → GRPO has nothing to learn from. It's the classic "reward saturated" failure. Note `reward` rose 0.64 → 0.92 on eval, but with 85% dead groups that rise is mostly the model settling into its existing mode, not learning.

2. **The format reward was unreachable.** A base model assigns essentially zero probability to the exact `<think>…</think>` token pair, so the format term was a constant 0 across every group → zero advantage → no gradient to acquire it. You cannot bootstrap an exact-token protocol from a ±1.0 correctness signal.

3. **The headline "gain" is largely an artifact.** Per your own `run2.sh` diagnosis: under run 1's buggy answer extraction, the base model scored ~82.8%, and most of the move to 92.4% was the policy learning to **stop emitting a stray trailing `</think>`** — a token habit, not arithmetic skill. Fixed extraction shows the base is already ~100% greedy on this distribution.

4. **What it really learned:** answer shorter (length dropped, entropy collapsed), answer without reasoning, and drop the stray tag. That's it.

## Bottom line

`reward ↑` ≠ `capability ↑`. This run demonstrates the two structural prerequisites GRPO needs, both of which were missing:
- **Mixed-outcome groups** (headroom) — fixed in `run2.sh` with `--difficulty harder` (3-digit add/sub, 2-digit products).
- **A reachable target behavior** — fixed with `--format-warmup 512`, which supervises the tag protocol to ~0.30 format reward *before* RL starts.

Use `headroom.py` to verify a category sits in roughly the **20–70%** base accuracy band before training. And ignore near-zero `eval_loss` as a quality signal — with `frac_reward_zero_std = 0.85`, it's the sound of nothing happening.