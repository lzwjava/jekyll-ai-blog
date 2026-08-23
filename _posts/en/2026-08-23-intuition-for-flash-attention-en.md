---
audio: false
generated: true
image: false
lang: en
layout: post
title: Intuition for Flash Attention
translated: false
type: note
---

Question: What is the intuition for Flash Attention?

Answer: Flash Attention is an algorithm that makes the attention mechanism in transformers dramatically faster and more memory-efficient by changing *how* we compute it — not *what* we compute. Here's the core insight:

**Standard attention has a memory bottleneck.** The naive approach computes the full N×N attention matrix (where N is sequence length), writes it to GPU memory (HBM — slow, far away), then reads it back for softmax, then reads it again to multiply by values. This repeated round-tripping to slow memory is the real bottleneck.

**Flash Attention stays in fast memory (SRAM).** Instead of computing the whole matrix at once, it tiles the computation into small blocks that fit in the GPU's fast on-chip SRAM (cache). It processes a block, keeps a running softmax correction factor, and fuses all the steps together — never writing the big N×N matrix to HBM at all.

The key trick is an **online softmax correction**: softmax requires knowing all scores to normalize, but Flash Attention uses a running max and running sum that get updated block by block. The final result is mathematically identical to standard attention — it's a pure implementation optimization.**The mental model in one sentence:** Standard attention is like doing your homework by writing every intermediate calculation on a whiteboard at the back of the room (HBM), walking back and forth each step; Flash Attention does the whole thing on a scratch pad at your desk (SRAM), only walking to the back once at the end.

Key things to internalize:
- The N×N matrix is never materialized in slow memory — this is the core win
- The **online softmax trick** is what makes tiling possible: you don't need to see all scores before normalizing, you just track a running correction factor
- Flash Attention 2 & 3 extended this with better parallelism across attention heads and sequence positions
