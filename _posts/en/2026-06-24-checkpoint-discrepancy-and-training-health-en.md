---
audio: false
generated: true
image: false
lang: en
layout: post
title: Checkpoint Discrepancy and Training Health
translated: false
type: note
---

**Question:** Explain the training run status — checkpoint vs. live tmux discrepancy, training health, and what to expect for the remaining ~100k steps.

**Answer:**

## What Happened: The Crash/Restart Pattern

The discrepancy is straightforward. Training ran to iter 350k, something interrupted it (OOM, SIGKILL, node preemption on AMD cloud, whatever), and the runner script reloaded the most recent *eval* checkpoint — step 325k with val loss 2.7892 — rather than the 350k checkpoint. So you lost ~25k steps of compute and are re-running that segment.

Why 325k and not 350k? Likely because `eval_interval` checkpoints are saved separately from the "best" checkpoint. The 350k `ckpt.pt` is the best-val checkpoint (loss 2.92 at that point), while 325k was a periodic eval save. The restart logic probably picked the most recent *eval* checkpoint, which happened to be 325k.

**Key implication:** val loss 2.7892 at 325k is *better* than 2.92 in the saved `ckpt.pt`. This means the live run is actually ahead of the checkpoint in terms of model quality. Don't restore from `ckpt.pt` — let it run.

---

## Training Health Breakdown

**Loss trajectory** — totally normal for a 124M non-embedding GPT-2 scale model:

```
Step 0:      10.87   (random init, ~log(50257) ≈ 10.82 — basically perfect)
Step 25k:    ~3.6    (fast early descent)
Step 325k:   2.7892  (val, current best)
```

The step-0 loss matching `log(vocab_size)` is a good sign — weights initialized correctly, no pathological startup.

**Learning rate** — you're deep into cosine decay. If peak LR was 6e-4 and you're now at ~1e-4, you're past the 80% mark of the schedule. The formula:

```
lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(π * t/T))
```

At t=325k, T=427k: `cos(π * 325/427) ≈ cos(2.39) ≈ -0.73`, so LR is near the floor. This is expected — the optimizer is taking small, precise steps now.

**MFU 14.44%** on MI300X is on the low side. Theoretical peak for MI300X is ~383 TFLOPS (bf16). At 14.44% utilization, you're getting ~55 TFLOPS effective. For a 124M model with small batch sizes, this is typical — the model is too small to saturate HBM bandwidth. You'd need larger batch or gradient accumulation to push MFU higher. Not a problem for this run, just context.

**621ms/step stability** — no degradation means no memory pressure building up, no thermal throttling, no gradient explosion requiring fallback. Solid.

---

## What the Next ~100k Steps Will Do

With cosine LR near the floor, you're in the "polishing" phase. The loss curve flattens here — expect maybe 2.79 → 2.65 range by the end, depending on data quality and schedule. The remaining gains come from:

1. **Data coverage** — model sees the tail end of the 14B token corpus, fills in distribution gaps
2. **Fine-grained weight updates** — tiny LR means no overshooting, optimizer converges weights to a local minimum

What you *won't* get: dramatic loss drops. The steep descent was steps 0-100k. You're past that.

**ETA:** 100k steps × 621ms = ~17.3 hours. Given the AMD cloud costs ~$2/hr, that's ~$35 to finish. Worth it if you haven't already sunk $100+ into this run — the model at 2.79 val loss is meaningfully better than 2.92.

---

## Practical Next Steps

```bash
# Verify the live run's checkpoint is saving correctly
ls -lth /path/to/checkpoints/ | head -5

# Watch val loss progression
grep "val loss" nanoGPT_train.log | tail -20

# Confirm it'll resume correctly if it crashes again
# Look for: iter_num, best_val_loss in the checkpoint
python -c "import torch; ck=torch.load('ckpt.pt'); print(ck['iter_num'], ck['best_val_loss'])"
```

One thing worth checking: make sure `always_save_checkpoint = True` or equivalent is set so that *every* eval checkpoint is saved, not just best-val. That way a future crash at 400k doesn't roll you back to 325k again.
