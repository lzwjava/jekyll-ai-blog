---
audio: false
generated: true
image: false
lang: en
layout: post
title: One-Layer Trick for LLMs
translated: false
type: note
---

It's **AirLLM** — a trick for running huge LLMs on tiny GPUs without quantization/distillation/pruning. Here's the core idea from the code (`air_llm/airllm/airllm_base.py`):

## The one-layer trick

A 70B model's memory problem is that you'd normally load all 70B parameters onto the GPU. AirLLM instead **only keeps one layer on the GPU at a time**, so VRAM needed ≈ size of *one layer*, not the whole model. That's how 671B DeepSeek-V3 runs on ~12GB and Kimi K3 (2.8T) on <4GB.

The mechanism has four pieces:

**1. Shard the checkpoint per-layer on disk first** (`utils.split_and_save_layers`) — the original weights file is decomposed into one shard per layer and cached. This is the disk-hungry step the README warns about.

**2. Instantiate the model on the `meta` device** — `init_empty_weights()` builds the full transformers model with all parameter *shapes* but zero memory. The model is real "code-wise" (owns all attention/rotary/generation logic), just weight-less.

**3. Stream weights with forward hooks**:

- Every big module (embedding → each decoder layer → final norm → lm_head) gets a pre-hook and post-hook.
- **Pre-hook**: load that layer's shard from disk → GPU, right before it runs.
- **Post-hook**: move its weights back to `meta` and call `clean_memory()` as soon as it's done.
- **Prefetching**: a worker thread loads the *next* layer while the current one computes, overlapping disk I/O with math (~10% speedup).

**4. Per-expert streaming for MoE models** (`_setup_expert_streaming`) — the big recent win. A sparse MoE layer (DeepSeek, Kimi K3) holds hundreds of experts but each token only routes to a handful. Since transformers calls each selected expert as its own module, AirLLM hooks *individual experts* and loads only the ones that actually run — so a K3 layer is ~55GB expanded but a token touches ~1GB. VRAM drops to *one expert's* size.

## Extras

- **Compression**: optional bitsandbytes 4bit/8bit for on-disk shards; FP8/MXFP4 pre-quantized checkpoints stream the *packed* bytes to the GPU (4x less PCIe traffic) and decompress there.
- **AutoModel** auto-detects architecture — most new models work the day they're released, because the forward pass is entirely delegated to transformers (`forward`/`generate` just call `self.model`).

**Trade-off**: you trade VRAM for speed — every layer is a disk→GPU round trip, so it's much slower than a normal full-memory inference. It's for hobbyist cards, not production throughput.
