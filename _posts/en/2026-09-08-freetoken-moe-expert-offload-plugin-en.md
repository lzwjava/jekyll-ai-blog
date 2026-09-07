---
audio: false
generated: true
image: false
lang: en
layout: post
title: FreeToken MoE Expert Offload Plugin
translated: false
type: note
---

This is a patch plugin for **FreeToken**, an LLM serving/inference engine. Below is a walkthrough of the project's logic, its Triton usage, and why both GLM-5.3 ("glm5_next") and DeepSeek-V4-Flash ("deepseek_v4") live in one repo.

## What the project fundamentally is

The hard problem this whole repo solves:

> Serve frontier-size MoE checkpoints on **one** 96 GB GPU (RTX PRO 6000 Blackwell), where the *experts alone* weigh 130–181 GB and live in host RAM. PCIe Gen5 (~50 GB/s) is the real bottleneck, not compute.

So everything here is about the **MoE expert offload cache**: a VRAM slot-cache of "hot" expert weights, with the rest pinned in host memory, fetched on demand over PCIe. The name of the game is reducing *bytes moved per token*, and keeping the GPU busy while bytes move.

FreeToken v0.1.2 (the baseline) already had DeepSeek-V4 support with this offload architecture. This repo is a set of **53 unified-diff patches + 19 new overlay files** that `install.sh` applies onto a clean upstream tree (`python/freetoken/...`), plus launch scripts in `examples/`. The repo deliberately contains *no upstream code*, only the deltas — hence `README.md` calls it a "patch plugin."

## Main logic

### 1. GLM-5.3-Flash model port (`overlay/freetoken/models/glm5_next/`)

This is the primary deliverable (see README headline). GLM-5.3-Flash is a 45-layer hybrid-attention MoE:

- **34 KDA layers** (`KdaAttention` in `attention.py`) — gated-delta linear attention (64 heads × 128 dim, short causal conv, lower-bounded forget gate, delta rule), computed via the upstream `fla` kernels `chunk_kda` / `fused_recurrent_kda`.
- **11 MLA + DSA layers** (`FullAttention = GlmMoeDsaAttention`) — Multi-head Latent Attention plus DeepSeek Sparse Attention with a Lightning indexer + k-pool compressor. Note MLA here is NoPE (`qk_rope_head_dim == 0`).
- **mHC (manifold-constrained Hyper-Connections)** — each decoder layer keeps *4 residual streams* (`hc_mult=4`, sinkhorn iters) and mixes them through per-sublayer matrices (`model.py: hc_pre/hc_post`, `hc_head` = unweighted mean). The knobs are identical to DSV4, so it **reuses the DSV4 hyper-connection kernels verbatim** — that's the first sign of why two models share this repo.
- **NVFP4 MoE** — 288 routed experts, top-8, sigmoid noaux_tc router, 1 shared expert, first 3 layers dense. Experts are ModelOpt-NVFP4 (packed uint8 + FP8 block-16 scales + fp32 global scales), 181 GB total.

### 2. The VRAM/host split — the heart of the decode path

`weight.py` decides where each expert layer lives:

- **Non-resident layers** (default 37 of 45) → their expert banks are *host-pinned*, and compute happens by fetching the chosen experts into a **VRAM slot cache** (LRU/LFU eviction), then running grouped Triton GEMM/GEMV.
- **Resident layers** (`experts_resident.py`, controlled by `FREETOKEN_GLM5_RESIDENT_LAYERS`, e.g. `3-6,8-11`) → full packed banks live on the GPU permanently; zero PCIe for them. Pick by measured fetch hotness (the miss curve is U-shaped).
- Everything non-expert that must stay dense runs on the GPU, optionally requantized to FP8 (`attention.py`/`mlp.py`, ~+28% decode).

Per decode step the flow is: router scores → top-8 expert ids → a **slot-cache "ensure" kernel** (see below) decides hits vs misses and picks eviction victims → H2D copies of missing experts run on a **side CUDA stream** → expert GEMMs wait on a copy event (`spec_prefetch.py` hides the copy under the next layers' work). The whole decode step is **CUDA-graph captured**, which is why every custom kernel must obey graph discipline: fixed shapes, no host sync, no host-side branches in the hot path.

### 3. Speculative expert prefetch (`overlay/freetoken/moe/spec_prefetch.py`)

Since routing is somewhat predictable, layer *L* runs layer *L+hop*'s real gate on its own hidden state, predicts the top-P experts, and warms the slot cache ahead of time — Mixtral-offloading style. Swept to P=4/hop-1. For GLM the routing is "flat" (low overlap between tokens' experts) which explains the concurrency ceiling: concurrent streams just add PCIe bytes.

### 4. Serving-level features

- **Radix/prefix KV cache** with content-hash keys for image spans (media prefix reuse), and a **KDA track-snapshot writer** so cached mid-prefill reuse points carry real recurrent state (a found-and-fixed correctness bug, documented in the README).
- **On-demand prefill** for short prompts (`FREETOKEN_PREFILL_ONDEMAND_TOKENS`): instead of streaming the whole prompt layer-by-layer, run it as one decode-style pass → TTFT 2.1 s → 0.59 s for 10 tokens.
- **Vision** tower port (0.6B ViT) + vendored HF-identical image preprocessing, env-gated off by default.
- Long-context stabilization for DSV4 (prefill chunk cap, sliced indexer top-k, staging slab) so 236K-token cold prefills don't OOM.

