---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从单GPU到分布式训练
translated: true
type: note
---

问题：你的探索路径——从单GPU LLM训练到多GPU基础设施、DeepSpeed、推理系统以及GPU硬件——这个方向对吗？

回答：

是的，你的方向非常自然。实际上，你目前的位置很有趣，因为你正处在 **AI工程的三个层面** 的交汇处：

```
模型研究
    ↓
训练基础设施
    ↓
硬件/系统优化
```

大多数人只接触其中一个层面。

你已经做过：

* 训练 GPT-2 760M/1.3B 规模的模型
* 理解 transformer 基础
* 运行 nanochat
* 接触 vLLM/KV cache
* 搭建 GPU 环境
* 调试 CUDA/驱动问题

下一步不一定需要“买更多 GPU”。而是理解**分布式训练为什么能工作**。

---

## 1. 两块消费级 GPU：你的直觉是对的

例如：

```
GPU0 RTX 4070
      |
    PCIe
      |
   CPU / 芯片组
      |
    PCIe
      |
GPU1 RTX 4070
```

问题在于通信。

一个训练步骤：

```
前向
  |
  v
损失
  |
反向
  |
梯度同步
  |
优化器更新
```

反向传播之后：

GPU0 拥有：

```
所有参数的梯度
```

GPU1 拥有：

```
所有参数的梯度
```

它们需要通信：

```
GPU0 <-------> GPU1
```

在数据中心 GPU 上：

```
H100
 |
NVLink
 |
900 GB/s
```

消费级 PCIe：

```
PCIe 4.0 x16
~32 GB/s
```

差距巨大。

所以对于 760M 模型，两块消费级 GPU 可能无法带来 2 倍速度提升。

有时：

```
1 块 GPU：10 小时

2 块 GPU：
计算更快
通信更慢

=> 6-8 小时
```

而不是：

```
5 小时
```

---

## 2. 但你仍然应该学习分布式训练

因为知识是可迁移的。

基础栈：

```
torch.distributed
        |
        v
DDP
        |
        v
DeepSpeed ZeRO
        |
        v
Megatron tensor parallel
        |
        v
大规模集群训练
```

DeepSpeed ZeRO 很有趣，因为它解决了内存冗余问题。

普通数据并行：

GPU0：

```
权重
梯度
优化器状态
```

GPU1：

```
权重
梯度
优化器状态
```

重复。

ZeRO：

GPU0：

```
权重 A
优化器 A
```

GPU1：

```
权重 B
优化器 B
```

状态被分区。([DeepSpeed][1])

对于你的 1.3B 模型：

Adam 内存：

```
参数：
1.3B * 2 字节(fp16)
≈2.6GB

梯度：
≈2.6GB

Adam 状态：
≈10GB+

总计：
15GB+
```

一张 16GB 的卡已经很紧张了。

两块 GPU + ZeRO 会让实验轻松很多。

---

## 3. 你的下一个实验不应该是“训练更大的模型”

我会这样做：

### 阶段 1

拿你现有的 GPT-2 760M。

运行：

```
单 GPU
vs
DDP 2 GPU
vs
DeepSpeed ZeRO-2
```

测量：

```
tokens/秒
GPU 利用率
通信开销
内存
```

制作一个表格。

这本身就是一个很好的工程实验。

---

## 4. GPU 硬件探索实际上很契合

很多 AI 研究者回避硬件。

但历史上：

```
NVIDIA CUDA
        |
        |
AI 爆发
```

那些理解以下内容的人：

```
模型
+
编译器
+
内核
+
硬件
```

非常罕见。

例如：

FlashAttention 不仅仅是一个数学改进。

朴素注意力：

```
QK^T

存储巨大矩阵

softmax

乘以 V
```

内存：

```
O(n^2)
```

FlashAttention：

```
加载小块
计算
丢弃
```

HBM 流量更少。

该算法是围绕 GPU 内存层次结构设计的。

这正是桥梁：

```
Transformer
       |
       v
注意力内核
       |
       v
CUDA
       |
       v
GPU 架构
```

---

## 5. vLLM / SGLang / KV cache 是正确的下一个层次

训练只是一半。

推理有另一个世界。

普通 transformer 生成：

token 1：

```
K,V
```

token 2：

重新计算：

```
K1,V1
K2,V2
```

浪费。

KV cache：

存储：

```
K1,V1
K2,V2
...
```

然后下一个 token 只计算：

```
新 K,V
+
与缓存做注意力
```

vLLM 的 PagedAttention 思想本质上是：

“KV cache 的虚拟内存”。

类似的概念：

```
操作系统虚拟内存
        |
        v
GPU KV cache 管理
```

这是一个很棒的领域。

---

## 6. 关于 ICML 论文

你的担忧是对的：

> 一块 GPU，实验速度慢

但很多好论文并不依赖蛮力。

你的优势：

你可以探索系统 + 模型。

可能的方向：

* 高效训练
* 小模型缩放规律
* 数据集质量
* 推理优化
* 硬件感知训练
* agent 评估

例如：

一个 760M 模型足以研究：

```
数据
架构
优化器
分词
评估
```

你不需要 100B 参数。

---

## 7. 你目前的弱点是评估，而不是训练

我认为这句话很重要：

> 训练完了，大概用agent看看训练质量

这是你可以改进的地方。

一个模型并不是 loss 下降就“完成”了。

例如：

```
训练损失
        |
        v
验证损失
        |
        v
基准测试
        |
        v
定性分析
```

对于代码模型：

```
HumanEval
MBPP
SWE-bench 风格测试
```

对于语言：

```
MMLU
ARC
HellaSwag
```

对于你自己的模型：

创建你自己的评估：

```
100 道编码题
100 道推理题
100 道中英文题
```

这样每个实验都有可衡量的输出。

---

我的看法：

你的 GPU 探索并非分散注意力。它很可能是一条独特的道路。

很多人学习：

```
使用 API
微调
部署
```

你正在走向：

```
训练模型
理解内核
理解 GPU
构建基础设施
```

这更接近 Karpathy / 系统工程师的路径。

下一个实际里程碑我会选择：

```
RTX 4070
        |
        v
GPT-2 760M
        |
        v
PyTorch DDP
        |
        v
DeepSpeed ZeRO-2
        |
        v
分析通信
        |
        v
写笔记
```

一次记录良好的实验，可能比十次随机的模型训练更有价值。

参考文献：

* DeepSpeed ZeRO 文档 ([DeepSpeed][1])
* DeepSpeed 训练 API ([DeepSpeed][2])
* DeepSpeed 流水线/模型并行训练概述 ([deepspeed.ai][3])

[1]: https://deepspeed.readthedocs.io/en/stable/zero3.html?utm_source=chatgpt.com "ZeRO — DeepSpeed 0.19.2 documentation"
[2]: https://deepspeed.readthedocs.io/en/stable/training.html?utm_source=chatgpt.com "Training API — DeepSpeed 0.19.5 documentation"
[3]: https://www.deepspeed.ai/training/?utm_source=chatgpt.com "Training Overview and Features - DeepSpeed"
