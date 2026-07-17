---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Frozen Root: In-Context Learning"
translated: false
type: note
---

Question: Does "reusing the same 五指毛桃 root for a third stew" map to "fine-tuning" in ML terms?

Answer: Your correction instinct is right — it's not quite fine-tuning. Here's why:

**What actually happens in the pot:**
- The root = frozen base weights (a pretrained model). It already encodes compressed "flavor" from prior training runs (first two boils).
- 3rd boil, same root, no update to the root itself = a **forward pass on frozen params**, not a gradient update.
- New ingredients each round (corn, carrot, beef shank, shrimp, orange) = new input/prompt/context, not new training data.

So the process is closer to **in-context learning / inference with varying prompts on a frozen model** than to fine-tuning. Fine-tuning requires backprop through the root — i.e. the root's internal composition changes based on what you feed it (LoRA-style weight delta, or full param update). Here the root is literally the same tensor every time; only the context (soup ingredients) changes, and the output (soup flavor) is a function of `frozen_weights(root) + new_context(ingredients)`.

**Where it does map correctly:**
- Diminishing 3rd-boil flavor extraction ≈ diminishing marginal gradient signal when you keep training on the *same* data repeatedly without new information — epoch N+1 on identical data extracts less new signal than epoch 1. That's a real analogy (data exhaustion / overfitting territory), just not "fine-tuning" specifically.

If you wanted a soup analogy that *is* fine-tuning: you'd have to alter the root itself between boils (e.g. marinate it, break it down further) so its own composition changes and persists into future stews — that's updating the weights, not just re-extracting from a static substrate.

TL;DR: same frozen root + different toppings each time = **in-context inference**, not fine-tune. Your gut catch (微调模型好像不妥当) was correct.
