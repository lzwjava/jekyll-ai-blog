---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Memory Exhaustion by Llama-Server
translated: false
type: note
---

Yes — it's llama.cpp. PID 3148789 is `llama-server` running DeepSeek-R1-0528-Qwen3-8B (Q4_K_M) with `-ngl 99` (all layers on GPU), holding **10.6 GiB** of your 12 GiB RTX 4070. That leaves PyTorch with ~1 GB, which is why a 14 MiB allocation failed — the GPU was already nearly full before PyTorch started.

`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` won't help here. Fragmentation isn't the problem; another process owns the memory.

Options:

1. **Stop llama-server** if you don't need it: `kill 3148789`
2. **Run it on CPU/fewer layers** — drop `-ngl 99` to e.g. `-ngl 20` to share the GPU
3. **Use a smaller quant** — Q4_K_M of an 8B model is ~5 GB weights + KV cache; the rest is context. Lower `-c` (context size) to free memory
4. **Run PyTorch on CPU** — `device="cpu"` if the workload is small

Which one fits? If you want both running concurrently, option 2 or 3 is the answer.
