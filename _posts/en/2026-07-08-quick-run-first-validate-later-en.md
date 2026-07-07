---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quick run first, validate later
translated: false
type: note
---

Question: Given the throughput estimates for a 1.45B-param model on H200 (~40-45K tok/sec) vs the 760M-param MI300X reference (~68K tok/sec), which training horizon should I choose — full Chinchilla-optimal (29B tokens, ~7.5 days), half (14.5B, ~3.7 days), or quick (7.25B, ~1.9 days)?

Answer:

**Do the quick run first. Don't commit to 7.5 days blind.**

**Why:**

1. **You haven't validated the pipeline on H200 yet.** Different GPU, different arch (Hopper vs CDNA3), different FA kernel path (FA3 vs whatever ROCm uses). Throughput estimates are extrapolated, not measured. If your actual MFU comes in at 25% instead of 35%, your 7.5-day estimate becomes 10+ days and you've burned rental cost discovering that on day 3.

2. **Sanity-check the FLOPs math before trusting Hermes' numbers.** Rough cross-check:

```python
# Compute-based throughput sanity check (Kaplan/Chinchilla approximation)
def est_tok_per_sec(params, peak_tflops, mfu):
    flops_per_token = 6 * params  # fwd+bwd, dense transformer
    achieved_flops = peak_tflops * 1e12 * mfu
    return achieved_flops / flops_per_token

# MI300X, 760M model
print(est_tok_per_sec(760e6, peak_tflops=1307, mfu=0.24))  # ~413K...
# wait — check against their reported 68K tok/s implied MFU:
def implied_mfu(params, tok_per_sec, peak_tflops):
    flops_per_token = 6 * params
    return (flops_per_token * tok_per_sec) / (peak_tflops * 1e12)

print(implied_mfu(760e6, 68_000, 1307))   # MI300X bf16 peak ~1307 TFLOPS
print(implied_mfu(1.45e9, 42_000, 989))   # H200 bf16 dense peak ~989 TFLOPS
```

Run these two — MI300X comes out ~24% MFU, H200 estimate comes out ~36% MFU. That's plausible (H200's software stack + FA3 genuinely does better MFU on small dense models than ROCm today), but it's an *estimate stacked on an estimate*. First 30 minutes of real training will tell you the true number — measure `tokens/sec` directly from your training loop, don't trust the projection.

3. **Opportunity cost matters more than compute-optimality right now.** You're pre-revenue-stable, still building the service pipeline, and a 760M/1.45B dense model isn't your moat — nanochat/DeepSeek v4 MoE understanding is. A week-long single run that produces one checkpoint is a bad trade against: validating the pipeline, writing a blog post, and freeing the H200 budget for MoE experiments where the real frontier learning happens.

**Suggested sequence:**

| Step | Tokens | Time | Purpose |
|------|--------|------|---------|
| 1. Smoke test | 100M | ~10 min | Confirm no NaNs, checkpoint/resume works, measure real tok/sec |
| 2. Quick baseline (5×) | 7.25B | ~1.9 days | Real loss curve, real checkpoint, publishable result |
| 3. Decide | — | — | If loss curve + eval justify it, scale to half or full Chinchilla with confidence |

Skip straight to a 7.5-day commit only if you already have a working checkpoint/resume harness and are prepared to lose the run to a preemption/OOM/driver hiccup with nothing to show.

**Minimal checkpoint/resume harness** (if you don't have one — non-negotiable for anything >1 day on rented compute):

```python
import torch, os, time

def save_ckpt(model, opt, step, path="ckpt.pt"):
    torch.save({
        "model": model.state_dict(),
        "opt": opt.state_dict(),
        "step": step,
    }, path + ".tmp")
    os.replace(path + ".tmp", path)  # atomic write, survives crash mid-save

def load_ckpt(model, opt, path="ckpt.pt"):
    if not os.path.exists(path):
        return 0
    ck = torch.load(path, map_location="cuda")
    model.load_state_dict(ck["model"])
    opt.load_state_dict(ck["opt"])
    return ck["step"]

# in training loop
step = load_ckpt(model, opt)
last_save = time.time()
for step in range(step, total_steps):
    train_step(...)
    if time.time() - last_save > 600:  # every 10 min
        save_ckpt(model, opt, step)
        last_save = time.time()
```

Also log `tokens/sec` and cost-per-billion-tokens every checkpoint — you'll want that number for pricing consulting engagements that involve training infra advice; "I've actually measured $/token on H200 vs MI300X" is a real differentiator over API-wrapper consultants.

**Bottom line:** run the 1.9-day quick baseline, measure real throughput in the first hour, then decide on the full Chinchilla run with actual data instead of an extrapolated table.
