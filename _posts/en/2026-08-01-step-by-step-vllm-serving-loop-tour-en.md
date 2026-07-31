---
audio: false
generated: true
image: false
lang: en
layout: post
title: Step-by-Step vLLM Serving Loop Tour
translated: false
type: note
---

Here's my recommended breakpoint tour. This codebase is a minimal vLLM clone, so the goal is to watch the **serving loop**: how a request flows through scheduling → KV cache allocation → model forward → token append, and how prefill and decode interleave (continuous batching).

Best run via the experiment that already drives the loop step-by-step (not the one-shot `run_inference.py`):

```bash
python3.12 experiments/04_scheduler_watch.py
```

It prints a scheduler trace with patched logging, which is the perfect scaffold for breakpoints.

---

## The tour (in this order)

### 1. The outer loop — see the whole pipeline first
- **`nanovllm/engine/llm_engine.py:66`** (`LLMEngine.step`) — *the* most important stop. The entire serving system is just this 4-line pipeline: `schedule → run → postprocess`. Put a breakpoint here and you'll see every phase fire per iteration.
- **`llm_engine.py:76`** (`generate`) — the main `while not self.is_finished()` loop that calls `step()`. Watch how `is_prefill`/`num_tokens` flip between prefill (positive) and decode (negative) steps.

### 2. The scheduler — the "continuous batching aha"
- **`nanovllm/engine/scheduler.py:27`** — prefill loop. Check `self.waiting` vs `self.running` deques, and `num_batched_tokens` accumulating.
- **`scheduler.py:46`** — `seq.num_scheduled_tokens = min(num_tokens, remaining)`. Watch a long prompt get **chunked** across steps when `max_num_batched_tokens` is exceeded (that's chunked prefill).
- **`scheduler.py:58`** — decode loop. This is where waiting seqs stop entering and running ones are picked, one token each (`num_scheduled_tokens = 1`, line 67).
- **`scheduler.py:60` / `preempt` (line 73)** — preemption, only fires when KV cache pressure is high. Run experiment `05_kv_cache_pressure.py` if you want to see it trigger.

### 3. KV cache block management — the PagedAttention core
- **`nanovllm/engine/block_manager.py:52`** (`can_allocate`) — prefix-cache hit detection (hash lookup) and the free-block count check.
- **`block_manager.py:69`** (`allocate`) — blocks are handed out for a sequence; note `seq.block_table` (logical→physical mapping). This is vLLM's anti-fragmentation trick — blocks need *not* be contiguous.
- **`block_manager.py:101` / `105`** (`can_append` / `may_append`) — the subtle "grow block table only when crossing a block boundary" logic (`len(seq) % block_size == 1`).
- **`block_manager.py:92`** (`deallocate`) — ref-counting and freeing on finish/preempt.

### 4. Tensor prep — the trickiest bookkeeping
- **`nanovllm/engine/model_runner.py:137`** (`prepare_prefill`) — inspect `slot_mapping` (flat KV slot index = `block_id * block_size + offset`), `cu_seqlens_q/k` (the variable-length batching encoding), and `block_tables`.
- **`model_runner.py:178`** (`prepare_decode`) — same idea for the 1-token decode case. This is where vLLM's per-sequence bookkeeping becomes tangible.

### 5. The moment KV is actually written/read
- **`nanovllm/layers/attention.py:158`** → `store_kvcache` (line 9) — see the KV cache write via `slot_mapping`.
- **`attention.py:194`** (`_decode_forward`) → `_gather_kv_from_cache` (line 35) — see the read: iterating `block_tables` to fetch past keys/values from physical blocks.
- Check `Sequence` fields (`num_cached_tokens`, `num_scheduled_tokens`) at these points — that's what makes the slicing work.

### 6. Closing the loop
- **`scheduler.py:79`** (`postprocess`) — token appended, EOS/max-length finish check, block deallocation, `running.remove`. Ends where the sequence began in `Sequence` (`sequence.py:24`).

---

**Watch expressions** worth having at stops 2–3: `seq.num_cached_tokens`, `seq.num_scheduled_tokens`, `seq.num_tokens`, `seq.block_table`, `len(self.block_manager.free_block_ids)`, and at stop 4: `seq.block_table[i] * self.block_size + offset`.

If you want an IDE-friendly path, `.idea/` is present (PyCharm), so you can set these as breakpoints in the GUI; for a quick CLI check, insert `breakpoint()` calls and step with `python3.12 experiments/04_scheduler_watch.py`. Note: `pdb`/stepping works fine since `experiments/04` drives the step loop on the main thread (the multiprocessing in `ModelRunner.__init__` is only for TP>1).