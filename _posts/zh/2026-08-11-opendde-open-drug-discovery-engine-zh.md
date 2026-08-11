---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenDDE：开放药物发现引擎
translated: true
type: note
---

Question: `aurekaresearch/OpenDDE` 简介

Answer:

[OpenDDE GitHub 仓库](https://github.com/aurekaresearch/OpenDDE?utm_source=chatgpt.com) 是一个**开源的 AI 基础模型，用于药物发现**，专注于**全原子生物分子建模**。项目名称意为 **Open Drug Discovery Engine**（开源药物发现引擎）。它旨在使类似于 Google DeepMind 的 AlphaFold 3 风格的系统更加开放和易用。（[arXiv][1]）

核心思想：

> 不仅是预测蛋白质结构，而是构建一个通用的分子推理引擎，能够理解蛋白质、DNA、RNA、配体及其相互作用。

（[GitHub][2]）

---

## 1. 背景：为什么这很重要

传统药物发现：

```
目标蛋白
      |
      v
寻找候选分子
      |
      v
实验室实验
      |
      v
优化药物
      |
      v
临床试验
```

非常昂贵：

* 数十亿美元
* 10 年以上
* 高失败率

AI 改变了早期阶段：

```
蛋白质序列
       +
药物分子
       |
       v
AI 分子模型
       |
       +--> 结构预测
       +--> 结合预测
       +--> 分子设计
       +--> 优化
```

OpenDDE 试图成为这个“基础模型”层。

---

## 2. “全原子生物分子基础模型”是什么意思？

普通语言模型：

```
文本 token
   |
Transformer
   |
下一个 token 预测
```

蛋白质 AI 模型：

```
原子 / 残基
        |
几何神经网络
        |
3D 分子推理
        |
结构 / 相互作用预测
```

分子不仅仅是一个序列。

示例：

蛋白质：

```
M K V L S A ...
```

仅序列是 1D 的。

但真实对象：

```
          O
          |
    C --- C
   /       \
 N         C
   \       /
    3D 结构
```

模型需要理解：

* 原子之间的距离
* 角度
* 化学键
* 对称性
* 物理约束

---

## 3. 与 AlphaFold 3 的关系

OpenDDE 明确基于以下项目的思想/组件构建：

* AlphaFold 3
* OpenFold
* Protenix
* ColabFold

（[GitHub][3]）

重要的演变：

### AlphaFold 2

主要是：

```
蛋白质序列
        |
        v
蛋白质 3D 结构
```

### AlphaFold 3 / OpenDDE

更通用：

```
蛋白质
DNA
RNA
小分子配体
离子
      |
      v
复合物结构
```

示例：

药物分子：

```
     阿司匹林
        |
        v
蛋白质结合口袋
        |
        v
预测相互作用
```

---

## 4. 模型架构（高层）

流程大致如下：

```
输入 JSON
    |
    v
序列编码器
    |
    v
原子级表示
    |
    v
几何推理网络
    |
    v
扩散 / 生成式结构采样
    |
    v
3D 复合物预测
```

类似于现代扩散模型：

```
噪声结构
       |
       v
去噪网络
       |
       v
有效的分子结构
```

---

## 5. 使用示例

安装：

```bash
uv venv --python 3.11

source .venv/bin/activate

uv pip install \
  --torch-backend cu126 \
  "opendde[gpu]"

opendde doctor
```

（[GitHub][4]）

运行：

```bash
opendde pred \
  -i input.json \
  -o ./output \
  -n opendde_v1
```

（[GitHub][4]）

输入示例：

```json
[
 {
  "name": "protein_test",
  "modelSeeds": [101],
  "sequences": [
    {
      "proteinChain": {
        "sequence": "ACDEFGHIK",
        "count": 1
      }
    }
  ]
 }
]
```

输出：

```
output/
 └── protein_test/
      └── predictions/
            structure.cif
```

---

## 6. 硬件需求

这不像运行 Qwen 7B 那样简单。

它要重得多。

官方支持：

* NVIDIA CUDA 12.6
* GPU 推理
* 可选 cuEquivariance 内核
* 多 GPU Fold-CP 模式

（[GitHub][4]）

对于大型复合物：

```
GPU0
 |
GPU1
 |
GPU2
 |
GPU3

上下文并行推理
```

他们提供 4-GPU 模式：

```bash
torchrun \
 --nproc_per_node 4 \
 -m runner.batch_inference pred ...
```

（[Hugging Face][5]）

你的 RTX 4070 12GB：

* 适合学习
* 可能不足以进行严肃的生产推理
* 可用于阅读代码/小型实验

一个现实的配置：

```
24GB GPU：
   小型实验

48GB GPU：
   可用

80GB A100/H100：
   严肃工作负载

多 GPU：
   大型复合物
```

---

## 7. 为什么这个项目对 AI 工程师来说很有趣

它是下一波浪潮的一个好例子：

之前：

```
LLM：
 文本 -> 智能
```

现在：

```
基础模型：

文本
图像
视频
机器人
生物学
化学
物理学
```

生物学可能成为最大的 AI 应用之一。

模式是相似的：

GPT：

```
互联网文本
     |
大型 Transformer
     |
推理
```

OpenDDE：

```
生物数据
     |
几何基础模型
     |
分子推理
```

---

## 8. 如果你想研究代码

推荐的阅读顺序：

```
README.md
   |
docs/inference_instructions.md
   |
输入 JSON 格式
   |
模型代码
   |
训练论文
```

仓库：

[OpenDDE GitHub 仓库](https://github.com/aurekaresearch/OpenDDE?utm_source=chatgpt.com)

论文：

[Folding, Reasoning, and Scaling with Open-source Drug Discovery Engine](https://arxiv.org/abs/2607.03787?utm_source=chatgpt.com)

---

我的看法：OpenDDE 之所以有趣，是因为它展示了**“基础模型”正在逃离 NLP**。GPT 的相同缩放理念正在进入科学领域：学习世界的表示，然后用于预测、生成和优化。对于已经训练过 GPT/nanoGPT 风格模型的人来说，概念上的跳跃主要是从 **token 空间 → 3D 几何空间**。

[1]: https://arxiv.org/abs/2607.03787?utm_source=chatgpt.com "Folding, Reasoning, and Scaling with Open-source Drug Discovery Engine"
[2]: https://github.com/aurekaresearch/OpenDDE?utm_source=chatgpt.com "GitHub - aurekaresearch/OpenDDE: An Open-source Drug Discovery Engine · GitHub"
[3]: https://github.com/aurekaresearch/OpenDDE/blob/main/README.md?utm_source=chatgpt.com "OpenDDE/README.md at main · aurekaresearch/OpenDDE · GitHub"
[4]: https://github.com/aurekaresearch/OpenDDE/blob/main/docs/inference_instructions.md?utm_source=chatgpt.com "OpenDDE/docs/inference_instructions.md at main · aurekaresearch/OpenDDE · GitHub"
[5]: https://huggingface.co/aurekaresearch/OpenDDE?utm_source=chatgpt.com "aurekaresearch/OpenDDE · Hugging Face"
