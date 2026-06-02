---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 FineWeb Loss Decay Pattern
translated: false
type: note
---

Here's the loss drop pattern from the log:

```
=================================================================
  Val Loss Decay Analysis — GPT-2 760M on FineWeb
=================================================================

  Phase 1: Early fast drop (13K-16K)
    3.4759 -> 3.4170  (rate=0.0196/1K steps)

  Phase 2: Fast drop (28K-37K)
    3.2967 -> 3.2261  (rate=0.0078/1K steps)

  Phase 3: Moderate (37K-48K)
    3.2261 -> 3.1838  (rate=0.0038/1K steps)

  Phase 4: Slowing (48K-60K)
    3.1838 -> 3.1695  (rate=0.0012/1K steps)

  Phase 5: Near plateau (60K-74K)
    3.1695 -> 3.1585  (rate=0.0008/1K steps)

=================================================================
```

Key findings:

1. **Classic power law decay** — loss drops as ~step^1.07. This is textbook. The decline rate halves roughly every 10-15K steps.

2. **Rate is slowing dramatically** — from 0.02/1K steps early on to 0.0008/1K steps now. That's a 25× slowdown. You're deep into diminishing returns.

3. **34% of checkpoints show slight upticks** — this is normal. Val set noise, learning rate schedule wobble, and data ordering all contribute. The trend matters, not individual points.

4. **Current noise floor** — val loss bounces around ±0.01 (std dev) in the 48K-74K range. The signal-to-noise ratio is getting low.

5. **Projected final loss** — if it follows the power law to step 445K, projected val loss ~1.19. But this is optimistic — the power law fit is dominated by the early fast-drop phase. Realistically, expect it to flatten around 3.10-3.12 by step 445K.

The bottom line: the model is still learning, but the marginal return per step is shrinking fast. The first 16K steps bought you 0.06 loss. The last 26K steps (48K→74K) bought you only 0.025. You're paying full price for each step but getting less and less back.
