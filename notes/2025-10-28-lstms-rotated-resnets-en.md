---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: LSTMs Were Just Rotated ResNets
translated: false
type: note
---

In his NeurIPS 2024 Test of Time award talk on the 2014 "Sequence to Sequence Learning with Neural Networks" paper, Ilya Sutskever reflected on key insights and missteps from that era. One major point he addressed under "what we got wrong" was the overcomplication and eventual limitations of LSTMs (Long Short-Term Memory networks), which powered early sequence modeling breakthroughs like machine translation.

### The Core Misconception About LSTMs
We treated LSTMs as a fundamentally novel, intricate architecture tailored specifically for sequential data—something "special" that deep learning researchers had to painstakingly engineer to handle time dependencies, vanishing gradients, and recurrence. In reality, Sutskever explained, LSTMs were far simpler than that: **they're essentially a ResNet (Residual Network) rotated 90 degrees**.

- **ResNets** (introduced in 2015) revolutionized image processing by adding skip connections (residuals) that let information flow directly across layers, enabling much deeper networks without training instability.
- LSTMs (from 1997) did something analogous but in the *temporal dimension*: their gates and cell state act like residuals, allowing gradients and information to propagate over long sequences without fading. It's the same principle—just "rotated" from spatial stacking (e.g., pixels in an image) to temporal stacking (e.g., words in a sentence).

Sutskever quipped: "To those unfamiliar, an LSTM is something that poor deep learning researchers did before Transformers. It’s basically a ResNet but rotated by 90 degrees... And it came before; it's like a slightly more complex ResNet, with an integrator and some multiplications." This analogy underscores that LSTMs weren't a radical departure; they were an early, elegant application of residual ideas to recurrence.

### Why This Mattered (and What Went Wrong)
- **What worked brilliantly**: LSTMs scaled surprisingly well for their time, enabling the seq2seq model to beat traditional statistical methods on translation tasks. The residuals made deep recurrent nets trainable, much like they did for feedforward nets later.
- **What we got wrong (and why LSTMs faded)**: We underestimated how the sequential nature of LSTMs would bottleneck scaling. Unlike parallelizable ResNets or Transformers, LSTMs process data step-by-step, making them inefficient for massive datasets or long contexts. They also added unnecessary complexity (e.g., multiple gates) that attention mechanisms in Transformers simplified away. By 2017, Transformers exposed these limits, shifting focus to self-attention for better parallelism and longer-range dependencies.

In hindsight, the "wrong" part wasn't inventing LSTMs—they were a heroic interim solution—but clinging to them as the endgame for sequences instead of recognizing residuals as a general tool and pushing toward more parallel architectures sooner.

This perspective reframes LSTMs not as a relic, but as a foundational step in understanding how skip connections unlock depth across dimensions.

[Sequence to Sequence Learning with Neural Networks: What a Decade – Transcript & Video](https://kingy.ai/news/sequence-to-sequence-learning-with-neural-networks-what-a-decade-transcript-video/)
[Ilya Sutskever NeurIPS 2024 full talk](https://www.youtube.com/watch?v=1yvBqasHLZs)
[Reflections from Ilya's Full Talk at NeurIPS 2024](https://dlyog.com/papers/one_internet_v1)
