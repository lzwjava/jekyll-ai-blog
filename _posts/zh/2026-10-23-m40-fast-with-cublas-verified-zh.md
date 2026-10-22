---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M40 快速，经 cuBLAS 验证
translated: true
type: note
---

**已验证——M40 搭配 cuBLAS 确实很快：**

```
cublasSgemm 4096³ : 4333.6 GFLOPS   (≈63% of the card's ~6.8 TFLOPS fp32 peak)
1×4096 row GEMM   : 1.42 ms/token   (the exact op llama inference is built on)
```

最后一个数字意味着：对于 7B 级模型（hidden 4096），纯 GEMM 时间本身就约 **~25+ tok/s**；加上 attention/KV/dequant 开销后，在 24 GB VRAM 上实际可达 **8–15 tok/s**。这确实是一台可用的推理机——你的直觉是对的。

## 关于 `192.168.1.137` 的修正情况

| | 可用 ✅ | 永远不行 ❌ |
|---|---|---|
| **你自己的 CUDA 版 mini-llama.cpp** | 在 M40 上使用原生 CUDA 12.4 `sm_52` + `cuBLAS` —— **刚刚已验证** | — |
| PyTorch/vLLM/MiniMax-H3 | — | 它们需要 torch 的 CUDA≥12 操作路径 → 我们遇到的 UVM 挂起 |

M40 没问题——它只是 **仅支持 fp32、CC 5.2**，所以你的项目正好瞄准这一点（而不是那些最新最花哨的堆栈）。

## 你的 mini-llama.cpp → 在这台机器上的 GPU 版本

1. **CPU（纯 C，AVX2）**：GGUF 头部 + 张量表解析、llama BPE tokenizer、采样、KV-cache 地址簿、层控制流
2. **GPU（CUDA `sm_52`）**：上传 GGUF 权重，**一次性将 q4 反量化为 fp32**；所有 GEMM 通过 `cublasSgemm`（可行：4.3 TFLOPS）；自己编写 RMSNorm、RoPE、SiLU、softmax、scaled-dot-product attention 的小型 kernel
3. **VRAM 预算**（24 GB）：权重（7B q4 ≈ 5 GB，甚至 13B q4 ≈ 8 GB 也能装下）+ fp32 KV cache —— 上下文绰绰有余
4. **预期**：7B q4 ≈ 10-15 tok/s，首个 token 包含一次性的 dequant+upload 开销

## 准备开始了吗？

我建议的下一步：下载一个 **Qwen2.5-0.5B-Instruct GGUF（q4_K_M，≈0.44 GB）** 到 `/mnt/models`（通过 hf-mirror），作为你的里程碑 1 测试资源，然后我们实现 **里程碑 1：GGUF 解析器 + GPU GEMM 可行性验证**（加载一个真实权重张量，对其执行 `cublasSgemm`，并与 CPU 参考结果比对）。你说一声，我就开始下载并在这个仓库中搭建第一个里程碑的框架。