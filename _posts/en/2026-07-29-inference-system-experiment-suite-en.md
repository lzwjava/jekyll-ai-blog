---
audio: false
generated: true
image: false
lang: en
layout: post
title: Inference System Experiment Suite
translated: false
type: note
---

## Summary

I built a complete experiment suite (1,326 lines) that teaches inference systems through the same experimental loop as nanoGPT training. Here's what was created:

### Files Created

```
experiments/
├── _00_utils.py                # 194 lines — Timer, GPU memory, scheduler patching
├── 01_input_length.py          # 133 lines — Vary prompt length (4→2048 tok)
├── 02_generation_length.py     # 125 lines — Vary generation length (8→512 tok)
├── 03_batch_scaling.py         # 117 lines — Vary batch size (1→16)
├── 04_scheduler_watch.py       # 141 lines — ⭐ Watch continuous batching LIVE
├── 05_kv_cache_pressure.py     # 141 lines — KV cache exhaustion & preemption
├── 06_config_sweep.py          # 245 lines — Sweep gpu_mem, max_seqs, max_len
├── 07_mixed_length_batch.py    # 162 lines — ⭐ Mixed-length batching demo
├── README.md                   # Documentation & learning guide
└── run_all.sh                  # Orchestrator for all experiments
```

Plus a fix to `nanovllm/engine/llm_engine.py` to prevent atexit double-free.

### What You Learn

| Experiment | Key Insight |
|---|---|
| **01** Input Length | Prefill is compute-bound, decode is memory-bound. Decode gets slower with longer context because attention reads the entire KV cache. |
| **02** Generation Length | Decode latency increases as KV cache grows during generation. Total time scales linearly with max_tokens. |
| **03** Batch Scaling | Batching improves throughput but increases latency. This motivates **continuous batching**. |
| **04** Scheduler Watch ⭐ | You **watch** continuous batching: 10 sequences start together, short ones finish and leave early, the batch dynamically shrinks. |
| **05** KV Cache Pressure | When blocks run out, sequences are preempted (paused & restarted). Expensive! |
| **06** Config Sweep | `gpu_memory_utilization`, `max_num_seqs`, `max_model_len` interact to determine KV cache capacity. |
| **07** Mixed-Length ⭐ | 6 requests with wildly different lengths. Short Q&A finishes before Story has done 10 tokens. In static batching, short requests WAIT — in continuous batching, they don't. |

### The Core Discovery

Experiment 4's trace shows it perfectly:
```
Step 1:  PRE-FILL 10 seqs (760 tokens) — all arrive together
Step 2:  DECODE 10 seqs in parallel
Step 4:  FINISHED seq[6] (Short answer, 4 tokens) — leaves batch
Step 5:  9 seqs remaining
Step 7:  FINISHED seq[4] (Long context, 8 tokens) — leaves  
...
Step 64: FINISHED seq[7] (Essay, 64 tokens) — last one done
```

**This is why vLLM exists.** Static batching would have padded every sequence to the longest length. PagedAttention + continuous batching lets each sequence progress independently.

### How to Run

```bash
cd /mnt/data/nano-vllm
bash experiments/run_all.sh           # Runs all 7 experiments
# or individually:
python3 experiments/04_scheduler_watch.py   # ⭐ Start here
python3 experiments/07_mixed_length_batch.py # ⭐ Then this
```