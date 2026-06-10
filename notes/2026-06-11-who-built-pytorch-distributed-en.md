---
audio: false
generated: true
image: false
lang: en
layout: post
title: Who Built PyTorch Distributed
translated: false
type: note
---

**Question:** Is Andrew Tulloch the person behind PyTorch's distributed training module (`torch.distributed`), or was it built by others?

**Answer:**

Short version: **not Tulloch**. He's a PyTorch ecosystem legend, but `torch.distributed` / DDP was built by a different group at Meta.

### Who actually built `torch.distributed` / DDP

The canonical reference is the VLDB 2020 paper *PyTorch Distributed: Experiences on Accelerating Data Parallel Training* (arXiv:2006.15704). The author list is Shen Li, Yanli Zhao, Rohan Varma, Omkar Salpekar, Pieter Noordhuis, Teng Li, Adam Paszke, Jeff Smith, Brian Vaughan, Pritam Damania, and Soumith Chintala. Tulloch is not on it. The key names to know:

- **Shen Li (mrshenli)** — lead author of the DDP paper and author of the official PyTorch Distributed Overview and DDP tutorials. If one person is "the DDP person," it's him. The core trick in DDP — registering autograd post-hooks on `AccumulateGrad` nodes, bucketing gradients, and overlapping `AllReduce` with the backward pass via the C++ `Reducer` — is his team's design.
- **Pieter Noordhuis** — built **Gloo**, the collective-communication backend, and much of early `torch.distributed` plumbing (he later co-authored the famous "Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour" paper — which, interestingly, Tulloch *was* a co-author on).
- **Yanli Zhao, Rohan Varma, Wanchao Liang, Pritam Damania** — DDP internals, RPC framework, and later **FSDP** (Yanli Zhao is first author on the FSDP paper, arXiv:2304.11277). Wanchao Liang went on to lead **DTensor** and **torchtitan**.
- **Soumith Chintala, Adam Paszke, Sam Gross, Gregory Chanan** — PyTorch core itself (autograd, tensor library), on top of which distributed sits.

### So what is Tulloch known for?

Adjacent but different territory — **performance and inference infrastructure**, not the distributed training APIs:

- Low-level, hardware-aware optimizations across PyTorch, Caffe2, TVM and FBGEMM — C and CUDA speedups in torch/nn, quantized inference kernels, plus NNPACK/ARM NEON work for mobile inference.
- Contributions to PyTorch and the FBGEMM library for efficient matrix operations — FBGEMM is the int8 quantized GEMM backend that powers a lot of Meta's CPU inference and DLRM training.
- He *did* co-author distributed-systems-adjacent work like the ZionEX paper on high-performance distributed training of 12-trillion-parameter DLRMs, with sharding algorithms for embedding tables and a PyTorch-based training stack supporting model and data parallelism — but that's a system built *on top of* `torch.distributed`/FBGEMM, not the module itself.
- Career arc: Distinguished Engineer at Meta from 2012, then OpenAI in 2023 where he worked on training GPT-4o, GPT-4.5, and o3, co-founded Thinking Machines Lab with Mira Murati, and in October 2025 departed Thinking Machines and rejoined Meta's TBD Lab — after a reported package of up to $1.5 billion over six years.

### Mental model for you

Since you're studying nanoGPT-scale training and DeepSeek-style MoE, map the names to the layers:

```
torch.distributed (c10d, ProcessGroup, NCCL/Gloo)  → Pieter Noordhuis, Teng Li
DDP (Reducer, bucketing, comm/compute overlap)      → Shen Li
FSDP (param sharding, ZeRO-3-style)                 → Yanli Zhao, Rohan Varma, Min Xu (fairscale)
DTensor / torchtitan (TP/PP/FSDP2 composition)      → Wanchao Liang
Kernels / quantization / inference perf (FBGEMM)    → Andrew Tulloch
```

If you want to read code, start with `torch/csrc/distributed/c10d/reducer.cpp` — that's the heart of Shen Li's DDP design (gradient buckets + autograd hooks + async AllReduce), and it's surprisingly readable.

**References:**

- [PyTorch Distributed: Experiences on Accelerating Data Parallel Training (arXiv:2006.15704)](https://arxiv.org/abs/2006.15704)
- [DDP paper, VLDB 2020 PDF](https://www.vldb.org/pvldb/vol13/p3005-li.pdf)
- [PyTorch DDP tutorial — Author: Shen Li](https://docs.pytorch.org/tutorials/intermediate/ddp_tutorial.html)
- [Reuters: Thinking Machines Lab co-founder Tulloch departs for Meta](https://in.tradingview.com/news/reuters.com,2025:newsml_L2N3VS042:0-thinking-machines-lab-co-founder-tulloch-departs-for-meta-wsj-reports)
