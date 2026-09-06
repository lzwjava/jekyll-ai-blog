---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distributed Speculative Decoding Codebase
translated: false
type: note
---

Here's a guided tour of the codebase:

## Architecture Overview

```
src/bloombee/
├── cli/            → Entry points (run_server.py, run_dht.py)
├── client/         → User-facing API for remote inference
├── server/         → The peer that hosts transformer layers
├── models/         → Model adapters (llama, qwen3, mixtral, falcon, gemma4, bloom + a template)
├── utils/          → Transport, microbatching, quantization, P2P glue
└── flexgen_utils/  → Tensor-offloading support (FlexGen-style)
```

### 1. Server side (`server/`) — a peer hosting layers
- **`server.py` / `backend.py` / `handler.py`** — the core: each peer loads a contiguous slice of transformer blocks and serves `forward`, `backward`, and `inference` (KV-cache step) requests over the DHT.
- **`block_functions.py`** — server-side computation on blocks; handles serialization, lossless compression, and microbatch slicing.
- **`microbatch.py`** — micro-batch pipelining (overlapping communication with computation).
- **`paged_kv.py`, `memory_cache.py`, `memory_cache_manager.py`** — KV cache management across stages.
- **`flexgen_tensor_parallel.py`** — tensor offloading so one GPU holds more layers.

### 2. Speculative decoding (`server/speculative_pruner/`) — the most interesting part
A pluggable strategy system built on `PrunerInterface` (ABC). During spec decoding, a peer sends a *tree* of draft tokens per round-trip; the pruner decides which branches to keep before they traverse the rest of the network:
- `simple_probability_pruner.py` — probability-based pruning
- `adaptive_neural_pruner.py` — a learned pruner
- `mid_layer_LM_head.py` + `lm_head_trainer.py` — a lightweight LM head attached mid-network to score drafts early
- `pruner_manager.py` / `pruner_factory.py` — wiring and selection

### 3. Client side (`client/`)
- `remote_sequential.py` — treats the whole P2P network like one `nn.Sequential` (autograd through the network via `sequential_autograd.py`)
- `remote_generation.py` / `inference_session.py` — token generation, maintaining a session across hops
- `routing/` — DHT-based discovery of which peer hosts which layers

### 4. Transport (`utils/lossless_transport.py`, `s2s_activation_quant.py`)
The lossless activation compression layer — serializes/deserializes tensors between peers, tracks compression ratios and profiles (`log_comp_ratio_event`, `transport_profile`).

**Typical request flow:** Client → discovers layer-hosting peers via DHT → sends hidden states (compressed) → each peer runs its slice + prunes spec-decode branches → passes activations to next peer → final peer runs LM head → tokens stream back.

Want me to dive deeper into any single piece — e.g., how the adaptive neural pruner works, or the microbatch pipelining logic?
