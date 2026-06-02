---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maximizing GPU Memory Usage Safely
translated: false
type: note
---

## Analysis: pushing 4070 memory from ~7.5 GB → ~10–11 GB

### Where memory comes from

At `batch_size=4, block_size=1024`, you're using 7538 MiB. Roughly:

- **Fixed**: weights + grads + AdamW states (m, v) ≈ ~2 GB for 124M params
- **Activations**: the rest (~5.5 GB), scales linearly with `batch_size` and quadratically-ish with `block_size`

So ~1.4 GB of activations per unit of `batch_size`. To hit ~10.5 GB you need roughly **+3 GB of activations → batch_size ≈ 6**, maybe 7 if you're aggressive.

### Main lever: `batch_size` (lines 15, 17)

Keep tokens-per-step (~524,288) constant so your LR schedule / `warmup_iters` / `max_iters` don't need re-tuning:

| `batch_size` | `gradient_accumulation_steps` | Tokens/step     | Expected VRAM       |
| ------------ | ----------------------------- | --------------- | ------------------- |
| 4 (current)  | 128                           | 524,288         | 7.5 GB              |
| 6            | 85 or 86                      | ~528K           | ~10 GB              |
| 8            | 64                            | 524,288 (exact) | likely OOM on 12 GB |

I'd start at **`batch_size=6, gradient_accumulation_steps=86`** and watch `nvidia-smi`. If there's headroom, try 7. Tokens/step won't be exactly identical with 6 — that's fine, the LR schedule is robust to a few % drift.

### Why not other levers

- **`block_size`**: tied to the GPT-2 124M architecture and to how the data was tokenized/sharded. Don't change it.
- **`n_layer / n_head / n_embd`**: changes the model, not just memory.
- **`compile=True`**: already on.
- **Precision**: nanoGPT already uses bf16/AMP by default in `train.py` — verify, but no config change needed.

### Caveats

- Display/Xorg holds ~115 MiB, so usable budget is ~12,160 MiB, not 12,288.
- First `torch.compile` step spikes memory; if it OOMs only on compile, that's not a steady-state problem but you still can't run it. Be conservative.
- Going from 128 → 86 grad-accum steps means **fewer optimizer updates per wall-clock second of compute** but the **same effective batch**, so loss curves should look the same. Step throughput (tokens/sec) should improve modestly because there's less Python/PyTorch overhead per token.

### TL;DR

Bump `batch_size` from 4 → 6 and `gradient_accumulation_steps` from 128 → 86. Everything else stays. Expect ~10 GB VRAM and a small throughput win.
