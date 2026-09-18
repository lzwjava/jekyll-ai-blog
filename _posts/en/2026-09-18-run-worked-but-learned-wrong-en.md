---
audio: false
generated: true
image: false
lang: en
layout: post
title: Run worked but learned wrong
translated: false
type: note
---

## tl;dr — the run finished and it worked, but it learned the wrong thing

No tmux session named `a` (you have `0` and `2`, both showing this run). Job ended at **20:11**, `Done - LoRA adapter saved to ./grpo_qwen15b_math/final`.

### Run facts

| | |
|---|---|
| Config | `Qwen2.5-1.5B` (base) + 4-bit QLoRA, GRPO, synthetic arithmetic, 2 epochs |
| Wall time | 760 steps / **1:44:50** (~8.3 s/step), clean exit, no OOM |
| Train reward | 0.44 → **1.0**; train_loss `-0.009` |
| Eval reward | 0.62 @step 25 → **0.9238** final, peak **0.965** @step 725 |
| KL / entropy | KL stayed ≤0.03 (beta leash fine), entropy 0.74 → ~0.45 |

### Does the adapter actually do anything? Yes — I checked it independently
Fresh in-distribution prompts, greedy, n=64:
```
BASE : 53/64 = 82.8%
TUNED: 64/64 = 100.0%    fixed=11  broken=0  net=+11
```
All 11 fixes are the `(a+b)*c` "hard" tier — it specifically stopped botching the parenthesized multiply. So the adapter is real and correct.

### Two things are wrong though

**1. The chain-of-thought objective completely failed.** `rewards/reward_format/mean` is **0.0 for all 760 steps**, and 0/64 final generations contain `<think>...</think>`. Mean completion length barely moved (18 words → 18 words). The model didn't learn to reason in tags, it just got more accurate while answering directly. The +0.2/+0.3 tag shaping reward is an unreachable rare event for a base model at temp 1.0, and ±1.0 correctness drowns it out. Fix: SFT warmup on ~200 format examples, or force the opening tag (prepend `<think>` to the prompt/prefix) so the tag is free and only the closing tag + content must be learned.

**2. It saturated in the first ~380 steps; epoch 2 was mostly wasted.** Fraction of groups with zero reward variance (→ zero advantage → zero gradient):
```
steps   1- 76: 30%      steps 381-456: 82%
steps  77-152: 47%      steps 457-608: ~82%
steps 153-228: 64%      steps 685-760: 82%  (0.01 grad_norm)
```
By the end ~82% of groups are all-1.0, so almost no learning signal. The dataset is too easy (base already 83%), so the ceiling was hit almost immediately.

Also: **no OOD gain** — on harder held-out problems (3-digit adds, 2-digit ×, bigger parens) base 84.4% vs tuned 78.1% (n=32, sampled, within noise but clearly no improvement). It overfit the narrow distribution.

### Minor
- `best_model_checkpoint: None` — `load_best_model_at_end` wasn't set, so `final/` is step 760 (0.9238) rather than the best (725, 0.965). Negligible here, but worth enabling.
- `report_to="none"` → no wandb/tensorboard; the only curves are in `checkpoint-760/trainer_state.json`. I parsed it manually.
- `final/ref/` being 2× the size of the policy adapter is just fp32 vs bf16, not a bug.
- Eval peeked at ~1.2 GB VRAM on the 4070, so you have lots of headroom — you can afford a bigger model or `num_generations=8`.

### If you want to iterate
1. Add a format SFT warmup (highest impact — this is the whole point of the experiment).
2. Make the data hard enough that base accuracy is ~30–50%: 3–4 digit arithmetic, multi-step, or swap in `--dataset gsm8k` (1500 train).
3. `--num-epochs 1` + `metric_for_best_model="eval_reward"` + early stopping.

Want me to save the two eval scripts into the repo (they're in `/tmp/eval_adapt.py`, `/tmp/eval_indist.py`) and wire up the format warmup + harder dataset as a `run2.sh`?
