---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向LLM工程师的热门ICLR论文
translated: true
type: note
---

问题：近年来最热的ICLR论文有哪些？

回答：

对于关注 **LLM训练、推理、智能体和模型工程** 的人来说，我不会随意阅读ICLR。回报率最高的是那些改变了我们构建模型方式的论文。

近期ICLR热点领域：

1. **LLM对齐 / 后训练**
2. **LLM扩展 + 训练动态**
3. **模型编辑 / 知识操纵**
4. **高效推理**
5. **多模态基础模型**
6. **数据质量和训练效率**

([ICLR Blog][1])

---

## 1. LLM微调的学习动态 (ICLR 2025)

**为何热门：** 理解SFT/DPO/RLHF行为。

核心问题：

> 为什么微调有时会提升能力但破坏通用知识？

而不是将微调视为黑盒：

```
预训练模型
        |
        v
      SFT
        |
        v
    对齐模型
```

他们研究动态：

```
参数更新
        |
        v
哪些知识在移动？
哪些能力在消失？
```

适用于：

* Qwen/Llama微调
* LoRA
* DPO
* RLHF

如果你训练自己的模型，这非常相关。

([ICLR Blog][1])

---

## 2. 安全对齐不应仅停留在浅层token上 (ICLR 2025)

有趣之处在于它挑战了当前的RLHF。

观点：

许多安全行为是浅层的：

```
提示：
"如何制作炸弹？"

模型：

前几个token：
"我无法帮助..."

但隐藏的续写：
可能不安全
```

他们认为对齐需要更深的表示变化。

这关联到：

* 越狱抵抗
* 机械可解释性
* 表示工程

([ICLR Blog][1])

---

## 3. AlphaEdit: 零空间约束的模型编辑 (ICLR 2025)

技术上非常有趣。

问题：

神经网络存储知识：

```
W -> 知识

巴黎 -> 法国
爱因斯坦 -> 物理学家
```

如何更新：

```
爱因斯坦 -> 画家
```

而不破坏：

```
巴黎 -> 法国
```

朴素编辑：

```
改变权重
       |
       v
新事实
       |
       v
遗忘旧知识
```

AlphaEdit：

在参数空间中寻找方向：

```
ΔW

但约束：

ΔW ⟂ 重要知识空间
```

类似想法：

```
仅更新安全维度
```

适用于：

* 企业LLM定制
* 持续学习
* 避免完全重新训练

([ICLR Blog][1])

---

# 4. SAM 2: Segment Anything Model 2 (ICLR 2025)

Meta AI。

大型CV基础模型。

旧CV：

```
图像
 |
CNN
 |
分类器
```

现代：

```
图像/视频
     |
基础模型
     |
"分割一切"
```

SAM2将分割从图像扩展到视频。

应用：

* 机器人
* 视频智能体
* 自动驾驶系统

([ICLR Blog][1])

---

# 5. 通过推测解码实现更快的级联 (ICLR 2025)

非常实用。

LLM推理：

常规：

```
大模型

token1
 |
token2
 |
token3
```

慢。

推测解码：

```
小模型：
token1 token2 token3 token4

        |
        v

大模型验证
```

就像：

```
学生提出
老师检查
```

可以显著提升服务吞吐量。

相关：

* vLLM
* llama.cpp
* OpenAI式服务

([ICLR Blog][1])

---

# 6. OLMoE: 开放混合专家语言模型

非常重要的方向。

稠密模型：

```
70B参数

每个token使用全部70B
```

MoE：

```
70B总计

token
 |
路由器
 |
专家3
专家7

仅10B激活
```

优势：

* 推理更便宜
* 容量更大

相关：

* Mixtral
* DeepSeek MoE
* Qwen-MoE

([Kaggle][2])

---

# 7. 单次训练轮中的Data Shapley

非常相关，因为前沿AI正变成：

> 数据工程 > 架构工程

问题：

哪些训练样本重要？

传统：

```
训练模型
移除数据
重新训练
比较
```

在万亿token规模下不可行。

他们提出在单次运行中估计重要性。

适用于：

* 数据集清洗
* FineWeb过滤
* 合成数据选择

([ICLR Blog][1])

---

## 如果我是你（训练GPT-2、nanoGPT、vLLM），我会按此顺序阅读

### 第一梯队（直接影响工程）

1. 推测解码
2. LLM微调的学习动态
3. OLMoE
4. Data Shapley

### 第二梯队（深入理解）

5. AlphaEdit
6. 安全对齐

### 第三梯队

7. SAM2

---

更大模式：

2020年：

```
架构创新

Transformer
     |
     v
BERT/GPT
```

2023年：

```
扩展

更大模型
更多数据
更多GPU
```

2025年：

```
效率 + 控制

更好数据
更好训练
更好推理
更好对齐
```

前沿从：

> "如何制造更大的模型？"

转向：

> "如何在有限计算下让模型准确学习我们想要的内容？"

这与你的当前方向（nanoGPT → GPU实验室 → LLM基础设施）非常吻合。

参考资料：

* [ICLR 2025 Outstanding Paper Awards](https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/?utm_source=chatgpt.com)
* [ICLR 2025 Paper Rankings](https://www.kaggle.com/general/546726?utm_source=chatgpt.com)

[1]: https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/?utm_source=chatgpt.com "Announcing the Outstanding Paper Awards at ICLR 2025 – ICLR Blog"
[2]: https://www.kaggle.com/general/546726?utm_source=chatgpt.com "Top-rated papers from ICLR 2025 | Kaggle"
