---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FreeToken高效本地MoE
translated: true
type: note
---

问题：什么是FreeToken论文？

答案：

**FreeToken**是一篇关于通过优化推理系统而非修改模型，使**超大规模混合专家（MoE）大语言模型**能够在普通计算机上本地运行的论文。论文标题是：

> **“FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution”**
> arXiv:2608.16157 ([arXiv][1])

核心思想：

> 将你的PC视为一个小型分布式系统：GPU显存 + CPU内存 + PCIe带宽 + 模型缓存，而不是认为“我的GPU太小了。”

([Hugging Face][2])

---

## 问题

现代MoE模型非常庞大。

示例：

```
GLM-5.2
753B参数
```

简单计算：

```
753B参数 × 2字节（BF16）

≈ 1.5 TB内存
```

对于以下设备不可能：

```
RTX 4090 24GB
RTX 5090 32GB
```

通常你需要：

```
8 × H100
16 × H100
大型数据中心
```

---

## 但MoE有一个技巧

混合专家模型：

```
              输入标记
                  |
                  v
        路由器选择专家
          /       |       \
      专家1    专家2    专家3
                  ^
                  |
              仅少数激活
```

一个700B的模型可能拥有：

```
总专家：
700B参数

每个标记激活：
30B参数
```

因此计算量很小，但内存是问题。

问题：

> 我们如何将正确的专家快速移到GPU？

---

## 以往方法：静态卸载

示例：

```
GPU显存：

专家1
专家2
专家3


CPU内存：

专家4
专家5
专家6
...
```

问题：

路由器每个标记都会改变。

标记1：

```
需要专家1,2,3
```

标记2：

```
需要专家20,21,22
```

现在PCIe传输成为瓶颈。

---

## FreeToken的思路

FreeToken将GPU内存变为**动态缓存**。

就像CPU缓存：

```
内存
 |
 | 更慢
 v

GPU显存
 |
 |更快
 v

张量核心
```

系统会观察：

```
哪些专家被频繁使用？
```

然后保留热门专家：

```
GPU：

专家7
专家15
专家21

（缓存）
```

移动冷门专家：

```
CPU内存
```

这类似于：

* 操作系统页缓存
* CPU L1/L2缓存
* Redis热键缓存

---

## 另一个重要思路：带宽感知执行

他们衡量：

```
GPU计算速度

vs

PCIe传输速度

vs

CPU内存带宽
```

然后决定：

```
CPU应该计算这个专家？

还是应该把它移到GPU？
```

不是固定规则。

由硬件决定。

([FreeToken Wiki][3])

---

## 为什么会提到MIT/伯克利的人？

作者列表包括研究人员，例如：

* Song Han
* Matei Zaharia
* Ion Stoica

([arXiv][1])

他们是重要系统背后的研究者：

```
深度学习硬件优化
+
分布式系统
+
云基础设施
```

例如：

* Song Han → 高效神经网络、TensorRT相关生态系统
* Matei Zaharia → Spark、ML系统
* Ion Stoica → Apache Spark、Ray、分布式系统

---

## 为什么对像你这样构建本地AI的人很重要

你当前的配置：

```
RTX 4070 Ti 12GB
```

传统思维：

```
12GB显存
      |
      v
无法运行大模型
```

FreeToken的思维：

```
RTX 4070 Ti
+
64/128GB内存
+
PCIe
+
智能缓存

=
可以运行更大的模型
```

未来的技术栈变成：

```
模型
 |
 v
推理引擎
 |
 +-- vLLM
 +-- SGLang
 +-- FreeToken
 +-- llama.cpp
 |
 v
硬件抽象
 |
 v
消费级GPU
```

突破并非新的Transformer层，而是**系统工程**。

类似于数据库领域曾发生的情况：

```
硬件改进
+
软件改进

=
新的可能性
```

LLM推理正在进入那个阶段。

([github.com][4])

参考文献：

* FreeToken论文：([arXiv][1])
* FreeToken GitHub：([github.com][5])
* 论文摘要：([Hugging Face][2])

[1]: https://arxiv.org/abs/2608.16157?utm_source=chatgpt.com "FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution"
[2]: https://huggingface.co/papers/2608.16157?utm_source=chatgpt.com "Paper page - FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution"
[3]: https://www.freetoken.wiki/architecture/FreeToken-paper?utm_source=chatgpt.com "FreeToken paper: MoE Serving Comparison and Setup Guide - FreeToken Wiki"
[4]: https://github.com/FlashML-org/FreeToken/blob/main/README.md?utm_source=chatgpt.com "FreeToken/README.md at main · FlashML-org/FreeToken · GitHub"
[5]: https://github.com/FlashML-org/FreeToken?utm_source=chatgpt.com "GitHub - FlashML-org/FreeToken · GitHub"
