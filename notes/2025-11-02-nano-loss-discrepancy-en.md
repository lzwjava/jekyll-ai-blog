---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: NanoGPT CPU vs GPU Loss Discrepancy
translated: false
type: note
---

### Understanding the Loss Discrepancy in NanoGPT Training

Your laptop (CPU) run wrapped up at 2000 iterations with a train loss of ~1.76 and val loss of ~1.89—decent progress from the initial ~4.0+ entropy baseline for Shakespeare chars, but still high compared to the 4070 Ti's 5000-step results (train 0.62, val 1.70). The per-iteration losses (1.90 → 1.70) show steady decline, but the gap to GPU performance is expected. Let's break it down:

#### Why Higher Losses on CPU (Laptop)
- **Fewer Effective Iterations**: You stopped at 2000 iters due to time (each ~100-1500ms, totaling ~40-50 mins?), while the GPU cranks through 5000 in similar wall time thanks to 10x+ speed. NanoGPT's Shakespeare config converges slowly early on; losses drop sharply after ~5k-10k iters as the model learns n-gram patterns and basic grammar. At 2k, you're still in the "memorizing characters" phase—val loss hasn't bottomed out yet. GPU's extra 3k iters let it refine to sub-1.0 train loss.

- **Gradient Noise and Precision**: CPU training uses FP32 by default (no AMP/FP16 like on CUDA), leading to slightly different numerics and potentially noisier updates. Combined with lower effective batch size (your 12 is small; CPU can't parallelize as well), this slows convergence. The mild overfitting (val > train by ~0.12) is normal, but on GPU it's more pronounced (1.70 vs 0.62) because faster training amplifies memorization before generalization kicks in.

- **Eval Mechanics**: Both use `estimate_loss()` with ~200 batches per split. Your CPU val loss (1.89) is higher partly because the model hasn't seen enough data variety—Shakespeare is tiny (~1M chars), so early evals are volatile. GPU's lower val (1.70) reflects better optimization, not just more steps.

| Metric | Laptop (2000 iters, CPU) | 4070 Ti (5000 iters, GPU) | Why the Diff? |
|--------|---------------------------|----------------------------|---------------|
| **Train Loss** | 1.76 | 0.62 | GPU: More steps + parallel grads = faster descent. |
| **Val Loss** | 1.89 | 1.70 | Both overfitting mildly; CPU lags due to fewer updates. |
| **Per-Iter Loss** | 1.70 (iter 2000) | 0.82 (iter 5000) | Extrapolate: CPU might hit ~1.2-1.5 at 5k if continued. |
| **MFU** | 0.01% | 9.99% | Hardware limits; irrelevant to loss but explains speed. |
| **Time per Iter** | 116-1505ms (variable, I/O heavy) | 4447ms? (Wait, that seems high—maybe incl. eval; typical <200ms) | CPU serial bottleneck vs GPU parallelism. |

#### Expected Convergence Trajectory
For this config (4-layer, 128-dim, no dropout), typical Shakespeare char losses:
- 0-1k iters: Train ~2.5-3.0, Val ~3.0+ (basic token prediction).
- 2k iters: Train ~1.8-2.2, Val ~2.0 (your spot—learning bigrams/trigrams).
- 5k iters: Train ~1.0-1.5, Val ~1.5-1.8 (GPU-like; starts generating coherent lines).
- 10k+: Train <1.0, Val ~1.3 (cross-entropy near perplexity 3-4; fun samples).

Your CPU run is on track but truncated. If you let it go to 5k (expect 2-3x longer, ~2 hours), train/val should dip to ~1.4/1.6—still above GPU due to subtle inefficiencies, but usable for testing.

#### Tips to Close the Gap on Laptop
- **Train Longer**: Bump `--max_iters=5000` and `--lr_decay_iters=5000`. Add `--eval_interval=500` to check progress without full stops. Use `nohup` or `screen` for overnight runs.

- **Tweak for CPU Efficiency**:
  - `--batch_size=24` (if >8GB RAM; yours should handle it—check with `free -h`).
  - `--compile=True` (PyTorch 2.0+; fuses ops, +20-30% speed).
  - Enable FP16: Add `--init_from=resume` if resuming, or hack `dtype=torch.float16` in config (but watch for CPU FP16 support; fallback to bfloat16 if errors).
  - Reduce `--eval_iters=10` for quicker checkpoints.

- **Resume and Compare**: Save your checkpoint (`out-shakespeare-char`), then on GPU: `python train.py config/train_shakespeare_char.py --device=cuda --compile=False --resume=out-shakespeare-char/ckpt-2000.pth --max_iters=5000`. This isolates if it's steps or hardware—expect val loss to plummet to ~1.0 in the next 3k iters.

- **Sample Generations**: At your losses, CPU model spits semi-coherent Shakespeare ("To be or not to be, that is the quoth"). GPU at 5k: Full soliloquies. Run `python sample.py` on both checkpoints to visualize.

If you share the full train log or `sample.py` outputs, I can pinpoint more (e.g., if LR decay is too aggressive). CPU prototyping is fine for debugging—save the heavy lifting for GPU!