### 5. The DSV4 line is the same playbook, second model

`MANIFEST.md` "DeepSeek-V4-Flash (DSV4) line": native FP8/MXFP4 experts, 43 layers, DSA compressor/indexer + mHC, ~6000 experts resident at ~75 GB. Serving it on the same single GPU, same offload logic, went 51 → 64 tok/s via the same techniques (fused route, FP8 GEMVs, fused compressor decode step, rms-in-mix fusion). Both models can't run at once (the serve scripts stop each other's systemd service), so DSV4 and GLM5 are **two swappable workloads for one machine**.

## How Triton is used

Triton appears in exactly two roles: **(a) replacing multi-kernel eager chains with one fused kernel** (to cut launch overhead and intermediate memory traffic), and **(b) implementing cache/control-plane kernels that upstream only had in eager form or as cuBLAS**. All in `overlay/freetoken/kernel/triton/`:

| Kernel | What it fuses / replaces |
| --- | --- |
| `fused_route.py` | Router epilogue: sigmoid(or sqrt-softplus)+bias+**top-k+renorm+scale** (~8 launches × ~40 MoE layers/step → 1 kernel). Iterative `tl.argmax` with first-index tie-break to match `torch.topk` semantics exactly. |
| `kda_gate.py` | KDA forget/input gate math (5 GEMVs + ~7 elementwise → 2 GEMVs + 1 fused elementwise kernel). |
| `dsv4/hc_norm.py` | mHC pre-norm: fp32 cast + sum-of-squares + rsqrt in one CTA-per-token kernel, and the mix GEMV with the rsqrt folded into the epilogue (no atomics → deterministic). |
| `dsv4/comp_step.py` | DSV4's fused compressor decode step — register roll of read/scatter/pool/promote/write in one launch per tier instance, tile-loaded pool rows (was a 52 µs serial load chain). |
| `dsv4/hc_fused.py` | mHC pre-mix rms folded into the mix GEMV. |
| `kda_gate.py`, `fused_route.py` (ACT constexpr) | shared across both models where the math matches. |

Plus the patch set adds GPU-side cache-control kernels such as the LFU admission kernel (`lfu_ensure.py` — saturating 3-bit frequency counters + `(freq<<48)|usage` composite keys, single-CTA register-resident scan over ~3000 slots, with a periodic halving decay sweep) and tweaks to upstream `lru_ensure`/`fast_index_copy` (device-side H2D slot copy plans).

Recurring design constraints visible in every kernel docstring:

- **Deterministic**: no atomics where possible (run-to-run reproducible vs the cublas chain it replaces);
- **Numerics-bit-compatible**: sigmoid/topk rounding must match ATen within ≤1 ulp — this repo's quality bar is *token-for-token* equality with the HuggingFace reference (48/48 steps), so kernels are validated against the eager path's rounding order;
- **CUDA-graph-safe**: fixed shapes, no host sync, no unpinned host→device copies inside capture; device buffers that are *refreshed* each replay (e.g. `decode_memo` for the one `idx.long()` cast shared across all 34 KDA layers);
- **Auto-fallback**: e.g. the b12x (cuBLAS) MoE path is rejected for GLM because its epilogue lacks the swiglu clamp; the engine auto-resolves to the Triton path.

## Why two models in one repo?

1. **DSV4 was the template.** FreeToken upstream shipped DeepSeek-V4-Flash with exactly the machinery GLM-5.3 needs: mHC hyper-connections, MLA + DSA sparse attention, a linear-attention state pool, quantized-expert offload banks. GLM-5.3-Flash is structurally near-identical (mHC with the *same* `hc_mult=4`/sinkhorn knobs, hybrid KDA/MLA-DSA attention, dense head layers + MoE tail, FP8-class expert quantization). The overlay is full of "reuse map" comments: GLM-5.3 reuses DSV4's hc kernels, GLM's full-attention layers *are* the upstream `glm_moe_dsa` attention verbatim, and the DSA/MLA KV pool serves GLM unchanged. Porting GLM therefore meant writing mostly a weight-loader + glue, not engine code.

2. **Same hardware problem, same box.** Both are "hundreds of GB of experts on one 96 GB card with host offload" workloads. All the core optimizations (fused route, resident-layer split, speculative prefetch, FP8 decode, radix/prefix cache, chunked prefill) apply to both, and many kernels are literally shared (`fused_route.py` handles both the GLM sigmoid flavor and DSV4's sqrt-softplus via a constexpr `ACT`). The machine runs both — `serve_full.sh` (glm5-flash) and `serve_dsv4.sh` (dsv4-flash) are two mutually-exclusive systemd services for the same GPU.

3. **Different optimization maturity, one artifact.** The README/MANIFEST headline is the GLM-5.3 adaptation (the git history only starts at DSV4 round 3, so the GLM work predates the repo snapshot); the DSV4 line then became a second, faster-moving optimization track (55 → 64 tok/s, then deep-context stabilization). Keeping both models in the patch set means the authors serve whichever model a request targets without reworking the tree, and every kernel improvement in one line is measured for the other.

Net: **DSV4 gives the project a proven, byte-billing-aware offload architecture to copy; GLM-5.3 is the flagship port that exercises it; the repo ships both because they share ~80% of the machinery and the same single-GPU hardware reality.**
