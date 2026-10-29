---
audio: false
generated: true
image: false
lang: en
layout: post
title: Modded-nanoGPT Training Tricks
translated: false
type: note
---

**Question:** What tricks does modded-nanoGPT use to train models?

**Answer:**

[Modded-nanoGPT](https://github.com/KellerJordan/modded-nanogpt) by Keller Jordan is a competitive "speedrun" benchmark — training a 124M GPT-style model to ≤3.28 val loss on FineWeb as fast as possible on 8×H100s. Starting from the llm.c baseline that took 45 minutes, it now reaches the same target in under 40 seconds using under 330M tokens. The tricks fall into several categories:

---

### 🏗️ Architecture

The core architectural changes include:
- **Rotary embeddings (RoPE)** replacing learned positional embeddings
- **QK-Norm** (normalizing queries and keys before dot product)
- **ReLU²** activation (squaring the ReLU output) instead of GELU
- **Untied head from embedding** — the LM head and token embedding matrices are separate weights (re-tied partway through later records)
- **U-net skip connections** — residual shortcuts from the embedding to every block, plus a direct skip from block 3 to block 6
- **Value embeddings** — extra learned embeddings mixed into the attention value vectors (inspired by Zhou et al. 2024)
- **Long-short sliding window attention** (inspired by Gemma 2), with a window size warmup schedule and YaRN for RoPE scaling
- **Smear module** — enables a 1-token "look-back" by smearing token embeddings forward one position
- **Sparse attention gate** — gates attention sparsely
- **Paired Head Attention** — Q and K matrices orthogonalized in pairs of heads rather than across all heads
- **Partial Key Offset**
- **Hashed bigram + trigram embedding table** (84.6M rows sharded across GPUs, with a sign trick)
- **MUDD skip connections** to the residual stream and attention values
- **Learnable XSA**
- **Lightweight Dynamically Composable MHA**
- **Depth reduction and mixed-width attention** (64-dim QK on most layers, half-width V on two layers)

---

### ⚙️ Optimizer

The headline optimizer is **Muon** (Momentum Orthogonalized by Newton-Schulz), applied to all linear layers. It works by taking the gradient, applying Nesterov momentum, then orthogonalizing the result via a quintic Newton-Schulz iteration — approximately replacing the update `G` with `U @ V.T` where `U, S, V = G.svd()`. For this training scenario it offers lower memory than Adam, ~1.5× better sample efficiency, and under 2% wall-clock overhead.

Later records layer on:

- **NorMuon** — a normalized variant of Muon
- **Polar Express** — a replacement for the Newton-Schulz orthogonalization step
- **Cautious Weight Decay** (with a schedule tied to the learning rate)
- **ANVIL optimizer** — a twin-rail (fast + slow) momentum variant with re-derived orthogonalization maps and cautious decay gated on the slow rail
- **Tail weight averaging (EMA)** with a raised LR floor
- **Batch size schedule** and **max sequence length schedule**

---

### 🔢 Precision / Numerics


- **FP8** for the LM head, MLP forward and backward passes, and QKV projections
- **Asymmetric logit rescale** and **logit softcapping** (lowered from 30 → 15 → asymmetric)
- **BFloat16 activations** and cross-entropy computation
- **Zero-init projections** (muP-style initialization of output projections to zero)

---

### 📐 Training Schedule Tricks


- Align training batch starts with **EoS tokens** and set a **max document length**
- **Gradient accumulation** for 2 steps for embedding and LM head before updating
- **Single activation input** for the last 3 attention layers
- **Multi-token prediction (MTP)** auxiliary loss
- **Prefix token prediction** auxiliary loss
- **Untie embed/lm_head at 2/3 of training**
- **Sampled softmax** over a shared candidate set for most of training
- **Sparse row-wise embedding updates** — only touched rows are exchanged and updated

---

### 🚀 Systems / Kernel Tricks


- **FlexAttention** (extending context from 1024 to 64K), then upgraded to **Flash Attention 3**
- **Overlap computation and gradient communication** (async gradient all-reduce → reduce scatter)
- **Fused Triton kernels** for ReLU², softcapped cross-entropy, QK-norm + RoPE + KeyOffset
- **CUDA-graph capture** of the entire training step including optimizer and FP8 weight refresh
- **Asynchronous data batch fetching**

---

The world record has fallen from 45 minutes all the way to under 40 seconds on 8×H100s, with each increment documented in the repo's world record table. It's a living benchmark where nearly every trick above was proven out by a real timing improvement.

**References:**
- [KellerJordan/modded-nanogpt (GitHub)](https://github.com/KellerJordan/modded-nanogpt)
- [Muon optimizer writeup](https://kellerjordan.github.io/posts/muon/)
- [World record history (wiki)](https://github.com/KellerJordan/modded-nanogpt/wiki)
