---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Transformer与RNN：训练与推理的权衡
translated: true
type: note
---

问题：Transformer（注意力机制 + KV 缓存）是否真的对训练友好但对推理不友好，而 RNN 则相反（推理友好、训练不友好）？

答案：是的，这是正确的标准描述——实际上这正是 Mamba/RWKV/RetNet/SSM 背后的动机张力。让我详细说明其机制。

**Transformer：并行训练，串行且受内存限制的推理**

训练使用教师强制（teacher forcing）——目标序列在训练前已知，因此掩码自注意力可以一次性计算所有位置：

```
Q, K, V = X @ Wq, X @ Wk, X @ Wv        # X: [T, d]，一次矩阵乘法，所有 T 个位置
scores = Q @ K.T / sqrt(d)               # [T, T]
scores = scores.masked_fill(causal_mask, -inf)
attn = softmax(scores) @ V               # [T, d]
```

没有任何位置需要等待另一个位置的*输出*——因果掩码只是在一个大的并行矩阵乘法中将非法的注意力权重置零。这就是为什么 Transformer 能很好地饱和 GPU：每个层的顺序深度为 O(1)，计算量为 O(n²)，所有操作均为密集矩阵乘法。

推理则相反。你逐个生成 token t+1，每一步都需要关注*所有*之前的键/值：

```
# 解码步骤 t
k_t, v_t = x_t @ Wk, x_t @ Wv
kv_cache_k.append(k_t); kv_cache_v.append(v_t)   # 缓存每步增长
scores = q_t @ kv_cache_k.T                       # O(t) 计算
out = softmax(scores) @ kv_cache_v
```

你避免了为旧 token 重复计算 K/V（这正是缓存的作用），但：
- 内存：O(n) 且随上下文增长——缓存大小 = `2 × 层数 × 注意力头数 × 头维度 × n × 批次 × 字节数`。
- 每一步都需要*从 HBM 读取整个缓存*来生成一个 token → 算术强度骤降 → 解码受内存带宽限制，而非计算限制。这避免了重复计算，使推理更快，但也带来一个简单的权衡：缓存大小随序列长度线性增长——上下文越长，消耗的内存越多，且 LLM 受内存带宽限制，而非计算限制。
- 这就是长上下文破坏服务经济性的原因——解码通常受内存带宽限制，而非计算限制；在搭载 80GB H100 的 70B 模型上，4K 上下文支持约 59 个并发用户，但 128K 上下文则降至约 1 个用户。

**RNN：廉价的推理，串行的训练**

推理步骤的内存和计算复杂度均为 O(1)，与序列长度无关，因为所有历史信息都被压缩到一个固定大小的隐藏状态中：

```
h_t = tanh(Wx @ x_t + Wh @ h_{t-1} + b)   # 固定大小，无缓存增长
```

训练（BPTT）则是痛点：`h_t` *依赖于* `h_{t-1}` 的实际输出，而不仅仅是一个掩码——你无法在步骤 t-1 完成之前计算步骤 t。这是一个长度为 T 的硬性顺序依赖链，因此无法像注意力那样将序列压缩成一次大的矩阵乘法。GPU 利用率低，且长链上存在梯度消失/爆炸问题。

**这在实践中的重要性**

正是这种不对称性催生了 SSM/线性 RNN 浪潮（Mamba、RWKV、RetNet）——它们采用循环形式（廉价、O(1) 推理，类似 RNN），同时也能以并行扫描/分块形式（密集矩阵乘法、廉价训练，类似 Transformer）实现：

RWKV 集成了线性注意力机制，使其能够像 Transformer 一样进行并行训练，同时保留 RNN 的高效推理特性，在推理时实现恒定的计算和内存复杂度。Mamba 在训练时具有线性时间缩放能力，推理时内存成本恒定，因为整个状态被总结为一个固定大小的张量，在推理任务中吞吐量可提升高达 5 倍。

| | Transformer (注意力+KV缓存) | RNN | Mamba/RWKV/RetNet |
|---|---|---|---|
| 训练并行度 | O(1) 顺序深度，密集矩阵乘法 | O(T) 顺序 (BPTT) | O(1) 通过并行扫描/分块形式 |
| 推理内存 | O(n)，随上下文增长 | O(1)，固定状态 | O(1)，固定状态 |
| 推理瓶颈 | HBM 带宽（读取 KV 缓存） | 可忽略 | 可忽略 |
| 推理计算量/每个 token | O(n)（关注整个缓存） | O(1) | O(1) |

因此你的说法成立。唯一的注意事项：Transformer 训练“友好”的具体原因是在训练期间*没有循环依赖*（掩码替代了循环），而不是因为注意力计算廉价——它仍然是 O(n²)，这也是为什么预填充（而非解码）受计算限制且对于长提示词有二次成本。

参考文献：
- [The Mamba in the Llama: Distilling and Accelerating Hybrid Models](https://www.together.ai/blog/the-mamba-in-the-llama-distilling-and-accelerating-hybrid-models)
- [A Survey on LLM Acceleration based on KV Cache Management](https://arxiv.org/pdf/2412.19442)
- [KV Cache and KV Caching: The Hidden Bottleneck of LLM Inference](https://medium.com/@sulbha.jindal/kv-cache-and-kv-caching-a46acea80fe4)
- [Transformers vs Mamba vs Linear Attention: Who Wins Long Context?](https://machine-learning-made-simple.medium.com/transformers-vs-mamba-vs-linear-attention-who-wins-long-context-f1dc8ceb5ede)