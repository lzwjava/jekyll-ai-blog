---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Minispeed: Mini DeepSpeed-Style Distributed Training"
translated: false
type: note
---

Done. **minispeed** — a mini DeepSpeed-style distributed training framework — is implemented, tested, and committed (`9c2bc67`, 26 files, ~3000 lines).

## What was built

```
minispeed/
├── engine.py                  DeepSpeedEngine: backward() / step() / accumulation boundaries
├── config.py                  DeepSpeed JSON config parsing + validation (fail-fast)
├── comm.py                    backend/device selection, collective wrappers (no-op single-proc)
├── flat.py                    FlatParamGroup: params → contiguous fp32 master buffers
├── precision.py               DynamicLossScaler + inf/nan detection
├── zero/stage_1_and_2.py      reduction, sharding, all-gather (stages 0/1/2)
├── optim/adam.py              AdamW over flat buffers, state only on this rank's shard
├── optim/scheduler.py         WarmupLR / WarmupDecayLR (DeepSpeed schema)
├── checkpoint.py              sharded save/load (global_stepN/ + latest pointer)
└── activation_checkpointing.py
examples/train_lm.py           tiny char-GPT, runs single-GPU or under torchrun
tests/                         36 passed, 2 skipped (NCCL needs ≥2 GPUs)
```

## Key features

- **ZeRO 0/1/2**: all-reduce vs reduce-scatter gradients, optimizer state sharded, params all-gathered each step; global grad norm stays exact under stage 2 via partitioned sum-of-squares
- **fp16** with fp32 master weights + dynamic loss scaling (window growth, ∞/NaN → skip + halve), **bf16** without scaling
- **Gradient accumulation**, global clipping, `train_batch_size` validation, warmup/decay LR
- **Auto backend**: NCCL when `world ≤ #GPUs`, else gloo over CUDA tensors (so `torchrun --nproc_per_node=2` works on this single-GPU box)
- DeepSpeed-style API: `engine, opt, _, sched = ms.initialize(model=..., config="ds_config.json")`

## Verified

- Engine trajectory **matches plain `torch.optim.AdamW`** to 1e-4; `gas=2` accumulation ≡ one big batch
- 2-rank runs (gloo/CPU and gloo/CUDA, fp32+fp16, stages 0/1/2) **match a single-process run on the union batch**; optimizer state provably partitioned
- fp16 GPU: forced-∞ grad → step skipped, weights untouched, scale halved, then recovers
- Checkpoint resume reproduces the exact training trajectory; wrong `world_size` refused

```bash
python examples/train_lm.py --dtype fp16 --zero 2            # 1 GPU: loss 83 → 2.3
torchrun --nproc_per_node=2 examples/train_lm.py --zero 2    # 2 ranks
python -m pytest tests/ -q                                   # 36 passed, 2 skipped
```
