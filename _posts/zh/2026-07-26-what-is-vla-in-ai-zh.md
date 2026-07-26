---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI中的VLA是什么？
translated: true
type: note
---

**VLA 在 AI 中的全称是什么？**

答案：**VLA = 视觉-语言-动作模型（Vision-Language-Action model）**。

这是一类结合了以下能力的 AI 模型：

* **视觉 (V)** → 理解摄像头拍摄的图像/视频
* **语言 (L)** → 通过自然语言理解指令、推理和概念
* **动作 (A)** → 输出动作以控制智能体（通常是机器人）

基本流程：

```
摄像头图像
     |
     v
[ 视觉编码器 ]
     |
     v
[ 多模态 Transformer / 大语言模型 ]
     |
用户指令：
"拿起红色杯子"
     |
     v
动作标记
     |
     v
机器人控制器
     |
     v
电机指令
```

与大语言模型 (LLM) 的比较：

| 模型                         | 输入        | 输出        |
| ---------------------------- | ----------- | ----------- |
| LLM                          | 文本        | 文本        |
| VLM (视觉-语言模型)          | 图像 + 文本 | 文本        |
| VLA (视觉-语言-动作模型)     | 图像 + 文本 | 机器人动作  |

VLA 模型示例：

* Google DeepMind **RT-2 (Robotics Transformer 2)**

  * 利用来自大型模型的视觉-语言知识，并将其转换为机器人动作。
* Physical Intelligence **π0 (pi-zero)**

  * 一个通用的机器人基础模型。
* NVIDIA **GR00T (Project GR00T)**

  * 人形机器人基础模型。
* OpenAI 的机器人研究也探索了多模态具身智能。

核心思想：

> VLA 本质上是一个 **用于机器人的大语言模型 (LLM)**：它生成的不是下一个文本标记，而是下一个物理动作。

从技术上讲，许多现代 VLA 是通过扩展 Transformer 架构构建的：

```
图像块
      |
视觉 Transformer (ViT)
      |
      +------ 文本标记
      |
      v
大型 Transformer
      |
      v
动作标记
      |
      v
轨迹 / 电机指令
```

一个常见的训练目标是：

[
P(a_t | I, L, a_{<t})
]

其中：

* (I) = 视觉观察
* (L) = 语言指令
* (a_t) = 下一个动作

类似于 GPT：

[
P(x_t | x_{<t})
]

但预测的标记是**动作标记**，而不是一个词。

参考文献：

* [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818?utm_source=chatgpt.com)
* [A Vision-Language-Action Model for General Robot Control (π0)](https://arxiv.org/abs/2410.24164?utm_source=chatgpt.com)
* [NVIDIA Project GR00T](https://www.nvidia.com/en-us/robotics/isaac/gr00t/?utm_source=chatgpt.com)