---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GQA和MLA详解
translated: true
type: note
---

**问题：** 我知道注意力机制在上下文长度上是二次复杂度的（Q@Kᵀ 矩阵乘法），这导致速度慢且内存占用高。请解释 GQA 和 MLA。另外：上下文长度 T 具体如何进入矩阵乘法的维度？在 CUDA 层面，矩阵乘法意味着什么？它在内存中是如何布局的？并行执行顺序是怎样的？

**回答：**

## 1. T 出现在哪里——确认你的思维模型

你的理解是正确的：**计算是二次的，KV 缓存是线性的**（每个 token），但注意力 *分数矩阵* 是二次的。形状，nanoGPT 风格：

```python
# B=batch, H=heads, T=seq_len, d=head_dim
q = x @ Wq   # (B, T, H*d) -> view -> (B, H, T, d)
k = x @ Wk   # (B, H, T, d)
v = x @ Wv   # (B, H, T, d)

att = q @ k.transpose(-2, -1)   # (B,H,T,d) @ (B,H,d,T) -> (B,H,T,T)  ← T² 在此处
att = softmax(att / sqrt(d) + causal_mask)
out = att @ v                   # (B,H,T,T) @ (B,H,T,d) -> (B,H,T,d)  ← 再次 T²
```

所以 T 同时是矩阵乘法 `(T×d) @ (d×T) → (T×T)` 的 M 和 N 维度。FLOPs ≈ `2·B·H·T²·d`。上下文长度翻倍 → 注意力计算量变为 4 倍，而 `(T,T)` 的分数矩阵正是导致朴素注意力内存溢出（OOM）的原因（FlashAttention 通过分块计算 softmax 解决了内存部分，从不实例化该矩阵——计算量仍然是 O(T²)）。

需要区分两个阶段：

- **预填充**：完整的 T×T → 二次。
- **解码**（一次一个 token）：q 是 `(B,H,1,d)`，K 被缓存为 `(B,H,T,d)` → 每一步是 O(T)，总生成过程是 O(T²)。这里的瓶颈是 *内存带宽*——每一步都要读取 KV 缓存。这就是 GQA/MLA 要解决的问题。

## 2. GQA——通过在 query 头部之间共享 K/V 来缩小 KV 缓存

MHA：每个 query 头都有自己的 K 和 V 头。GQA：**G 个 query 头共享一个 KV 头**。Llama-3-70B：64 个 query 头，8 个 KV 头 → KV 缓存缩小 8 倍，解码时内存读取减少 8 倍。质量损失很小，因为不同头部之间的 K/V 表示存在冗余。

```python
# GQA 约 15 行
n_head, n_kv_head, d = 32, 8, 128
group = n_head // n_kv_head  # 每个 KV 头对应 4 个 query 头

q = x @ Wq  # (B, T, n_head*d)    -> (B, n_head,    T, d)
k = x @ Wk  # (B, T, n_kv_head*d) -> (B, n_kv_head, T, d)   Wk 缩小了 4 倍
v = x @ Wv  # (B, T, n_kv_head*d) -> (B, n_kv_head, T, d)

k = k.repeat_interleave(group, dim=1)  # 广播到 (B, n_head, T, d)
v = v.repeat_interleave(group, dim=1)  # （实际内核使用索引，不复制）
# ...然后标准注意力
```

每层每个 token 的 KV 缓存：MHA `2·n_head·d`，GQA `2·n_kv_head·d`。MQA 是极端情况（`n_kv_head=1`）。

## 3. MLA——将 KV 压缩为低秩潜变量，只缓存潜变量

DeepSeek 的举措（V2/V3，你会在 v4 系列中看到）：不再缓存 K 和 V，而是每个 token 缓存一个小的**潜向量**，并在需要时从中重构 K/V。

```python
# MLA 草图（省略 RoPE 细节）
d_model, d_c = 5120, 512          # 潜变量维度 << 2*n_head*d

c_kv = x @ W_down                  # (B, T, d_c)   ← 这就是你缓存的所有内容
k    = c_kv @ W_uk                 # (B, T, n_head*d)  需要时重构
v    = c_kv @ W_uv                 # (B, T, n_head*d)
```

每个 token 的缓存：`d_c + d_rope` ≈ 512 + 64 = **576 个值**，相比之下 MHA 有 128 个头 × 128 维 = `2·128·128` = **32,768** 个值——减少约 57 倍。使其真正有效的两点：

1. **矩阵吸收**：推理时你永远不会实例化 k。`qᵀk = qᵀ(W_uk · c) = (W_ukᵀ q)ᵀ c`——将 `W_uk` 折叠到 query 投影中，直接对缓存的潜变量做注意力。同样的技巧将 `W_uv` 折叠到输出投影中。
2. **解耦的 RoPE**：RoPE 是位置相关的，因此无法吸收到固定矩阵中；MLA 为每个 token 携带一个小的独立旋转子维度（就是那个 +64）。

与 GQA 不同，MLA 不仅是共享——它是一个学习到的低秩瓶颈，DeepSeek 证明了它在缓存远小于 MHA 的情况下，质量却 *优于* MHA。好的后续阅读：DeepSeek-V2 论文 §2.1，或 deepseek-ai/DeepSeek-V3 的 `model.py` 中的 `mla` 实现（约 100 行）。

