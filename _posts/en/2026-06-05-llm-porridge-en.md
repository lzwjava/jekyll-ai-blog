---
audio: false
generated: false
image: true
lang: en
layout: post
title: LLM Porridge — Simple Porridge Views the World
translated: false
---

Simple porridge, quick eat. This is surprisingly close to LLM training and inference with FlashAttention. You could say they are exactly the same in one key aspect.

To eat quickly, you need shallow plates laid out flat. When shallow plates can't hold enough, you need multiple shallow plates. This is the same logic as GPU tiles — bricks of compute.

![Porridge cooking in a rice cooker](/assets/images/porridge/p1.jpg)

Simple porridge views the world. Simple porridge views large language models. The great way is simple (大道至简).

![Three bowls of porridge on the table](/assets/images/porridge/p2.jpg)

## The Analogy

FlashAttention works by tiling the attention matrix into small blocks that fit in GPU SRAM — shallow plates, laid flat. Each tile (a GPU brick) processes a piece of the matrix without needing to materialize the full O(n²) attention matrix in HBM. When one tile isn't enough, you use multiple tiles in sequence. Same as porridge: one shallow plate can't hold a bowl of porridge, so you spread it across several.

<div style="text-align: center; margin: 1.5em 0;">
  <img src="/assets/images/porridge/p3.jpg" alt="FlashAttention infographic — tiling evolution" style="max-width: 100%; border-radius: 6px;" />
  <p style="font-size: 0.85em; color: #888; margin-top: 0.5em;">Image credit: from the internet</p>
</div>

## Clean Plate — Inference Successful

Clean plate. Token porridge grains successfully passed through shallow plates (GPU bricks) and into my stomach. Inference successful.

The only blemish: I used three plates instead of four. Can't do parallel computation.

![Clean plates — tokens consumed](/assets/images/porridge/p4.jpg)

Four plates would have meant four GPU tiles running in parallel — full utilization. Three plates means one tile sits idle. That's the difference between 75% and 100% hardware utilization. The porridge is eaten either way, but the throughput story changes.

The great way is simple: spread the work flat, use multiple tiles, consume everything. Porridge and transformers share the same wisdom.
