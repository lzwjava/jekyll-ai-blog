---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exponential Moving Average Explained Briefly
translated: false
type: note
---

**EMA** stands for **Exponential Moving Average**.

It’s a type of weighted average that gives **more weight to recent observations** and less weight to older ones, decaying exponentially over time.

---

### In the context of your training loss discussion:

When you said *"the EMA window is very small"*, you meant that the smoothing factor used to average your loss values over time is set to look at only a very short history. 

- **Small EMA window** = the smoothed loss reacts very quickly to new batches. It follows the noisy raw loss closely, so it **looks jumpy**.
- **Large EMA window** = the smoothed loss reacts slowly, averages over many more steps, and **looks flat and stable** (like your 100-step view).

---

### Mathematically (simple version):

\\[
\text{EMA}_t = \alpha \times \text{value}_t + (1 - \alpha) \times \text{EMA}_{t-1}
\\]

- \\(\alpha\\) (alpha) is the **smoothing factor**. 
- A **large alpha** (e.g., 0.5) means a *small window* – recent values dominate, very responsive.
- A **small alpha** (e.g., 0.01) means a *large window* – very smooth, slow to change.

---

### Where else is EMA used in ML/LLM training?

1. **Model parameter averaging** (e.g., EMA of weights) – often used to produce a more stable final model for inference.
2. **Optimizer states** – some optimizers (like Adam) use EMA-like logic for gradient moments.
3. **Batch norm statistics** – often updated with EMA during training.

---

In your case, you were using EMA on the **loss curve** to decide whether training is stable. Your point was: *don't be fooled by a smooth EMA – if the window is too small, the noise is still there, and if you look at raw 10-step intervals, you'll see the jumps clearly.*

Does that clear it up? Want me to explain how to choose the right EMA window for your use case?