---
audio: false
generated: true
image: false
lang: en
layout: post
title: Qwen3VL-2B CUDA Graph Manual Optimization
translated: false
type: note
---

Here's the project again with the URL:

**Project**: <https://github.com/AxonoOfficial/qwen3vl-2b-cudagraph-manual>

---

# Qwen3VL-2B CUDA Graph Manual Optimization

This is a **manual CUDA Graph optimization** for the [Qwen3VL-2B](https://huggingface.co/Qwen/Qwen3-VL-2B) vision-language model, built for the **IEEE AICAS 2026 Grand Challenge (VLM)**. The team placed **first runner-up**, and this V1 is the author's hand-crafted implementation.

## What it does

It replaces the HuggingFace `transformers` forward pass of Qwen3VL's **language model decoder** with **CUDA Graph capture/replay** — capturing the entire decoder computation graph once, then replaying it for each autoregressive decode step, bypassing Python's per-iteration overhead entirely.

## How it works (3 phases)

### 1️⃣ Graph Registration (`register_graph`)

For each "milestone" sequence length (e.g. 1200 tokens):

- Pre-allocates fixed-shape tensors (`position_ids`, `attention_mask`, `inputs_embeds`) as static CUDA buffers
- Creates an `ASStaticCache` (KV cache with `max_cache_len = milestone`)
- Runs one "pre-warmup" forward pass to initialize CUDA kernels
- Then wraps the entire `language_model.forward()` in a `torch.cuda.CUDAGraph` — capturing every kernel launch
- Stores `(graph, buffers, cache)` as a reusable pair

### 2️⃣ Decode-time replay (`Qwen3VLModel_Forward`)

- **First call (prefill)**: runs normally through the LM to establish the destination position
- **Subsequent decode tokens**: `AutoTensorLand` copies the real dynamic tensors (new token embedding, updated attention mask, position IDs) into the pre-allocated static buffers, then calls `graph.replay()` to execute the captured graph without Python dispatch overhead

### 3️⃣ Custom KV Cache (`ASStaticCache`)

Extends HuggingFace's `StaticCache` with:

- A `reset()` that fills `cumulative_length` to `max_cache_len` (tricks the position-aware layers into correct behavior)
- An `update()` that slices KV states to only the `done` portion (`cache_position.shape[0]`) — critical because CUDA Graphs need fixed tensor shapes but the actual KV content grows each step

## Key optimizations

| Technique | Where |
| ----------- | ------- |
| **CUDA Graph capture/replay** | `register_graph()` → `graph.replay()` |
| **`channels_last_3d`** memory format | Vision patch embed Conv3d |
| **TF32 on matmul & cudnn** | `allow_tf32 = True` |
| **`cudnn.benchmark = True`** | Auto-tune convolution kernels |
| **Static pre-allocation** | All tensors allocated once at max sequence length |
| **Monkey-patching** | Replaces `Qwen3VLModel`, `Qwen3VLVisionModel`, `Qwen3VLForConditionalGeneration` methods at module level |

## Usage pattern (from README)

```python
# 1. Warmup — capture graphs at milestone lengths
for i in milestones:
    cache = model.model.register_graph(model, i)["cache"]

# 2. At inference time, select the right pre-captured cache
past_key_values = caches[find_idx(milestones, seq_len)]
past_key_values.reset()

# 3. Generate with graph-replayed decode steps
model.generate = add_last_past_keys(model.generate)
```

## Why it matters

Autoregressive LLM decoding runs the same forward pass shape for every output token. Without CUDA Graphs, each step pays Python overhead (PyTorch autograd, dynamic dispatch, tensor allocation). By capturing and replaying a static graph, the GPU kernel launches are essentially free — the throughput gain is largest at small batch sizes where kernel launch overhead dominates.

The V1 is rough (chunked prefill is partially implemented, commented-out `torch.compile` line), but it's an impressive manual optimization job from someone who clearly understands CUDA Graph internals.
