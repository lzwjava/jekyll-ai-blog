---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 单头门控值嵌入
translated: true
type: note
---

这两行代码位于 `CausalSelfAttention.__init__`（gpt.py:80-82）中，实现了 **“值嵌入”（VE）机制的门控** —— 一种 ResFormer 风格的值残差，将每个 token 的查找注入注意力机制的 V 路径。以下是每行的作用：

## `self.ve_gate_channels = 12`

一个硬编码的超参数：门控仅读取残差流的前 **12 个通道**，而非完整的 `n_embd=768`。这使得门控网络非常小（类似于隐藏状态的“廉价标量探针”，与第 183 行读取 `:24` 的 `smear_gate` 思路相似）。

## `self.ve_gate = Linear(12, n_kv_head, bias=False) if has_ve(...) else None`

一个小的线性层，将 12 个通道映射到 `n_kv_head` 个标量，每个 KV 头对应一个 **门控值**。条件判断的存在是因为模型并非每一层都使用 VE：

```python
def has_ve(layer_idx, n_layer):            # gpt.py:53
    return layer_idx % 2 == (n_layer - 1) % 2
```

这选取了 **与最后一层同奇偶性的交替层** —— 最后一层始终拥有 VE，其余层交错分布。没有 VE 的层根本没有门控模块（`None` → 无参数，无计算），从而保持网络轻量化。

## 在 `forward` 中的使用方式（gpt.py:93-98）

```python
# ve: (B, T, n_kv_head * head_dim) from value_embeds[str(layer)](token_ids)
if ve is not None:
    ve = ve.view(B, T, self.n_kv_head, self.head_dim)          # 每个 KV 头一个嵌入
    gate = 3 * torch.sigmoid(self.ve_gate(x[..., :12]))        # (B, T, n_kv_head), 范围 (0, 3)
    v = v + gate.unsqueeze(-1) * ve                            # 门控按头应用，作用于所有 head_dim
```

因此流程如下：

1. **值嵌入查找**：`self.value_embeds[str(i)]` 是一个 `nn.Embedding(vocab_size → kv_dim)`，将原始 token id 映射为与 V 流投影相同形状的向量（gpt.py:501，192）。
2. **依赖输入的门控**：隐藏状态 `x`（token 的前12通道）经过门控线性层 + sigmoid 压缩，再乘以 3 以落在 (0, 3) 范围内。每个 KV 头获得独立的乘数 —— 网络学习*何时/多少*将 token 的值嵌入注入每个头。
3. **混入 V**：`v = v + gate * ve` 在 flash attention 之前将门控后的值嵌入加到投影后的值上，从而参与注意力输出。

门控使得 VE 变成 *依赖输入* 的：模型并非像原始 ResFormer 那样总是向 V 添加固定的每个 token 嵌入，而是在每个位置和每个头上决定注入的强度。`bias=False` 加上 `Linear` 子类与模型其余部分保持一致（权重在优化器中保持 fp32，但在矩阵乘法时转换为激活精度），并且在 gpt.py:254-255 的初始化将权重设为 `uniform_(0.0, 0.02)`，使得门控从接近其中性工作点开始并从那里学习。