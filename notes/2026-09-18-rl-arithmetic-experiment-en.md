---
audio: false
generated: true
image: false
lang: en
layout: post
title: RL Arithmetic Experiment
translated: false
type: note
---

## Short answer

`/mnt/data/zz/grpo-rl` is a **from-scratch RL post-training experiment**: can a small *base* (non-instruct) LLM learn to solve arithmetic by **reinforcement learning on a verifiable reward** — the "R1 recipe" — without any supervised fine-tuning warmup? Everything is designed to fit your single 12 GB RTX 4070.

---

## 1. The setup, concretely

| Piece | Value | Where |
| --- | --- | --- |
| Policy | `Qwen/Qwen2.5-1.5B` **base** (deliberately not `-Instruct`) | `run.sh` |
| Compression | 4-bit NF4 QLoRA + LoRA r=16/α=32 on all attn+MLP proj, grad ckpt | `train_grpo.py:load_model_and_tokenizer` |
| Data | 800 synthetic problems (easy `a+b`, medium `a*b+c`, hard `(a+b)*c`), 95/5 split → 760 train / 40 eval | `make_synthetic` |
| Algorithm | TRL `GRPOTrainer`, `loss_type="grpo"`, G=4 generations/prompt, β=0.02 KL to frozen ref, temp 1.0, lr 5e-6 | `GRPOConfig` |
| Step shape | **2 unique prompts × 4 generations = 8 completions per optimizer step** → 760 steps for 2 epochs | verified from the `epoch` field (`2·step/760`) |
| Checkpoints | every 25 steps, `save_total_limit=2` | `grpo_qwen15b_math/` |

Reward is **two functions summed** (`train_grpo.py:reward_format` / `reward_correctness`):

- `reward_format` → ≤ **+0.3** for emitting a well-formed `<think>…</think>` block with ≥20 chars of content
- `reward_correctness` → **+1.0** answer right, **−0.5** wrong, **−0.7** no number at all

## 2. What "RL training" means here (vs. pretraining/SFT)

Everything else in this repo is **imitation**: you have target text and you minimize cross-entropy against it. Here there are **no target reasoning traces at all** — you only have a *checker*. The model samples its own attempts and gets reinforced for attempts that pass the checker. That's the whole point:

```
prompt ──► policy samples 4 completions (G=4)
              │
              ├─ "… 8 * 1 + 1 = 9"          → reward +1.0
              ├─ "… = 11"                    → reward −0.5
              ├─ "<think>8*1=8; +1=9</think>9" → reward +1.3
              └─ "I cannot answer"           → reward −0.7
                    │
        GRPO: advantage = (rᵢ − mean(r_group)) / std(r_group)
                    │
        policy-gradient update on LoRA weights  −  β·KL(policy‖ref)
```

Why **GRPO** specifically: it normalizes rewards *within the group of 4* to get the advantage, so it needs **no value/critic network** — that's the memory saving that makes this fit in 11.6 GB. The KL term (β) is a leash that stops the policy from drifting into gibberish that games the checker. Why a **base** model: an instruct model already has an RLHF prior fighting your reward, so you can't attribute behaviour change to your reward signal.

## 3. What the run is telling us so far

Good news — it's working as an RL pipeline:

- **Held-out reward is rising monotonically**: `eval_reward` 0.642 → 0.649 → 0.712 → 0.747 → 0.823 → **0.888** (at step ~175). That's generalization, not memorization.
- KL stays tiny (0.011–0.05), entropy 0.5–0.7, `clip_ratio` ≈ 0 → stable, gentle updates, no divergence.
- (The negative `eval_loss` you see is normal for GRPO — it's the policy-gradient + KL objective, not a log-likelihood. Don't panic.)

But the **scientific goal of the experiment is not being achieved**, and the logs say so plainly:

**`reward_format/mean` is 0 in 142 of 175 steps** (max observed 0.075, latest eval: **0.003**). The model is almost never emitting `<think>` tags — it just answers the arithmetic directly. The reason is a reward-design loophole:

1. `_extract_answer` falls back to "last number anywhere in the text", so a direct answer gets the full **+1.0** without any reasoning.
2. The format bonus is only +0.2/+0.1 — a small fraction of +1.0, and irrelevant when the answer is already right.
3. These problems are **too easy** for a 1.5B base model: it's near-saturated, so there's no pressure to reason. `frac_reward_zero_std ≈ 0.5` confirms it — in half the groups all 4 samples get the identical reward, so the advantage is 0 and **no gradient flows**.

So what's actually being learned is "answer easy arithmetic directly, more reliably". Chain-of-thought is *not* emerging. That's a clean, honest negative result about the reward design, not a bug.

## 4. Where this sits, and what's next

This repo is a staged ML-infra playground — data/tokenization pipelines (FineWeb, codeparrot, climbmix) → pretraining runs on 4070/H200 → and now `grpo-rl` as the **post-training stage**. This run is the pipeline-proving first rung (the `--smoke` 2-step mode and `setup_env.sh` exist exactly for that).

Natural next moves, in order of value:

1. **`--dataset gsm8k`** — already wired in (`make_gsm8k`, `Makefile`-free, uses your local HF cache). The base model will score far below saturation, CoT becomes *necessary*, and `frac_reward_zero_std` drops.
2. **Close the shortcut**: require the `<think>` block for the correctness reward to pay out (e.g. gate correctness on format, or add a large format term). Right now you're rewarding the answer, not the reasoning.
3. **Re-run with a fresh `--output-dir`** so you have a clean before/after comparison against this near-saturated baseline.
4. Add `--wandb` if you want curves instead of grepping the pane.

Minor cleanup while you're in there: the banner in `train_grpo.py` prints `G / batch : 4 generations x 8 prompts per step`, but the effective shape is **4 generations × 2 prompts** per step (8 completions) — the `epoch` arithmetic proves it. Worth fixing so the logs aren't misread.
