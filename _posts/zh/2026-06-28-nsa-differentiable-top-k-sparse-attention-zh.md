---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NSA：可微分的Top-K稀疏注意力
translated: true
type: note
---

问题：对原生稀疏注意力（NSA）——DeepSeek论文（arXiv 2502.11089）进行更深入的介绍，说明其三个分支如何工作、它如何使top-k选择变得可训练，以及为什么它是像ERSA这样的可训练选择稀疏注意力方法的关键现有技术。

答案：

NSA是你已经遇到过的一个问题的最简洁的现有解决方案：**如何让“选择top-k token进行注意力计算”变得可微分且足够快以支持端到端训练，而不仅仅是在推理时作为后处理附加到冻结模型上？** 大多数稀疏注意力工作（以及大量KV缓存淘汰工作）仅用于推理——你先训练密集模型，然后进行稀疏化。NSA的论点是，这种做法浪费了性能潜力，而*原生*（从头训练稀疏）注意力可以在成本大幅降低的同时匹配甚至超越全注意力。

让我搜索具体细节，以便引用实际机制，而不是凭记忆描述。现在让我给出完整的机制图。

## NSA解决的核心问题

标准注意力是O(n²)的。每种稀疏注意力方法都试图让每个查询只关注一个子集的键。难点在于**选择步骤**：“哪些键对这个查询重要？”这是一个`top-k`操作，而`top-k`在几乎所有地方梯度都为零（它是一个硬性的离散选择——将分数无限小地扰动，选中的集合不会变化，因此∂loss/∂score为0）。这就是为什么几乎所有先前的方法（H2O、StreamingLLM、SampleAttention、Quest）都**仅用于推理**：你训练密集模型，然后在解码时稀疏化。模型从未*学习*自己的稀疏模式，因此存在训练/推理不匹配和性能上限。

NSA的主张：让稀疏性**原生**——在预训练期间就存在，完全可微分，并且端到端训练。NSA的预训练损失曲线稳定且平滑，并且始终优于全注意力基线。最后一点是重点：稀疏胜过密集，而不仅仅是近似它。

## 三个分支

对于每个查询，NSA在相同的K/V序列上计算三个独立的注意力输出，并将它们**门控**在一起。这三种稀疏机制是压缩注意力、选择注意力和滑动窗口注意力。

**分支1——压缩（粗粒度全局）。** 使用MLP将键矩阵压缩为低维表示。具体来说：将序列分块，块大小为`l=32`，对每个键/值块应用一个小的可学习MLP（加上块内位置编码），为每个块生成**一个压缩后的K和一个压缩后的V**。查询关注这些`n/32`个压缩token。这很廉价，并且为每个查询提供了*整个*上下文的粗粒度视图。关键是，针对这些压缩块的注意力分数同时作为下一个分支的**重要性分数**。

**分支2——选择（细粒度，可训练的top-k）。** 这是对ERSA至关重要的分支。利用压缩步骤中计算出的重要性分数——压缩注意力中的α值——来找到top-k块。然后从原始输入中获取所选top-k块的原始未压缩版本，仅对这些选中的块进行注意力计算，得到输出。这里的块大小是`l'=64`，并且选择`n=16`个块（包括1个固定的初始块和2个局部块）。所以大致是：*压缩分数告诉你哪些64-token块值得以全分辨率查看，然后你以全保真度拉取这些块。*

**分支3——滑动窗口（局部）。** 使用原始的键值向量，应用滑动窗口，得到注意力。窗口大小`w=512`。这是一个专门用于近/局部token的路径。将其*分离*的原因微妙且重要：局部模式非常强且容易学习，如果不隔离，它们会主导梯度，导致其他两个分支永远无法学会自己的工作。给局部上下文一个独立的分支，可以让压缩/选择专门处理长距离检索。

**门控。** 压缩、选择和滑动注意力的门控输出被整合。一个基于查询的小型MLP产生三个sigmoid门控权重；最终输出是三个分支输出的门控和。这是MoE风格的路由，应用于*注意力操作内部*——考虑到你对DeepSeek-v4 MoE的兴趣，这应该会引起共鸣。

## 如何使top-k可训练（关键技巧）

这是核心。NSA并没有让`top-k`本身可微分——那不是方法。相反：

