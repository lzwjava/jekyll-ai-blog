---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 递归变换器与自适应深度
translated: true
type: note
---

**问题：** HuggingFace 上的 `Hippocrene/recurrent-transformer-0.1b-e0.4b` 是什么？

**回答：**

这是一个巧妙的研究模型，将三个经典思想融合在一个紧凑的包中。以下是详细解析：

## 核心思想：权重共享的循环深度

该模型并非堆叠 N 个*不同的* transformer 层（如 GPT-2 那样），而是拥有**一个共享的 transformer 块**，该块在每一个 token 上会被循环应用最多 8 次。可以理解为：

```
# 普通 transformer（GPT-2 风格）
x = layer_1(x)
x = layer_2(x)
...
x = layer_N(x)  # N 套不同的权重

# 该模型（Universal Transformer 风格）
for step in range(max_steps):
    x = shared_block(x)   # 每次使用相同的权重
    if halting_head(x) > threshold:
        break              # ACT：每个 token 可提前停止
```

## 架构细节

| 属性 | 数值 |
|---|---|
| 存储参数 | **110M** |
| 计算激活块 | ~46M |
| 最大循环步数 | 8 |
| 有效计算量 | ~0.4B（因此名称中有 `e0.4b`） |
| 隐藏维度 | 1280 |
| 注意力 | 20 个头 × 64 头维度 |
| FFN | SwiGLU, 10240 |
| 上下文 | Transformer-XL 记忆，最多 **4096 tokens** |
| 分词器 | GPT-2（词表 50257） |

## 融合的三篇论文

1. **Universal Transformer**（Dehghani 等人，2018）——深度间共享权重
2. **Adaptive Computation Time / ACT**（Graves，2016）——每个 token 的停止头；更难的 token 获得更多循环步数
3. **Transformer-XL**（Dai 等人，2019）——长上下文的段级记忆

ACT 部分尤其有趣：模型测量到代码平均需要 **~6.3 个循环步**，而难度大的散文则达到 **~8 步**——这表明停止机制确实在发挥有意义的作用。

## 训练栈

- 在 **8.7B tokens** 上预训练，13 个语料库混合（FineWeb、代码、书籍、arXiv、维基、对话、Pile）
- 在单块 RTX PRO 6000 Blackwell 上以 **原生 FP8** 训练
- 长上下文课程：512 → 1024 → 2048 → 4096 tokens
- 在 707M tokens 上进行 SFT（Dolly、Alpaca、OpenOrca、OpenHermes）
- 在 UltraFeedback 上进行 DPO

## 性能

- FineWeb PPL：**25.4**（相比之下 6 层基线为 35.8）
- 零样本宏观准确率：在 LAMBADA/HellaSwag/ARC-Easy/Winogrande 上为 **0.41**

## 为什么对你来说有趣

鉴于你在 nanoGPT/nanochat 上的工作以及对 MoE 和 transformer 内部机制的关注——这是模型效率的另一个方向：**深度自适应计算** 对比 **宽度稀疏计算**（MoE）。相同权重可以被复用 8 次的理念本质上是**通过循环实现的参数效率**，而非通过稀疏性。

停止头只是隐藏状态上的一个小型线性探测——实现起来微不足道。如果你想在 nanochat 中尝试这种模式，在标准 GPT 块基础上大概只需额外 50 行代码。

这是一个**研究/演示模型**，并非生产级——但与 MoE 浪潮相比，其架构思想扎实且探索不足。

**参考文献：**
- [模型卡片](https://huggingface.co/Hippocrene/recurrent-transformer-0.1b-e0.4b)
- [Universal Transformers (Dehghani 2018)](https://arxiv.org/abs/1807.03819)
- [ACT (Graves 2016)](https://arxiv.org/abs/1603.08983)
- [Transformer-XL (Dai 2019)](https://arxiv.org/abs/1901.02860)