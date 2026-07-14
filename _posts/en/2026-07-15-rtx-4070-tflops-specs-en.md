---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 TFLOPS Specs
translated: false
type: note
---

Question: RTX 4070 TFLOPS?

Answer:

Base **RTX 4070** (5888 CUDA cores, AD104): FP32: 29.15 TFLOPS, FP16: 29.15 TFLOPS, BF16: 29.15 TFLOPS. Tensor core throughput is much higher: 184 fourth-generation tensor cores offering 466 tensor-TFLOPS for AI processing (that's the INT8 dense figure — FP16 tensor is ~58 TFLOPS dense / 117 with sparsity per WareDB).

Related SKUs for context:

- **RTX 4070 Ti**: 7,680 CUDA cores, providing 40.09 TFLOPS of FP32 performance
- **RTX 4070 SUPER**: FP32: 35.48 TFLOPS, FP16: 35.48 TFLOPS, BF16: 35.48 TFLOPS

For your GPT-2 760M training context: 29 FP32 TFLOPS on a single 4070 is toy-scale — you'd want BF16 tensor throughput (~58 TFLOPS dense) and note the 12GB VRAM cap will bottleneck batch size long before compute does. MI300X you're already using has ~163 TFLOPS FP32 / much higher matmul throughput, so 4070 is really a dev/inference box, not a training box for anything beyond small-scale experiments.

References:

- [WareDB RTX 4070 specs](https://www.waredb.com/processor/nvidia-geforce-rtx-4070)
- [WareDB RTX 4070 SUPER specs](https://www.waredb.com/processor/nvidia-geforce-rtx-4070-super)
- [ComputePrices RTX 4070 Ti specs](https://computeprices.com/gpus/rtx4070ti)
