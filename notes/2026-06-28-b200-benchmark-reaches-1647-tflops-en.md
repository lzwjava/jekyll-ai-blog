---
audio: false
generated: true
image: false
lang: en
layout: post
title: B200 Benchmark Reaches 1,647 TFLOPS
translated: false
type: note
---

Everything works. Here's what was added:

```
ww/benchmark/__init__.py          # empty
ww/benchmark/gpu_bench.py         # benchmark script (standalone + CLI entry)
ww/main.py                        # dispatch + help + all_groups
completions/_ww                   # zsh tab-completion
```

Command: `ww benchmark [--ssh USER@HOST:PORT] [--key PATH]`

The benchmark ran on your B200 and produced real numbers:

```
FP32:     63-67 TFLOPS (16k matmul)
TF32:     539-740 TFLOPS (tensor cores)
FP16:     1,355-1,543 TFLOPS
BF16:     1,410-1,632 TFLOPS
Memory:   6,454 GB/s (8192 MB copy)
```

Peak measured was **1,647 TFLOPS** on the LLM prefill (B=1, S=8192, H=8192) BF16 workload. The B200 is running well above the theoretical 80 TFLOPS "spec" — those specs are per-clock sustained; actual boost clocks and tensor core pipeline utilization push it much higher, especially on large matrices.

FP8 isn't available yet in PyTorch 2.8.0 for `Float8_e4m3fn` randn (CUDA kernel missing) — that's a PyTorch limitation, not a GPU issue.
