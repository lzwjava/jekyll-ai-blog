---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从LLM用户到LLM拥有者
translated: true
type: note
---

问题：除了仅仅使用LLM，建立对LLM（架构、训练和推理）真正第一性原理理解的最佳方法是什么？

回答：你已经有缩放定律/屋顶线笔记，所以跳过“什么是注意力”的教程。使用LLM和*掌握*LLM之间的差距通常在于以下三点之一：（1）从未手动推导过反向传播，（2）从未逐层推理过FLOPs/内存带宽，（3）从未自己实现过KV缓存+采样。做到这三点，“本质”就会豁然开朗。

**1. 前向传播——知道每个形状，不用自动求导**

```python
import numpy as np

def gpt_forward(x, Wte, Wpe, blocks, Wlm):
    # x: (B, T) token ids
    B, T = x.shape
    tok_emb = Wte[x]                      # (B, T, C)
    pos_emb = Wpe[np.arange(T)]           # (T, C)
    h = tok_emb + pos_emb                 # (B, T, C)
    for blk in blocks:
        h = block_forward(h, blk)         # (B, T, C)
    logits = h @ Wlm.T                    # (B, T, V)
    return logits

def attn(x, Wq, Wk, Wv, Wo, n_head):
    B, T, C = x.shape
    hd = C // n_head
    q = (x @ Wq).reshape(B, T, n_head, hd).transpose(0,2,1,3)  # (B,nh,T,hd)
    k = (x @ Wk).reshape(B, T, n_head, hd).transpose(0,2,1,3)
    v = (x @ Wv).reshape(B, T, n_head, hd).transpose(0,2,1,3)
    att = q @ k.transpose(0,1,3,2) / np.sqrt(hd)     # (B,nh,T,T)
    mask = np.triu(np.ones((T,T)), k=1).astype(bool)
    att[..., mask] = -np.inf
    att = np.exp(att - att.max(-1, keepdims=True))
    att /= att.sum(-1, keepdims=True)
    out = att @ v                                     # (B,nh,T,hd)
    out = out.transpose(0,2,1,3).reshape(B, T, C)
    return out @ Wo
```

精髓就在这里：注意力机制只是一个基于内容的加权平均——softmax(QKᵀ/√d)V。其他一切（RoPE、GQA、MLA、滑动窗口）都是对Q/K/V如何生成或掩码的修改，而不是一种新机制。

**2. 反向传播——手动推导一个线性层+softmax**

这是人们因为自动求导而跳过的一部分。做一次：

```python
# y = softmax(x @ W), loss = -log(y[target])
# dL/dz (softmax前的logits) = y - onehot(target)   <- 这就是交叉熵+softmax的全部魔力
dz = y.copy()
dz[range(B), target] -= 1
dW = x.T @ dz / B
dx = dz @ W.T
```

Transformer中的每个梯度都可以简化为像这样通过矩阵乘法和softmax进行链式法则。如果你自己推导出了`dz = y - onehot(target)`，那么在GPT-2训练过程中观察到的损失曲线就不再是黑箱了。

**3. 推理——预填充/解码分离 + KV缓存就是全部故事**

```python
class KVCache:
    def __init__(self, n_layer, n_head, hd, max_T):
        self.k = np.zeros((n_layer, n_head, max_T, hd))
        self.v = np.zeros((n_layer, n_head, max_T, hd))
        self.pos = 0

def decode_step(token, cache, blocks, Wte, Wpe, Wlm):
    h = Wte[token] + Wpe[cache.pos]        # (1, C) — 单个新token
    for i, blk in enumerate(blocks):
        q, k, v = project(h, blk)          # 每个 (1, hd)
        cache.k[i, :, cache.pos] = k
        cache.v[i, :, cache.pos] = v
        att = softmax(q @ cache.k[i, :, :cache.pos+1].T / sqrt(hd))
        h = att @ cache.v[i, :, :cache.pos+1] @ blk.Wo
    cache.pos += 1
    return h @ Wlm.T                       # 下一个token的logits
```

预填充是计算受限的（大矩阵乘法，一次处理完整序列）。解码是内存带宽受限的（你需要从HBM重新加载整个模型权重来生成*一个*token）——这正是你笔记中已经有的屋顶线区分，也是为什么批处理、推测性解码和量化都专门针对解码阶段的原因。

**现在真正的深度在哪里（基础之后）：**

- FlashAttention：注意力在GPU上的内存受限特性，IO感知而非FLOP感知——这在精选的推理论文列表中附有代码。
- MLA/GQA：压缩KV缓存是降低长上下文服务成本的主要杠杆——DeepSeek-V2的多头潜在注意力和相关的经济推理工作是当前的最新技术。
- 既然你已经训练过GPT-2 760M：下一步是在你自己的损失曲线上重新推导Chinchilla（拟合 `L(N,D) = E + A/N^α + B/D^β` 与实际运行结果），而不是相信论文中的常数——你的MI300X运行结果正是这个任务的完美数据集。

对于从模型→预训练→SFT→奖励→DPO/PPO/GRPO的端到端版本，并附带真实（非玩具）代码，这个仓库是最完整的公开资料，包含实际训练形状的代码，而非单个文件的演示：它按阶段结构化（数据、预训练、SFT、奖励、DPO、PPO、GRPO、评估、聊天），每个阶段都有理论和实际代码。

参考资料：

- [train-llm-from-scratch（完整流程，真实代码）](https://github.com/FareedKhan-dev/train-llm-from-scratch)
- [Awesome-LLM-Inference（FlashAttention、PagedAttention、量化、论文+代码）](https://github.com/xlite-dev/Awesome-LLM-Inference)
- [LLM Inference Unveiled: Survey + Roofline Model](https://arxiv.org/pdf/2402.16363)
- [你的笔记：Transformer基础（缩放定律、屋顶线）](https://phonism.github.io/LLMNotes/en/transformer-part1-fundamentals/)
- [Karpathy: Let's reproduce GPT-2 (build_nanogpt)](https://github.com/karpathy/build-nanogpt)
