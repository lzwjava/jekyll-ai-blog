---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 嵌入维度与头维度解析
translated: true
type: note
---

**问题：** 在嵌入维度为768、头维度为128的nanoGPT/nanochat中，这两个维度有什么区别？

**回答：**

它们并非二选一的关系——而是**多头注意力机制中相互关联的维度**：

- **嵌入维度（768）** = 每个token的隐藏状态总大小
- **头维度（128）** = 每个注意力头所处理的嵌入切片大小

当嵌入维度为768、头维度为128时，会形成 **768 / 128 = 6个注意力头**。

具体流程如下：

```python
batch_size, seq_len = 2, 10
embed_dim = 768
num_heads = 6
head_dim = embed_dim // num_heads  # 128

# Token嵌入
x = torch.randn(batch_size, seq_len, embed_dim)  # (2, 10, 768)

# 线性投影生成Q、K、V
W_q = torch.randn(embed_dim, embed_dim)
Q = x @ W_q  # (2, 10, 768)

# 重塑维度以分离注意力头
Q = Q.reshape(batch_size, seq_len, num_heads, head_dim)  # (2, 10, 6, 128)
Q = Q.transpose(1, 2)  # (2, 6, 10, 128) — 现在有6个头，每个头在128维上运行

# 每个头独立计算注意力
K = x @ W_k  # (2, 10, 768)
K = K.reshape(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)  # (2, 6, 10, 128)

# 注意力计算：(Q @ K^T) @ V，全部在每头128维空间中进行
scores = Q @ K.transpose(-2, -1)  # (2, 6, 10, 10) — 注意力logits
attn_weights = softmax(scores / sqrt(128), dim=-1)  # 缩放因子为sqrt(head_dim)

V = x @ W_v
V = V.reshape(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)  # (2, 6, 10, 128)

out = attn_weights @ V  # (2, 6, 10, 128) — 每个头输出128维

# 将所有头的结果拼接回去
out = out.transpose(1, 2)  # (2, 10, 6, 128)
out = out.reshape(batch_size, seq_len, embed_dim)  # (2, 10, 768)
```

**关键要点：** 每个头独立处理其128维投影，随后将所有6个头的输出拼接起来，恢复完整的768维表示。这种方式可以实现**并行、多样化的注意力模式**，且不会增加计算量（6个头 × 128维 = 768维总量，与单个768维注意力相同）。

注意力机制中的`sqrt(head_dim)`缩放至关重要——它能稳定不同头维度下的梯度。

对于nanoGPT规模（768维、6个头）而言，这是典型配置。更大的模型如GPT-3使用12288维、96个头（每个头128维）——采用相同的比例。
