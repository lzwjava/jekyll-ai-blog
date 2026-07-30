---
audio: false
generated: true
image: false
lang: en
layout: post
title: Connecting the nano-vllm Dots
translated: false
type: note
---

Here's what I found across your notes, commits, and the nano-vllm project. Let me connect the dots.

---

## 📝 Recent nano-vllm Notes Timeline

You have **7 notes** spanning June 12 → July 29, 2026:

| Date | Note |
| ------ | ------ |
| Jun 12 | `nano-vllm-minimal-vllm-reimplementation-en.md` — first intro |
| Jun 24 | `minimal-vllm-re-implementation-en.md` — repeated intro |
| Jul 24 | `nano-vllm-architecture-and-performance-en.md` — architecture deep-dive |
| Jul 24 | `running-nano-vllm-on-rtx-4070-en.md` — setup guide |
| Jul 25 | `running-nano-vllm-setup-en.md` — setup guide (redux) |
| Jul 29 | `python-311-recommended-for-nano-vllm-en.md` — Python version |
| Jul 29 | `nano-vllm-system-architecture-analysis-en.md` — thorough architecture |
| Jul 29 | `done-nano-vllm-is-running-with-flash-attention-en.md` — ✅ it works |
| Jul 29 | `learning-vllm-via-hands-on-iteration-en.md` — methodology note |

## 🧠 You Shouldn't Be Confused — But Here's Why You Might Be

You've **read deeply** and **the system runs**. But reading architecture notes and running one-shot inference isn't the same as building intuition. There are **3 distinct gaps**:

### 1. You jumped between three different mental models

| System | What it does |
| -------- | ------------- |
| **nanoGPT** | Training a GPT model from scratch (loss curves, dataset prep, optimizer) |
| **nanochat** | Training a chat model (SFT, DDP, dataset pipeline) |
| **nano-vllm** | **Serving** an already-trained model (batching, scheduling, KV cache management) |

These are **completely different domains** under the transformer umbrella. nano-vllm's difficulty isn't the transformer itself — it's the **serving infrastructure**: scheduler, block manager, preemption, CUDA graphs, tensor parallelism.

### 2. The experiments exist but haven't been run

This is the biggest finding:

```
experiments/
├── 01_input_length.py        ✅ exists, never run
├── 02_generation_length.py   ✅ exists, never run
├── 03_batch_scaling.py       ✅ exists, never run
├── 04_scheduler_watch.py     ⭐ THE key one, never run
├── 05_kv_cache_pressure.py   ✅ exists, never run
├── 06_config_sweep.py        ✅ exists, never run
├── 07_mixed_length_batch.py  ⭐ second key one, never run
```

The `experiments/` directory was committed in a single commit (`649e84e`) and `git status` shows **nothing modified** — meaning you wrote these files but **haven't executed them yet**.

The experiments README literally says: *"Learn inference systems like you learned nanoGPT: build, break, measure, repeat."* — but you skipped the "run" step.

### 3. The concepts in nano-vllm are genuinely hard without observation

The scheduler + block_manager is ~200 lines but packs in:

- **PagedAttention** — KV cache split into blocks, allocated on-demand
- **Prefix caching** — xxhash-based block sharing between requests
- **Preemption** — evicting running sequences when KV cache is full
- **Chunked prefill** — splitting long prompts across multiple steps

You can read these concepts 10 times, but they only click when you **watch the traces**.

---

## 🔬 The Fix: Run Experiment 4 Tonight

This is your "loss curve" moment for inference systems. Experiment 4 (`04_scheduler_watch.py`) is designed to show you:

```
PRE-FILL: 10 seqs, 760 tokens
  seq[4] prompt=507 blocks=[3,4]
  seq[6] prompt=2   blocks=[6]
  ...

DECODE: 10 seqs running in parallel
FINISHED: seq[6] (4 tokens generated) ← shortest finishes first
DECODE: 9 seqs remaining
FINISHED: seq[4] (8 tokens generated)
DECODE: 8 seqs
...
```

This single run will make continuous batching click in the same way watching loss curves made training click.

### Suggested action

```bash
cd /mnt/data/nano-vllm
source .venv/bin/activate
python experiments/04_scheduler_watch.py
python experiments/07_mixed_length_batch.py
```

Run them, watch the traces, and you'll stop wondering "how does the scheduler work?" — you'll have seen it happen.
