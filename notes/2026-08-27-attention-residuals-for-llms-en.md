---
audio: false
generated: true
image: false
lang: en
layout: post
title: Attention Residuals for LLMs
translated: false
type: note
---

**Question:** What is AttnRes (Attention Residuals) in the context of LLMs?

---

**Answer:**

**AttnRes** stands for **Attention Residuals**, a novel architectural upgrade to the standard residual connections used in Transformer-based LLMs, proposed by the **Kimi team at Moonshot AI** (March 2026).

---

### The Problem: Standard Residual Connections

In modern LLMs with PreNorm architectures, residual connections work by simply summing all previous layer outputs with **fixed unit weights (all = 1)**:

```
h_l = h_{l-1} + f_l(h_{l-1})
```

As network depth grows, this causes two problems: **feature dilution**, where each layer's relative contribution to the accumulated sum diminishes, and **unbounded magnitude growth**, a well-known issue in PreNorm Transformers.

---

### The Solution: AttnRes

AttnRes replaces this fixed accumulation with **softmax attention over preceding layer outputs**, allowing each layer to selectively aggregate earlier representations with learned, input-dependent weights.

Think of it this way: just as the Transformer revolution replaced the sequential recurrence of RNNs with attention across time (the sequence), AttnRes replaces the additive recurrence of residuals with **attention across depth**.

---

### Two Variants

**Full AttnRes** keeps the embedding and every earlier sublayer output. This list grows with model depth.

**Block AttnRes** (the practical variant) addresses memory concerns by partitioning layers into blocks: within each block, standard residuals are used, and between blocks, attention-based aggregation is applied. This reduces memory while recovering most of Full AttnRes's gains.

For `L` sublayers grouped into `N` blocks, the storage per token goes from `O(Ld)` to `O(Nd)`. The large experiments use about eight blocks.

---

### Key Design Choice

A key design choice shared by both variants is **zero-initialization of all pseudo-queries**, which causes the mechanism to start as uniform averaging and gradually specialize during training.

---

### Results

The Attention Residuals paper reports consistent (but modest) improvements in validation loss and downstream performance, with about **4% in training cost** and **2% in inference cost** overhead.

---

**References:**

- [Attention Residuals — Technical Report (Kimi / Moonshot AI)](https://arxiv.org/pdf/2603.15031)
- [Sebastian Raschka: Attention Residuals (AttnRes)](https://sebastianraschka.com/llm-architecture-gallery/attention-residuals/)
- [HuggingFace Paper Page](https://huggingface.co/papers/2603.15031)
- [Beyond the "Gradient Highway" — Substack](https://kenhuangus.substack.com/p/beyond-the-gradient-highway-how-attention)