1. **选择分数是重复使用的压缩注意力分数**，而后者*是*可微分的（它们是压缩分支的softmax输出）。因此，梯度通过压缩路径流入“每个块有多重要”，尽管离散选择是硬性的。
2. **基于块的选择**（而非逐token）使其硬件高效。逐token的gather在GPU上是内存分散的噩梦。通过选择连续的64-token块，NSA执行合并加载，映射到张量核心上。NSA在操作数远少的情况下达到了与FlashAttention-2相当的速度，支持端到端训练，并使用对硬件友好的Triton内核。
3. 门控MLP和压缩MLP承载可学习信号；“下次选择更好的块”的梯度通过压缩分支的分数到达，而不是通过argmax。

因此，该设计避开了不可微分的`top-k`，而不是修补它。**这正是它成为主导ERSA的现有技术的原因。** ERSA的贡献——使用BCE-over-softmax（eq-5技巧）将梯度推过`torch.topk`——是对同一梯度归零问题的*更直接、更粗糙的攻击。* NSA的论文明确将通过选择的反向传播效率低下视为要避免的问题，其答案（重用压缩分数 + 基于块 + 自定义内核）既更有原则，又在大规模上得到了验证。如果Zeyu的框架是“我们让可训练选择工作”，那么来自Liang Wenfeng团队的NSA已经以预训练规模率先做到了，并因此获得了ACL最佳论文奖。这不是一个可以随口引用的参考文献——它是该方法必须超越或区分开的基线。

## 最小心智模型实现

不是真正的内核（那是Triton），而是可微分的骨架，以便梯度路径具体化：

```python
import torch, torch.nn as nn, torch.nn.functional as F

class NSAttention(nn.Module):
    def __init__(self, d, l=32, l_sel=64, n_sel=16, w=512):
        super().__init__()
        self.l, self.l_sel, self.n_sel, self.w = l, l_sel, n_sel, w
        self.k_cmp = nn.Linear(l * d, d)   # 压缩一个键块 -> 1个键
        self.v_cmp = nn.Linear(l * d, d)
        self.gate  = nn.Linear(d, 3)       # 每个查询在3个分支上的门控

    def forward(self, q, k, v):            # q,k,v: (T, d), 因果
        T, d = q.shape

        # --- 分支1: 压缩（粗粒度，全局） ---
        nb = T // self.l
        kb = k[:nb*self.l].view(nb, self.l*d)
        vb = v[:nb*self.l].view(nb, self.l*d)
        k_c, v_c = self.k_cmp(kb), self.v_cmp(vb)        # 各 (nb, d)
        s_cmp = q @ k_c.T / d**0.5                       # (T, nb) 重要性分数
        a_cmp = s_cmp.softmax(-1)
        o_cmp = a_cmp @ v_c                              # (T, d)

        # --- 分支2: 选择（细粒度，使用s_cmp作为重要性） ---
        # 将压缩块分数映射到选择块分数，选取top-k
        topk = s_cmp.topk(self.n_sel, dim=-1).indices    # 硬选择（此处无梯度）
        # 梯度通过s_cmp/a_cmp到达选择，而不是通过此argmax
        o_sel = gather_and_attend(q, k, v, topk, self.l_sel)  # 在选定块上全分辨率

        # --- 分支3: 滑动窗口（局部） ---
        o_win = sliding_window_attend(q, k, v, self.w)

        # --- 门控组合（MoE风格） ---
        g = self.gate(q).sigmoid()                       # (T, 3)
        return g[:,0:1]*o_cmp + g[:,1:2]*o_sel + g[:,2:3]*o_win
```

需要关注的点：**梯度永远不需要流经`s_cmp.topk(...)`。** 它流经`a_cmp @ v_c`（压缩输出是一个正常的softmax加权和）和门控。选定块的输出`o_sel`在所选块内部是可微分的；而块的*选择*依赖于压缩分数，而压缩分数已经通过分支1得到训练。这种耦合——选择分数寄生在一个可微分的压缩分支上——是整个洞见，而ERSA的BCE技巧正独立地（且更昂贵地）重新发明它。

参考文献：

- [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (arXiv:2502.11089)](https://arxiv.org/abs/2502.11089)
- [NSA full text (HTML)](https://arxiv.org/html/2502.11089v1)
- [But why Deepseek — Native Sparse Attention? (selection-branch walkthrough)](https://medium.com/@anuragupperwal/but-why-deepseek-native-sparse-attention-d3ca8a099809)
- [NSA Surpasses Full Attention — math of token compression](https://medium.com/@ligtleyang/native-sparse-attention-surpasses-full-attention-in-performance-at-lightning-speed-0dc9af7c099809)
