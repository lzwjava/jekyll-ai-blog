---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fineweb-Code-SEC Training Summary
translated: false
type: note
---

Training completed. Here's the full summary:

---

**code-sec-fineweb-d12 — Complete (50,000 steps, 16.5 hours)**

| Step | Val BPB | Train Loss | Time |
| ------ | --------- | ------------ | ------ |
| 5,000 | 1.680 | 1.397 | 1.6h |
| 10,000 | 1.640 | 1.372 | 3.3h |
| 15,000 | 1.626 | 1.465 | 4.9h |
| 20,000 | 1.595 | 1.363 | 6.6h |
| 25,000 | 1.568 | 1.136 | 8.2h |
| 30,000 | 1.536 | 1.199 | 9.9h |
| 35,000 | 1.510 | 1.229 | 11.5h |
| 40,000 | 1.468 | 1.169 | 13.1h |
| 45,000 | 1.446 | 1.077 | 14.8h |
| **50,000** | **1.418** | **1.062** | **16.5h** |

**Key differences from previous fineweb-only run (val_bpb: 0.866):**

- Final val_bpb is **1.418 vs 0.866** — higher, but expected: code + SEC are harder domains than web text alone (code has denser token distributions)
- Smooth train loss: 1.062 — loss is still trending down at step 50k, suggesting more training would help
- The model saw code, SEC filings, and web text — likely better at code/finance than the fineweb-only model

**Checkpoints:** `/home/lzw/.cache/nanochat/base_checkpoints/d12/` — 10 checkpoints (5k intervals), 793MB each
