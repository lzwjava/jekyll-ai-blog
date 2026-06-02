---
audio: false
generated: true
image: false
lang: en
layout: post
title: Shakespeare Model Training Progress
translated: false
type: note
---

Working! After just 500 iterations on a 10.65M parameter model, it's generating Shakespearean-sounding (if somewhat garbled) text. Here's the summary:

**Training results:**

- Model: 10.65M params, 6-layer character-level GPT
- Loss: 4.28 → 1.71 (val) in 500 steps (~30s total)
- Checkpoint saved to `out-shakespeare-char/`

**Samples with prompt `"To be or not to be"`** show the model has learned:

- English words and basic grammar
- Some Shakespearean vocabulary ("Madam", "noble", "thee/thou")
- Line breaks like stage dialogue
- But still incoherent at 500 iters — train to 5000 for much better quality

To get proper Shakespeare-quality text, run the full 5000 iters:

```bash
python3 train.py config/train_shakespeare_char.py
```
