---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 124M Training Loss Spikes
translated: false
type: note
---

Here's the analysis:

========================================================================
GPT-2 124M github-code — Loss Analysis (steps 262k–280k)
========================================================================

    Step  Train Loss    Val Loss   Δ Train  Notes
------------------------------------------------------------------------
  262000      3.0952      3.0265
  263000      3.3459      3.2922    +0.251
  264000      3.6089      3.3886    +0.263
  265000      3.8677      3.7542    +0.259
  266000      3.9365      3.8930    +0.069
  267000      5.0157      5.0602    +1.079  <<< SPIKE
  268000      5.0102      5.1968    -0.005  <<< SPIKE
  269000      4.6592      4.7792    -0.351
  270000      4.2488      4.2854    -0.410
  271000      3.9500      3.9416    -0.299
  272000      3.7400      3.8020    -0.210
  273000      3.6361      3.5530    -0.104
  274000      3.4293      3.5930    -0.207
  275000      3.5167      3.6213    +0.087
  276000      3.6871      3.5147    +0.170
  277000      3.7307      3.6379    +0.044
  278000      3.4410      3.4339    -0.290
  279000      4.4294      4.6838    +0.988  <<< SPIKE
  280000      4.2341      4.3662    -0.195

Tokens seen: ~9.2B of 14B planned (65.6%)

--- Key Findings ---

1. LOSS WAS RISING, NOT FALLING (steps 262k–266k)
   Before the first spike, train loss climbed from 3.10 → 3.94 over
   just 4000 steps. That's a +27% increase. At this stage of training
   (60%+ done) loss should be flat or slowly decreasing. Something was
   already going wrong before the big spike.

2. TWO MAJOR LOSS SPIKES
   - Spike 1 at step 267k–268k: loss jumped from 3.94 → 5.02 (+1.08).
     Val loss hit 5.20. This is a 28% single-step jump — extremely
     abnormal for a cosine LR schedule at this point.
   - Spike 2 at step 279k–280k: loss jumped from 3.44 → 4.43 (+0.99).
     Another ~29% jump. Not as deep as spike 1 but same pattern.

3. SLOW RECOVERY BETWEEN SPIKES
   After spike 1, loss took ~10k steps (269k→278k) to recover from
   5.02 back down to 3.44. That's a lot of wasted compute — roughly
   10,000 steps × 32,768 tokens = 328M tokens just recovering.

4. BEST LOSS WAS AT THE START OF THIS WINDOW
   The lowest val loss was 3.03 at step 262k. Current val loss is
   4.37 — the model has gotten WORSE, not better, over this window.

5. PERIODICITY SUGGESTS DATA SHARD ROTATION
   The spikes are ~12k steps apart (267k and 279k). If the dataset
   cycles through shards or shards have very different distributions
   (e.g. different languages, file types), that could explain periodic
   loss shocks when hitting a "hard" or out-of-distribution shard.

--- Likely Causes ---

a) DATA DISTRIBUTION SHIFT: The github-code dataset likely has shards
   with very different code characteristics (languages, file types,
   comment density). When the data loader wraps to a new shard, the
   model suddenly faces out-of-distribution data → loss spike.

b) LR MAYBE TOO HIGH for this stage: At step 262k with cosine decay
   from 6e-4 → 6e-5 over 427k steps, the LR is still ~2.7e-4.
   That's 45% of peak — quite aggressive for mid-training. The
   increasing loss before spike 1 suggests the model was oscillating.

c) NO GRAD NORM CLAMPING EVIDENCE: If grad_clip=1.0 isn't catching
   outlier gradients from hard shards, the optimizer can overshoot.

--- Recommendations ---

- Check if loss spikes correlate with shard boundaries in the data
  loader (log the shard index each eval).
- Consider lowering LR or switching to a warmer cosine schedule.
- If the model keeps spiking, it may be worth restarting from the
  step 262k checkpoint (best val loss) with a gentler LR schedule.
- The current val loss (4.37) is worse than step 262k (3.03) — the
  last ~18k steps may have been net negative for model quality.
