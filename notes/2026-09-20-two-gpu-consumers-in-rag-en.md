---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two GPU Consumers in RAG
translated: false
type: note
---

## How `rag/` uses the GPU

There are exactly **two** GPU consumers in this codebase, and neither of them is the retrieval math.

**1. Embedding model (`build_index.py` + `retriever.py`)**
- `build_index.py` → `load_encoder()` (`retriever.py:239`) calls `SentenceTransformer(model, device=device)`. `--device` defaults to `None`, so sentence-transformers auto-selects `cuda:0` when available (the probe log confirms `dim=1024, device=cuda:0`).
- Runs in **fp32** (no `model.half()`), with `--batch-size 32`. `--fp16` only controls the dtype written to `embeddings.npy`, not the compute dtype.
- Measured on the RTX 4070 (`logs/probe_bge_m3.log`): **63–67 chunks/s** with bge-m3, batch 32. The full 186,263-chunk build would be ~**50 min** of GPU time.
- At query time, `Retriever.encode_query()` lazily loads the *same* encoder onto the GPU and embeds one query.

**2. Answer generation (`rag_chat.py`)**
- `--backend llama` (default): llama.cpp loads `lzw-notes-merged.Q4_K_M.gguf` (2.5 GB) with `--n-gpu-layers -1` → **all** layers on GPU.
- `--backend hf`: `AutoModelForCausalLM.from_pretrained(..., torch_dtype=bfloat16, device_map="auto")` → whole Qwen3-4B in bf16 (~8 GB) on GPU.
- `--backend vllm`: `gpu_memory_utilization=0.85`.

**Not on GPU:**
- Dense search is `faiss.IndexFlatIP` from **`faiss-cpu` 1.15.1** (`has_gpu=False`), plus a NumPy fallback — both CPU. BM25 is pure NumPy CPU too.
- The index itself (`embeddings.npy` 286 MB, `index.faiss` 286 MB, `chunks.jsonl` 294 MB) lives in **system RAM**, not VRAM. `Retriever.__init__` parses all 186k JSON records into a Python list of dicts — that's the real host-RAM cost (~1–1.5 GB heap).

## What VRAM usage depends on

| Component | Depends on | Current numbers |
|---|---|---|
| Embedding weights | model × dtype | e5-small 118M → **0.47 GB** fp32; bge-m3 568M → **2.27 GB** fp32 (4.3 GB cache dir includes a duplicate `pytorch_model.bin`) |
| Embedding activations | batch × seq_len × hidden × depth | chunks avg 458 chars ⇒ short; batch 32 ⇒ few hundred MB (bge-m3 fp32 peak ≈ 2.5–3.5 GB) |
| LLM weights | params × quant | Qwen3-4B Q4_K_M = **2.5 GB**; bf16 HF = **~8 GB** |
| KV cache | `2 × layers × kv_heads × head_dim × ctx × 2 B` | 36 × 8 × 128 ⇒ **144 KiB/token** ⇒ 1.2 GB @ 8k, 2.4 GB @ 16k, 6 GB @ 40k |
| Compute buffers / overhead | backend | llama.cpp ~0.5–1 GB; vLLM reserves 85% of the card |
| Co-residency | both models loaded at once | e5 0.5 **+** LLM ~4.5 ≈ **5 GB**; bge-m3 2.5 **+** LLM ≈ **7–8 GB** |

So VRAM ≈ `embedding_weights + embedding_activations + llm_weights + kv_cache(ctx) + buffers`. The two knobs that move it most are **`--ctx`** (linear in KV cache) and **`--batch-size`** (activations during indexing). That's why the README's target is 12 GB — current `nvidia-smi` shows 8.2 GB used, with only ~3.2 GB free.

## Does a more powerful GPU help?

Yes, but only for the two GPU stages — and by very different amounts:

- **Index build: scales ~linearly.** 63 chunks/s on a 4070 → a 4090 (~2× bandwidth/compute) ≈ 2×, H200 ≈ 4–6×. You must raise `--batch-size` (64–128) to keep a bigger card saturated. Switching to `intfloat/multilingual-e5-small` is a bigger, cheaper win (~5×, per the README) than a GPU upgrade.
- **Generation: the real payoff.** Single-stream decode of a 4B Q4 model is memory-bandwidth-bound (2.5 GB read/token): 4070 = 504 GB/s, 4090 ≈ 1 TB/s, H100/H200 ≈ 3.35–4.8 TB/s. Expect roughly 2× / 4–6× faster tokens/s, plus prefill (compute-bound) scaling even better. A big GPU also makes `--backend vllm` worthwhile for concurrent users via continuous batching.
- **Retrieval: almost no benefit.** `IndexFlatIP` over 186k × 384 dims is 71M MACs — ~10–30 ms on CPU, already far below the LLM latency. Throwing a bigger GPU at it is pointless; if you ever care, install `faiss-gpu` (a 1–2 ms saving) or switch to IVF/HNSW at millions of chunks. The GPU's only retrieval role is embedding the single query (~10–30 ms).

**Bottom line:** for single-query interactive use, ~90%+ of latency is the LLM, so a faster GPU speeds up answers roughly in proportion to memory bandwidth. For the offline index build, a faster GPU helps linearly, but a smaller/faster embedding model or fp16 compute is a better lever than raw hardware.