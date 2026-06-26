---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC Filing Training Spike and Recovery
translated: false
type: note
---

There's the full picture. Here are the key takeaways:

THE STORY IN 4 PHASES:

Phase 0 (steps 0→19k, not in buffer): Started from scratch, loss dropped from ~10.8 (random) to 2.70. Model learned SEC filing structure fast.

Phase 1 (steps 19k→21k): CATASTROPHIC SPIKE. Val loss jumped 2.70 → 8.04 in 2000 steps. Train loss spiked too (not overfitting) — this was a DATA event. The sequential shard loader hit a run of structurally weird filings (XBRL-heavy, unusual exhibits, nested tables). The model didn't break; the data changed.

Phase 2 (steps 21k→30k): RECOVERY. 8.04 → 3.34 over 9000 steps. ~20% of total training spent re-learning what it already knew. No intervention needed.

Phase 3 (steps 30k→37k): SMOOTH CONVERGENCE. 3.34 → 2.45. Clean power-law decline. Still going.

COMPARISON:

- SEC-EDGAR at 2.45 val loss is BEATING GPT-2 on OpenWebText (~2.85)
- GitHub-Code was 3.466 and produced garbage
- SEC filings are a narrow, structured domain — easier to model than general text

The per-iter loss swings (0.79 to 7.73) look scary but are normal for batch=32k tokens. The val loss (100-iter average) is the only number that matters.

~12 minutes remaining. Should finish around val_loss ≈ 2.2-2.3.
