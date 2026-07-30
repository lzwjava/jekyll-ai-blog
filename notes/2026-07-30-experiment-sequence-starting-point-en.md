---
audio: false
generated: true
image: false
lang: en
layout: post
title: Experiment Sequence Starting Point
translated: false
type: note
---

## Which experiment to run first

The experiments are designed sequentially — but per the project notes, the star is **Experiment 4**. Here's the recommended order:

### 🥇 Start with **Experiment 4** — *Scheduler Watch*

```bash
cd /mnt/data/nano-vllm
python3.12 experiments/04_scheduler_watch.py
```

This is described as **"the 'loss curve moment' for inference systems"** — the single most important experiment. You watch continuous batching happen in real time: 10 requests start together, then progressively finish and leave the batch. It's the core vLLM insight made visible.

### After that, follow this order for the full picture:

| # | Experiment | Why |
|---|-----------|-----|
| **4** | `04_scheduler_watch.py` ⭐ | See continuous batching with your own eyes |
| **1** | `01_input_length.py` | Understand prefill (compute-bound) vs decode (memory-bound) |
| **2** | `02_generation_length.py` | See KV cache grow and slow down decode |
| **3** | `03_batch_scaling.py` | See why batching helps but also creates problems |
| **5** | `05_kv_cache_pressure.py` | See what happens when KV cache runs out (preemption) |
| **6** | `06_config_sweep.py` | Tune the trade-off knobs |
| **7** | `07_mixed_length_batch.py` ⭐ | See why continuous batching beats static batching 10x |

### Commands for any experiment

```bash
cd /mnt/data/nano-vllm
python3.12 experiments/04_scheduler_watch.py   # Start here
python3.12 experiments/07_mixed_length_batch.py # Also starred
python3.12 experiments/01_input_length.py       # Then fundamentals
# ... etc
```

> **Important:** Always use `python3.12` (not `python3`). The system `python3` is 3.14.3 which is outside nano-vllm's supported range (`>=3.10,<3.13`).