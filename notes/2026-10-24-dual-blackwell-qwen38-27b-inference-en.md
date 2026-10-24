---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dual Blackwell Qwen3.8-27B Inference
translated: false
type: note
---

This repo is a high-performance inference stack for serving **Qwen3.8-27B** (NVFP4 4-bit weights) across **two heterogeneous Blackwell GPUs** — an RTX PRO 6000 (96 GB, `GPU0`) and an RTX PRO 5000 (72 GB, `GPU1`) — exposing an OpenAI-compatible endpoint. It was a 4-commit project, and "what it actually did" is a deep performance-engineering exercise. Concretely:

**1. Two-server + adaptive router deployment** (`router/adapd.py`, `scripts/duo.sh`)

- Two patched vLLM 0.30.0 servers (one per card) behind a custom async router on port 8090.
- **Session homing** (`--home`): each agent session is pinned to one card so its KV cache / GDN state stays warm across turns (what makes follow-ups 2.2–2.6 s instead of re-prefilling).
- **Adaptive P/D split over NIXL** (`--home-split` / default): a long cold prefill can run on *one* card, then the KV (+ GDN state) is pushed over NIXL (UCX, cuda ipc, ~13 GB/s measured) to the other card for decoding. Short requests stay aggregated.
- Cost-model routing with per-card constants, prefix-cache tracking via chained message hashes, seat/KV-fill accounting, and a `GET /router/state` live view.

**2. Custom sm_120a CUDA kernels** (`kernels/`, JIT-built with CUDA 13)

- `fp8attn` — FP8 tensor-core paged extend attention (prefill), 496 lines with a long "v13b / v13 / v10h / v10g..." version history.
- `fp4_gemv` — NVFP4 GEMV for small M (decode / MTP verify), exact-by-construction numerics.
- `gdn_defer` — deferred Mamba/GDN state writes for speculative decoding.
- Decode-fused argmax for the MTP drafter.

**3. Latency-aware scheduler** (`vllm/v1/core/sched/qwen38_sched.py`) to fix the stock-vLLM problem where one 256K prefill (~14 s) blocks all decodes: decodes first, prefill bounded to T_ADD per step when decodes are running, SRPT ordering, reserve tokens for waiting requests, chunk-alignment to the b12x extend cost sawtooth, and decode-starvation/prefill-share curve controls.

**4. Speculative decoding** — two layouts behind `duo.sh`:

- `apd`: DFlash2 W4A16 drafter (k=7) + KV transfer, target-cache 2.5× offload.
- `home`: MTP drafter (k=4) with a pruned 98304-token draft vocab built by the `tools/`.

**5. Claude-API-style thinking budgets on top of vLLM** — reasoning-effort tiers, chain-of-thought privacy scrubbing, hard thinking caps per tier, answer-room reservation, and session compaction — i.e., it made vLLM behave like the API semantics of a proprietary agent platform.

**Bottom line**: it's a validation/harness repo proving that one quantized 27B model can serve long-context (256K) agent workloads on two *cheap-ish* consumer Blackwell cards with near-interactive latency — worst-case cold start of a 224K session ≈ 70 s, follow-up turns 2.2–2.6 s, aggregate output ~376 tok/s for 10 concurrent sessions. The README's headline figures were clearly the deliverable.
