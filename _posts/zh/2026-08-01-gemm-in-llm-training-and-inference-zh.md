---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GEMM在大语言模型训练与推理中的应用
translated: true
type: note
---

问题：什么是GEMM，它在LLM训练/推理中出现在哪里？

答案：

GEMM = **通用矩阵乘法**：`C = alpha * A@B + beta * C`，形状为 `(M,K) @ (K,N) -> (M,N)`。它是BLAS-3基础操作（cuBLAS/cutlass/rocBLAS），其他所有操作都构建在其之上。

**它在Transformer层中的位置：**

每个`nn.Linear`都是一个GEMM。每层包含：
- QKVO投影：4个GEMM，每个形状为 `(seq, d_model) @ (d_model, d_model)`
- MLP上下投影：2个GEMM，形状分别为 `(seq, d_model) @ (d_model, 4*d_model)` 及其反向
- 注意力分数 `Q@K^T` 和 `attn@V`：按注意力头进行批处理GEMM

这就是Kaplan/Chinchilla `C ≈ 6ND` FLOPs近似存在的原因——GEMM的FLOPs（每个为`2*M*N*K`）占总计算量的主导地位；softmax/layernorm/RoPE的FLOPs可忽略不计，仅影响延迟和内存开销。

```python
# 朴素GEMM，复杂度O(M*N*K)
def gemm_naive(A, B):
    M, K = A.shape
    K2, N = B.shape
    C = [[0.0]*N for _ in range(M)]
    for i in range(M):
        for j in range(N):
            s = 0.0
            for k in range(K):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C

flops = lambda M,N,K: 2*M*N*K  # 乘加操作 = 2次FLOP
```

真实的GEMM内核将A/B矩阵分块到共享内存/寄存器块中，使其匹配张量核心的形状（例如Ampere及以上架构上fp16的16x16x16），以最大化算术强度并达到峰值TFLOPS。这就是cuBLAS/cutlass/Triton所做的——上述朴素的三重循环比分块张量核心内核慢约1000倍。

**对你实际重要的洞察（推理/代理服务）：** GEMM假设 `M > 1`。在自回归**解码**过程中，当批次大小为1时，你执行的是 `(1, d) @ (d, d)`——这是一个**GEMV**（矩阵-向量乘法），而不是GEMM。GEMV受内存带宽限制（每个token加载整个权重矩阵，几乎没有重用），而GEMM受计算限制（在M和N维度上重用行/列）。这就是为什么存在连续批处理/vLLM风格的服务：将解码请求一起批处理，将许多小GEMV转换为一个大GEMM，从而从带宽受限转为计算受限，并成倍提高吞吐量。

粗略的算术强度检查：
```
AI = FLOPs / bytes_moved
GEMM（M,K,N较大）：  AI ~ O(min(M,N,K))  -> 计算受限
GEMV（M=1）：          AI ~ O(1)           -> 内存受限，GPU饥饿
```

这也是为什么**MFU（模型FLOPs利用率）**——实际达到的FLOPs/秒除以GPU峰值FLOPs/秒——是在MI300X上训练760M GPT-2时跟踪的指标。低MFU几乎总是意味着你的GEMM在形状/批处理上未达到计算受限状态（分块大小不合适、批处理小、未融合操作导致GEMM之间产生额外内存流量）。

参考文献：
- [数据移动才是关键（GEMM/内存受限分析）](https://arxiv.org/abs/2007.00072)
- [NVIDIA cuBLAS GEMM性能指南](https://docs.nvidia.com/cuda/cublas/)
- [vLLM PagedAttention论文（连续批处理动机）](https://arxiv.org/abs/2309.06180)