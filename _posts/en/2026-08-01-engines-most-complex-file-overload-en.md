---
audio: false
generated: true
image: false
lang: en
layout: post
title: Engine's Most Complex File Overload
translated: false
type: note
---

No uncommitted changes, so I can't tell what you were just looking at. Let me give you my read of the codebase so you can point me at the right thing.

**The most complex piece by far is `nanovllm/engine/model_runner.py` (263 lines).** It crams in four independent subsystems:

| Complexity | Lines | What it does |
| --- | --- | --- |
| Tensor parallelism | ~70 | `dist.init_process_group` + `SharedMemory` RPC (`loop`/`read_shm`/`write_shm`), but default `tensor_parallel_size=1` |
| CUDA graphs | ~50 | `capture_cudagraph`, `graph_bs`, `graph.replay()`, graph pool — but `enforce_eager` skips it |
| KV cache math | ~20 | The budget/already-used/free×0.95 OOM juggling from your last commit |
| Prefix-cache prefill | ~60 | `prepare_prefill` with slot mappings, block tables, `cu_seqlens_k ≠ cu_seqlens_q` branching |

The engine (scheduler, block manager, sequence) is actually fairly clean already.

**Quick question — which one is "this"?** A few common targets:

1. **`model_runner.py` overall** → I'd simplify by deleting the two optional subsystems (TP and CUDA graphs) since they're ~120 lines of machinery that the default config never runs.
2. **The KV cache allocation** (your last commit) → can be reduced to ~6 lines: `blocks = int(free_after_weights * gpu_memory_utilization / block_bytes)`.
3. **The whole project** → different conversation; the experiments folder is where the "learn by running" value lives, so I'd keep that.

Which one did you mean? Or were you looking at something else entirely?
