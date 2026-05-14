---
audio: false
generated: true
image: false
lang: en
layout: post
title: Finish Baseline Before Scaling Up
translated: false
type: note
---

**Let it finish.** Reasons:

1. **76% sunk cost, ~14h left.** Killing now throws away 46 GPU-hours to save 14. Not worth it.
2. **You need a baseline.** "How far can the 4070 go" only means something against a reference point. A clean 124M / 10B / val-3.0X run at this exact config is exactly the baseline you'll compare every bigger run to. Stopping mid-cosine gives you a *worse* baseline (LR not decayed, val noisier).
3. **No new info from stopping early.** The loss curve flattened around step 12k; the remaining 4.5k iters are mostly LR-decay polish. Letting it run answers "where does 124M plateau on this config" — useful — without committing more than one extra day.
4. **The next experiment is multi-day anyway.** A 350M medium run at this tokens/step is ~3–4× per step → 5–6 days. 14h to lock in a baseline first is rounding error.

The only reason to kill it would be if you'd discovered a bug in the run (you haven't) or needed the GPU urgently for something else.

**Suggested plan when it finishes tonight:**

1. Back up the final ckpt: `cp out-fineweb-gpt3/ckpt.pt out-fineweb-gpt3/ckpt_124M_10B_final.pt` — `always_save_checkpoint=True` will otherwise stomp it the next run.
2. Note the final val loss + sample some generations (`python sample.py --out_dir=out-fineweb-gpt3`) as the baseline qualitative reference.
3. Kick off the next rung. Two reasonable directions — pick one, not both:

   - **Scale params** → gpt2-medium 350M, 10–20B tokens. Answers "can the 4070 train a 350M at all, and how does loss compare to 124M at the same token budget."
   - **Scale tokens** → keep 124M, bump `max_iters` to ~38k (≈20B). Answers "is 124M token-starved at 10B, or saturated."

The medium-scale run is the more informative one for your stated goal (find the 4070's ceiling). I'd go that direction.

Want me to draft the `train_fineweb_gpt2_medium.py` config now so it's ready to launch the moment this one finishes?