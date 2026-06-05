---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash Attention SRAM 效率
translated: true
type: note
---

问题：Flash Attention 中的 SRAM 是什么，为什么它很重要？

回答：

Flash Attention 中的 SRAM 是 GPU 流多处理器上的**片上高速缓存存储器**，该算法利用它来减少昂贵的 HBM（高带宽内存）访问。

## GPU 内存层次结构（RTX 4070 / MI300X 上下文）

```
L0 缓存（128 字节/线程）  ← 超快速，隐式
L1 缓存（每个 SM 128 KB）
SRAM / 共享内存（每个 SM 96-192 KB）  ← Flash Attention 位于此处
L2 缓存（全局共享 12 MB）
HBM（GDDR6/HBM3）  ← 慢！RTX 4070 为 750 GB/s，但每 100 个周期为 192 GB/s
```

SRAM 带宽比 HBM **快约 10-100 倍**。在 RTX 4070 上，SRAM 带宽 ≈ 5 TB/s，而 HBM ≈ 576 GB/s。延迟差距更大。

## Flash Attention 的洞见

标准注意力计算：`Attention(Q, K, V) = softmax(Q @ K^T / √d) @ V`

**朴素方法**（NVIDIA 多年来的做法）：

1. 从 HBM 加载所有 Q、K、V → GPU 寄存器/SRAM
2. 计算完整的 `Q @ K^T`（N×N 矩阵）——**必须存在于 HBM 中，因为它对于 SRAM 来说太大**
3. 逐行计算 softmax，产生 O(N²) 次 HBM 访问

**Flash Attention 方法**：

1. 将 Q 分块，块大小 M = SRAM_size / (3 × d × sizeof(float))
2. 对于每个 Q 块，循环遍历 K、V 块
3. **所有中间计算都留在 SRAM 中**——加载、计算、累加、写回
4. 将 HBM 访问从 O(N²d) 减少到 O(Nd)

## 数学原理（简化版）

假设你有：

- 序列长度 N = 4096，d_model = 128
- 可用于张量的 SRAM ≈ 96 KB
- 块大小：M = 96_000 / (3 × 128 × 4) ≈ 62 个 token

对于每个包含 62 个 Q token 的块：

```python
# 伪代码
m = -inf  # 行最大值（用于数值稳定的 softmax）
l = 0     # exp 的行和
O = zeros(M, d)  # 输出累加器

for block_k_v in range(0, N, block_size_kv):
    # 将 K、V 块加载到 SRAM 中
    K_block = load_from_HBM(block_k_v)  # (block_kv, d)
    V_block = load_from_HBM(block_k_v)  # (block_kv, d)

    # 在 SRAM 中计算这个块的注意力
    scores = Q_block @ K_block.T / sqrt(d)  # (M, block_kv)

    # 数值稳定的 softmax，使用运行最大值/求和
    m_new = max(m, scores.max(axis=1))
    l = exp(m - m_new) * l + exp(scores - m_new).sum(axis=1)
    m = m_new

    # 累加输出（关键：在 SRAM 中完成）
    O += exp(scores - m[:, None]) @ V_block

# 最终归一化
return O / l[:, None]
```

关键点：**Q_block、K_block、V_block、scores 和 O 全部驻留在 SRAM 中**。仅发生 HBM -> SRAM 和 SRAM -> HBM 的传输。没有存储中间的 O(N²) 矩阵。

## 为什么这对你的 MI300X 很重要

在 AMD MI300X（192 GB HBM3）上：

- HBM3 带宽：5.2 TB/s（比 RTX 4070 好得多）
- 但 MI300X 上的 SRAM 带宽惊人：核心访问本地 SRAM 可达 100+ TB/s
- 效率提升**较小**（你的差距较小），但仍然至关重要

对于一个 4B token 模型，Flash Attention 根据序列长度和 d_model 可节省大约 4-10 倍的 HBM 压力。

## 实现说明

如果你在训练 nanoGPT 规模模型：

- torch.nn.functional.scaled_dot_product_attention（PyTorch 2.0+）在可能时自动使用 Flash Attention
- 对于手动 CUDA，使用 `cutlass::gemm` 进行 Q @ K^T 并仔细累加
- MI300X 每个芯片有 64 MB L3 缓存——更激进的分块空间更大

论文（Dao 等人，2022）包含了完整算法，包括梯度传递。前向传播很简单；反向传播才是真正神奇的地方（你需要从块中重新计算注意力，而不是存储它）。

参考文献：

- [Flash-Attention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) (Dao et al., 2022)
- [GPU Memory Hierarchy & Roofline Model](https://people.eecs.berkeley.edu/~sameh/SC16/SC16_Roofline_Samuel_Williams.pdf)
