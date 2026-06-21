---
audio: false
generated: true
image: false
lang: en
layout: post
title: 10GB Code to GPT-2 Training
translated: false
type: note
---

Here's the full story:

---

COMPREHENSIVE SUMMARY: From 10GB Code Data to Training

== PHASE 1: TOKENIZATION=***

GOAL: Convert 38 parquet files (10.2 GB, github-code dataset) into nanoGPT binary format (.npy shards).

WHAT HAPPENED: Original script used `multiprocessing.Pool(16)`. Each worker loaded an entire parquet file via `pq.read_table()`, then accumulated tokens into a Python list before converting to numpy.

THE KILL: One parquet file produces ~369M tokens. A Python list of 369M ints = ~10 GB RAM (Python int overhead ~28 bytes each). 16 workers in parallel = 160+ GB RAM on a 62 GB machine. The kernel either OOM-killed workers or thrashed swap so hard that sshd couldn't even send its SSH banner — TCP port 22 accepted connections but hung during banner exchange. Required physical reboot.

THE FIX: Rewrote the script with three changes:
1. Single process — no multiprocessing at all
2. Streaming parquet reads via `pq.ParquetFile.iter_batches(batch_size=8192)` instead of loading entire files
3. Direct numpy uint16 accumulation — pre-allocated 200MB buffer, no Python list intermediate

RESULT: 141 shards, ~14.07B tokens, 27 GB output, 41 minutes, peak RAM ~600 MB.

== PHASE 2: TRAINING SETUP ==

AVAILABLE INFRASTRUCTURE:
- RTX 4070 (12 GB VRAM), 62 GB system RAM
- nanoGPT already installed at /mnt/data/nanoGPT with PyTorch 2.10 + CUDA 12.8
- Existing configs: 760M model (for MI300X 192GB), 124M model, etc.

== PHASE 3: CHOOSING MODEL SIZE ==

WHY GPT-2 124M (not 760M or 350M):

The 760M config (n_layer=24, n_head=24, n_embd=1536) was designed for MI300X with 192 GB HBM3. RTX 4070 has 12 GB. Simple math:
- 760M params in fp16 = ~1.5 GB for model weights
- Optimizer states (Adam) = 2x model = ~3 GB
- Activations for batch_size=32, block_size=1024, 24 layers = 8-12 GB
- Total: 13-17 GB → doesn't fit in 12 GB

GPT-2 124M (n_layer=12, n_head=12, n_embd=768):
- Model weights in fp16 = ~250 MB
- Optimizer states = ~500 MB
- Activations = 2-4 GB depending on batch size
- Total: 3-5 GB → fits comfortably

Scaling law consideration: 14B tokens / 124M params = ~113 tokens per parameter. Chinchilla optimal is ~20 tokens/param, so this is actually over-trained in terms of data — which means better quality per parameter. Good use of the data.

== PHASE 4: SMOKE TEST ==

TEST 1 — batch_size=8, grad_accum=4:
Result: OOM. 10.37 GB in use, needed 1.54 GB more. The eval forward pass (logits for 50304 vocab × 1024 positions) was the culprit.

TEST 2 — batch_size=4, grad_accum=8:
Result: WORKED. Loss dropped 10.77 → 8.03 in 10 steps. ~700ms/step, MFU 12.83%.

Key observations from smoke test:
- Initial loss 10.77 is close to ln(50304) ≈ 10.83 — exactly what you'd expect for random initialization with 50304 vocab. Model is starting from scratch correctly.
- Loss dropped to 8.03 in just 10 steps — the model is learning from the code data immediately.
- MFU 12.83% without torch.compile — with compile=True, expect 2-3x improvement.

== PHASE 5: CONFIG DECISIONS ==

batch_size=4 (not 8):
Smoke test proved 8 doesn't fit. 4 fits with room for the forward/backward pass. Each micro-step processes 4 × 1024 = 4,096 tokens.

gradient_accumulation_steps=8 (not 4):
To keep effective batch size at 32,768 tokens/step (4096 × 8). This is a standard effective batch size for GPT-2 scale training — large enough for stable gradients, small enough for good learning dynamics.

block_size=1024:
Standard for GPT-2. Matches the context window of the model architecture. No reason to change.

learning_rate=6e-4 (not 3e-4):
The 760M config uses 3e-4. Smaller models can handle higher learning rates — this is standard scaling law practice. 6e-4 is the GPT-3 paper's LR for their 125M model.

min_lr=6e-5:
10% of peak LR. Standard cosine decay floor.

warmup_iters=2000:
Standard for this model size. Prevents early training instability.

max_iters=427000:
14B tokens / 32,768 tokens per step = ~427,000 steps. This consumes the entire dataset once. For pre-training from scratch, one epoch is standard (LLMs don't benefit much from multiple passes over the same data).

compile=True:
torch.compile fuses kernels and reduces overhead. Expect 2-3x speedup after initial compilation (~2-3 min). The smoke test warning "Not enough SMs to use max_autotune_gemm mode" is harmless — RTX 4070 has 46 SMs, fewer than the threshold for autotune, but compilation still helps.

== ESTIMATED TRAINING TIME ==

Without compile: ~700ms/step × 427,000 steps = ~83 hours (~3.5 days)
With compile (expected 2x): ~41 hours (~1.7 days)
With compile (optimistic 3x): ~28 hours (~1.2 days)

== WHAT TO WATCH FOR ==

- Loss should drop below 3.0 by ~100k steps
- If loss plateaus or spikes, check learning rate schedule
- Checkpoints save every 1000 steps to /mnt/data/nanoGPT/out-github-code-124m/
- To sample from the model during training: `python3 sample.py --out_dir=out-github-code-124m`
