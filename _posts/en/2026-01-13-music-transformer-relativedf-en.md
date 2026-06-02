---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Music Transformer and Relative Self-Attention
translated: false
type: note
---

Question: What is Anna Huang's main idea in this video (<https://www.youtube.com/watch?v=5vcj8kSwBCY>), and what does she say?

Answer:

The video is a lecture from **Stanford CS224N: NLP with Deep Learning | Winter 2019 | Lecture 14 – Transformers and Self-Attention**. It is co-presented by Christopher Manning, Ashish Vaswani, and **Cheng-Zhi Anna Huang** (from Google/Magenta project).

Anna Huang's section focuses on applying **Transformer** and **self-attention** mechanisms beyond text, specifically to **music generation**. Her core idea is that **self-attention** (especially when enhanced with **relative attention**) excels at modeling **long-range dependencies** and **self-similarity** (repetitions and structures) in music, which traditional models like RNNs struggle with due to compressing distant information into fixed vectors.

Key points she discusses:

- **Raw representations in music**: She compares music to language, using symbolic MIDI-like sequences (note on/off events, time advances, velocity/dynamics) from piano performances instead of raw audio waveforms.

- **Limitations of prior models**: RNNs generate poor continuations that "wander off" and fail to repeat motifs accurately over long sequences (e.g., a Chopin fragment loses coherence). Standard Transformers improve this but still degrade beyond trained lengths.

- **Music Transformer with relative attention**: This is her key contribution (the "Music Transformer" paper). It uses **relative self-attention** to incorporate pairwise distance/relative positional information efficiently (reducing quadratic memory issues for long music sequences). This allows the model to:
  - Maintain motifs, repetitions, and overall structure over thousands of steps (e.g., generating coherent ~1-minute pieces).
  - Achieve better coherence and translational equivariance (relational patterns carry forward regardless of absolute position).
  - Visualize attention heads focusing directly on relevant past motifs, even distant ones.

- **Attention as a weighted average**: She explains self-attention as directly accessing and weighting any past context (cheap and powerful for music's repetitive nature), unlike RNNs' sequential bottleneck.

- **Relative vs. absolute positional encodings**: Standard sinusoids work but lack explicit relative structure; relative attention adds distance biases to attention logits, enabling periodicity and better handling of translational invariance (useful in music, images, etc.).

- **Demonstrations**: She plays audio samples showing RNN vs. standard Transformer vs. Music Transformer outputs, highlighting how the relative version sustains musical arcs, repetitions, and gaps far better.

- **Broader implications**: Relative attention helps with expressive timing, extends to images (Image Transformer), graphs, and other domains needing relational modeling.

In summary, Anna Huang argues that transformers, when augmented with relative attention, are particularly well-suited for generative music tasks because they can capture music's inherent self-similar, hierarchical, and long-distance repetitive structures more effectively than previous approaches.

References:

- [Stanford CS224N Lecture 14 video](https://www.youtube.com/watch?v=5vcj8kSwBCY)
- [Music Transformer paper (Huang et al., 2018)](https://arxiv.org/abs/1809.04281) (her main work referenced in the talk)
