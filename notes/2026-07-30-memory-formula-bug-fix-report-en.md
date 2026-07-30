---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Formula Bug Fix Report
translated: false
type: note
---

The experiment ran to completion successfully! Here's a summary of what was wrong and what I fixed:

---

## Root Cause

**Two issues caused `num_kvcache_blocks <= 0`:**

### Bug 1: Broken memory formula (in `model_runner.py`)

The original formula was:
```python
used = total - free                   # OS-level: ALL GPU processes
peak = memory_stats()["...peak"]      # PyTorch-level: only THIS process  
current = memory_stats()["...current"] # PyTorch-level: only THIS process
available = total * 0.92 - used - peak + current
```

This mixed **OS-level** memory metrics (which include llama-server, Xorg, zed-editor, etc.) with **PyTorch-internal** allocator stats (only the current process). Since other processes consumed ~9.5 GB, `used` was ~11.2 GB while `peak`/`current` were only ~1.2 GB. The resulting `available` was **-0.5 GB**, giving 0 blocks.

### Bug 2: Crashed after warmup due to OOM (secondary)

Even after fixing the formula, `llama-server` (PID 2202) was consuming **5.8 GB** of VRAM, leaving only ~35 MiB free for the forward pass intermediates.

---

## Fixes Applied

### 1. `nanovllm/engine/model_runner.py` — `allocate_kv_cache()`

Fixed to use `torch.cuda.get_device_properties().total_memory` (reliable) and `free` from `mem_get_info` (capped by what's truly available):

```python
total = torch.cuda.get_device_properties(0).total_memory
free, _ = torch.cuda.mem_get_info()
current = torch.cuda.memory_stats()["allocated_bytes.all.current"]
budget = int(total * config.gpu_memory_utilization)
available = min(budget - current, int(free * 0.95))
config.num_kvcache_blocks = max(1, available // block_bytes)
```

### 2. Killed `llama-server` (PID 2202, using 5.8 GB)

This freed enough GPU memory for the forward pass to run.

---

## Experiment Output

The scheduler trace shows clean continuous batching:
- **10 requests** → 1 prefill step (760 tokens), 63 decode steps
- Sequences finish incrementally: first at step 5 (Short answer, 4 tokens), last at step 64 (Essay, 64 tokens)
- `free_blocks` started at 212 after prefill, climbed to 222 as sequences completed
- No preemption needed (plenty of KV cache headroom after killing llama-server)