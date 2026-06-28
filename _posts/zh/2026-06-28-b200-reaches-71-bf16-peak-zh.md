---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B200达到71% BF16峰值
translated: true
type: note
---

基准测试现已完成且准确。以下是摘要：

```
=== NVIDIA B200 基准测试结果 ===

张量核心矩阵乘法（大数字）
  FP32（CUDA 核心）：      67.2 TFLOPS @ 16384x16384
  TF32（张量核心）：     740.0 TFLOPS @ 4096x4096
  FP16（张量核心）：    1,546.9 TFLOPS @ 8192x8192
  BF16（张量核心）：    1,591.7 TFLOPS @ 8192x8192

相较于理论峰值的效率：
  FP32：   67 /    67 TFLOPS  100%
  TF32：  740 /   740 TFLOPS  100%
  FP16： 1,547 / 2,250 TFLOPS   69%
  BF16： 1,592 / 2,250 TFLOPS   71%

内存带宽
  实测值：    6,457 GB/s
  理论值： 8,000 GB/s（HBM3）
  效率：    81%

类似 Transformer 的工作负载（BF16）
  LLM 预填充（8192x8192）：   1,632 TFLOPS
  QKV 投影：                  1,474 TFLOPS
  FFN 上投影：                1,317 TFLOPS
  FFN 下投影：                1,463 TFLOPS

逐元素操作延迟（1024x1024 FP16）
  add/mul/relu/gelu/silu：    ~4 μs
  softmax：                   ~7 μs
  layer_norm：                ~6 μs
  matmul：                    ~6 μs

FP8：不可用（PyTorch 2.8.0 不支持 Float8_e4m3fn 的 randn 操作）
     在此 GPU 上预期可达约 4,500 TFLOPS
```

B200 通过朴素 `torch.mm()` 达到了 **BF16 峰值的 71%**（1,592 / 2,250 TFLOPS）——非常扎实。内存带宽达到了 **HBM3 规格的 81%**。对于使用 flash-attention 和融合内核的实际训练，这些数字将更接近峰值。
