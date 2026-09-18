---
audio: false
generated: true
image: false
lang: en
layout: post
title: tags training progress
translated: false
type: note
---

## tmux status

**Session `2`** — training is running, currently healthy.
**Session `0`** — just `mihomo` (proxy), unrelated.

### Running job

```
/mnt/data/zz/grpo-rl  →  .venv/bin/python train_grpo.py
  --model Qwen/Qwen2.5-1.5B --dataset synthetic
  --num-epochs 2 --per-device-batch-size 2 --grad-accum 4
  --num-generations 4 --max-completion-length 384
  --lr 5e-6 --beta 0.02 --temperature 1.0
```

- Elapsed: **1h 36m**
- GPU: RTX 4070, **80% util, 6.2 GB / 12 GB** (torch cu128, real CUDA run)
- `step_time` 2.5–4.6 s/it, loss ~1e-3, `grad_norm` mostly ~0.4, KL 0.02–0.05

### Progress: **step 650 / 760 (86%) — epoch 1.71 / 2**

The tqdm bars:

```
86%|██████████████▋      | 650/760 [1:29:09<07:15, 3.96s/it]   ← training
70%|█████████████▍       |  14/20 [00:44<00:17, 2.86s/it]    ← eval pass (40 eval ex ×bs2)
```

**ETA ≈ 13–15 min** (~7 min training + 4 evals of ~65 s each + final save). Last checkpoints written: `checkpoint-600`, `checkpoint-625` (LoRA adapters, ~37 MB, `save_total_limit=2`).

### Reward history

| | first 50 steps | last 50 steps |
|---|---|---|
| train `reward` | 0.561 | **0.936** |

| eval step | 25 | 150 | 250 | 375 | 450 | 600 | 625 |
|---|---|---|---|---|---|---|---|
| `eval_reward` | 0.642 | 0.888 | 0.908 | 0.925 | 0.963 | 0.944 | 0.884 |

So the run **did learn**, but it plateaued around **step 150–375**; epoch 2 (steps 380→760) has produced no further gain.

### Two things worth flagging

1. **`rewards/reward_format/mean` is `0` at every single step and eval** — same for `std`. `reward` == `reward_correctness` numerically. The prompt asks for `<think>...</think>` tags and `reward_format` gives up to +0.3 for them, but the model never emits the tags, so that whole shaping term is dead. Worth checking why (likely the base model just never samples the tag, so it's never rewarded into existence — a cold-start problem).
2. **`frac_reward_zero_std` is climbing: 0.35 → 0.725–0.9.** Train reward is pinned at 1.0 on many steps (see the tail: `[1.0, 1.0, 1.0, 1.0, 1.0, 0.625, ...]`). Once all `G=4` generations in a group get identical reward, the advantage is zero and the step contributes no gradient. That's why epoch 2 is essentially wasted compute — the synthetic arithmetic task is saturated.

Practical read: the run is fine to let finish (~15 min), but for a next run consider raising task difficulty, cutting to `--num-epochs 1`, and fixing the `<think>` cold-start.