## 4. 矩阵乘法 *是什么*，以及 CUDA 如何实现它

定义：`C[i,j] = Σₖ A[i,k] · B[k,j]`——A 的第 i 行与 B 的第 j 列点乘。仅此而已。`(M×K) @ (K×N) → (M×N)`，`2·M·N·K` FLOPs。

**内存布局**：不存在二维内存。一个 `(M,K)` 的行主序矩阵是一个扁平数组，其中 `A[i][k]` 位于 `A[i*K + k]`。行元素连续；列元素以 K 为步长。这就是为什么按列读取 B 很慢，以及为什么转置和分块很重要。

朴素内核——每个输出元素一个线程：

```cuda
__global__ void matmul_naive(const float* A, const float* B, float* C,
                             int M, int N, int K) {
    int i = blockIdx.y * blockDim.y + threadIdx.y;  // 行
    int j = blockIdx.x * blockDim.x + threadIdx.x;  // 列
    if (i >= M || j >= N) return;
    float acc = 0.0f;
    for (int k = 0; k < K; k++)
        acc += A[i*K + k] * B[k*N + j];   // B 访问：步长 N -> 重用性差
    C[i*N + j] = acc;
}
```

这种方式可以工作，但 A 和 B 的每个元素都会从全局内存中重新读取约 N 或 M 次。算术强度极低 → 受内存限制。解决方法：**在共享内存中进行分块**：

```cuda
#define TILE 32
__global__ void matmul_tiled(const float* A, const float* B, float* C,
                             int M, int N, int K) {
    __shared__ float As[TILE][TILE], Bs[TILE][TILE];
    int i = blockIdx.y * TILE + threadIdx.y;
    int j = blockIdx.x * TILE + threadIdx.x;
    float acc = 0.0f;
    for (int t = 0; t < K; t += TILE) {
        // 协作加载：32x32 个线程各抓取一个元素。
        // threadIdx.x 变化最快 -> 连续线程读取连续地址
        // -> 每个 warp 一次合并的 128 字节事务。
        As[threadIdx.y][threadIdx.x] = A[i*K + (t + threadIdx.x)];
        Bs[threadIdx.y][threadIdx.x] = B[(t + threadIdx.y)*N + j];
        __syncthreads();                       // 等待分块到位
        for (int k = 0; k < TILE; k++)
            acc += As[threadIdx.y][k] * Bs[k][threadIdx.x];  // SRAM，~很快
        __syncthreads();
    }
    C[i*N + j] = acc;
}
```

现在每个全局内存值在共享内存中被重复使用 TILE(=32) 次。真实的内核（cuBLAS/CUTLASS）更进一步：每个线程计算一个 8×8 的寄存器分块，warp 驱动 16×16×16 分片上的张量核心，双缓冲异步加载。但分块是核心思想——FlashAttention 对 `(T,T)` 分数矩阵应用了同样的思想。

**并行执行顺序——人们常搞错的部分：**

- **跨块之间**：顺序是 *未定义的*。GPU 以任意顺序将块调度到 SM 上；你不能假设块 0 在块 5 之前运行。正确性不能依赖于此。块只能通过内核边界（或协作组）进行同步。
- **块内**：`__syncthreads()` 是你唯一的顺序屏障。
- **warp 内**：32 个线程锁步执行（SIMT）。
- **单个线程内**：k 循环的累加是顺序的，从左到右，在该线程的寄存器中。因此基本的分块矩阵乘法是确定性的。当 *规约被拆分到多个线程* 时会出现非确定性——例如使用 `atomicAdd` 的 split-K 矩阵乘法，某些反向内核——因为浮点加法不是结合的：`(a+b)+c ≠ a+(b+c)`。这就是为什么 `torch.use_deterministic_algorithms(True)` 会禁用某些内核。

## 5. 在你的 4070 上试试

```bash
nvcc -O3 matmul.cu -o matmul && ./matmul          # 你的内核
python -c "import torch; ..."                      # 对比 torch.matmul (cuBLAS)
ncu --set full ./matmul                            # Nsight Compute：查看合并访问、占用率
```

在 M=N=K=4096 时基准测试朴素→分块→cuBLAS。在 4070 上预期大约 ~300 GFLOPs → ~3 TFLOPs → ~25+ TFLOPs (fp32)。看着这个 100 倍的差距缩小是最快理解为什么内存布局是全部关键的方法。然后阅读 FlashAttention 论文——你会觉得它很明显。

**参考文献：**

- [DeepSeek-V2: MLA 论文](https://arxiv.org/abs/2405.04434)
- [GQA 论文 (Ainslie et al.)](https://arxiv.org/abs/2305.13245)
- [Simon Boehm — 如何优化 CUDA Matmul 内核](https://siboehm.com/articles/22/CUDA-MMM)
- [FlashAttention](https://arxiv.org/abs/2205.14135)
- [karpathy/llm.c — 纯 CUDA 的注意力和矩阵乘法内核](https://github.com/karpathy/llm.c)