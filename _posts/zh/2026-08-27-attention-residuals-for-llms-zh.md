---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型的注意力残差
translated: true
type: note
---

**问题：** 在大语言模型（LLM）中，AttnRes（注意力残差）是什么？

---

**答案：**

**AttnRes** 代表**注意力残差**，是一种对基于 Transformer 的大语言模型中标准残差连接的新型架构升级，由**月之暗面（Moonshot AI）的 Kimi 团队**提出（2026年3月）。

---

### 问题：标准残差连接

在现代采用 PreNorm 架构的大语言模型中，残差连接通过将所有先前层输出与**固定单位权重（全部为1）**简单相加来工作：

```
h_l = h_{l-1} + f_l(h_{l-1})
```

随着网络深度增加，这会导致两个问题：**特征稀释**，即每层对累积总和的相对贡献减少；以及**无界幅度增长**，这是 PreNorm Transformer 中一个众所周知的问题。

---

### 解决方案：AttnRes

AttnRes 将这种固定累加替换为**对先前层输出的 softmax 注意力**，使得每层能够以学习到的、依赖于输入的权重，选择性地聚合早期表示。

可以这样理解：正如 Transformer 革命将 RNN 的顺序循环替换为跨时间步（序列）的注意力一样，AttnRes 将残差的加性循环替换为**跨深度的注意力**。

---

### 两种变体

**完整 AttnRes** 保留嵌入层和每个较早子层输出。此列表随模型深度增长。

**分块 AttnRes**（实用变体）通过将层划分为块来解决内存问题：在每个块内使用标准残差，在块之间应用基于注意力的聚合。这减少了内存开销，同时恢复了完整 AttnRes 的大部分收益。

对于分组为 `N` 个块的 `L` 个子层，每个 token 的存储从 `O(Ld)` 降至 `O(Nd)`。大规模实验使用了大约八个块。

---

### 关键设计选择

两种变体共享的一个关键设计选择是**对所有伪查询进行零初始化**，这导致该机制从均匀平均开始，并在训练过程中逐渐特化。

---

### 结果

注意力残差论文报告了验证损失和下游性能方面一致（但适度）的提升，同时产生约**4%的训练成本**和**2%的推理成本**开销。

---

**参考文献：**
- [注意力残差——技术报告 (Kimi / 月之暗面)](https://arxiv.org/pdf/2603.15031)
- [Sebastian Raschka: 注意力残差 (AttnRes)](https://sebastianraschka.com/llm-architecture-gallery/attention-residuals/)
- [HuggingFace 论文页面](https://huggingface.co/papers/2603.15031)
- [超越“梯度高速公路”——Substack](https://kenhuangus.substack.com/p/beyond-the-gradient-highway-how-attention)