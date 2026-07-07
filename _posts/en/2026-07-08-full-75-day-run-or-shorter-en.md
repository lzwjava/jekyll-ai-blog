---
audio: false
generated: true
image: false
lang: en
layout: post
title: Full 7.5-Day Run or Shorter?
translated: false
type: note
---

Rough estimate based on the MI300X reference and H200 specs:

**~7.5 days** for Chinchilla-optimal (20× param ratio = 29B tokens)

Breakdown:

- 760M model on MI300X: 68K tok/sec, 62h for 15.2B tokens
- 1.45B model on H200: **~40-45K tok/sec** (model 2× bigger, but FA3 is faster)
- 29B tokens ÷ 42K tok/sec ≈ **180 hours ≈ 7.5 days**

**Options:**

| Training horizon | Tokens | Est. time | Quality |
| --- | --- | --- | --- |
| **Chinchilla (20×)** | 29B | ~7.5 days | Optimal |
| **Half Chinchilla (10×)** | 14.5B | ~3.7 days | Decent |
| **Quick (5×)** | 7.25B | ~1.9 days | Rough baseline |

Or go smaller model for faster turnaround:

| Model | Params | Time (20× Chinchilla) |
| --- | --- | --- |
| d24 (MI300X ref) | 760M | ~2.6 days |
| d30 | **1.45B** | ~7.5 days |
| d20 | 530M | ~1.9 days |

Want to go for the full 7.5-day run or do a shorter one first?
