---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Training Progress and Time Estimate
translated: false
type: note
---

### Current progress

- You've just passed iter 2800 (out of your target 20,000)
- Stable speed right now: **≈ 3.91 seconds per iteration**
  (the occasional 19-second logs at eval steps are only every 500 iters and don’t change the average much)

### Remaining iterations

20,000 − 2,800 = **17,200 iterations left**

### Estimated time to finish

| Average iter time | Remaining time | When it will finish (from now, Nov 19 2025) |
|-------------------|----------------|---------------------------------------------|
| 3.91 s (current)  | **18 hours 35 minutes** | ~ **tomorrow (Nov 20) around 14:30–15:30** (depending on your timezone and exact start time of this log) |
| Slightly faster (3.8 s, common as MFU climbs a bit more) | ~ 18 hours         | tomorrow early–mid afternoon              |
| Slightly slower (4.0 s) | ~ 19 hours 5 min   | tomorrow ~16:00                            |

Realistic expectation on an RTX 4070 with this exact setup: **18–19 hours from now**.

### Quick reference

- If you started logging this around noon–early afternoon today → finishes tomorrow morning–early afternoon.
- If you let it run overnight → you’ll wake up to a finished (or almost finished) very strong 40M model tomorrow.

Your loss is dropping nicely (val loss already 3.94 at only ~1.5B tokens seen) and still falling steadily. Absolutely worth letting it run the full 20k — just leave it going overnight and you’ll have an excellent model by tomorrow afternoon!
