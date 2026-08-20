---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Inkling-Small：高效MoE模型
translated: true
type: note
---

## 问题：介绍 Thinking Machines Lab 的 **Inkling-Small**

## 答案

Thinking Machines Lab 发布了 **Inkling-Small**，这是一个开源权重、多模态的混合专家（MoE）语言模型，旨在将前沿模型的能力浓缩到更便宜、更易部署的规模中。（[Thinking Machines Lab][1]）

核心理念：

> **将约 1T 参数的前沿模型（Inkling）的有用能力压缩到更小的激活模型中，使其对开发者更实用。**（[Thinking Machines Lab][2]）

---

## 1. 模型架构

Inkling-Small：

```
总参数量：     276B
激活参数量：     12B
架构：          稀疏 MoE Transformer
上下文窗口：       高达 1M tokens
输入：               文本 + 图像 + 音频
输出：               文本
许可证：               Apache 2.0
```

（[Thinking Machines Lab][3]）

关键数字是 **12B 激活参数**，而不是 276B。

推理过程中：

```
输入 token
    |
    v
路由器
    |
    +--> 专家 17
    +--> 专家 92
    +--> 专家 201
    +--> ...
    |
    v
输出
```

只有一小部分专家执行。

类似理念：

* Mixtral 8x7B
* DeepSeek MoE 模型
* Switch Transformer

区别于：

```
密集模型：

每个 token
   |
   v
所有参数执行

70B 模型 = 70B 计算量
```

MoE：

```
每个 token
   |
   v
选择专家

总计 276B
但计算量 ~12B
```

这带来了：

* 更大的知识容量
* 更低的推理成本
* 更好的扩展性

---

## 2. 为什么值得关注？

AI 行业正从：

```
更大的模型
      |
      v
更多参数
```

转向：

```
更好的架构
      |
      v
高效的推理和智能体
```

Inkling-Small 重点关注：

### A. 推理能力

它支持**可控的思考深度**。

意思是：

```
廉价模式：

问题
  |
  v
少量推理步骤
  |
答案


高成本模式：

问题
  |
  v
长链思维
  |
更好的答案
```

你可以权衡：

```
延迟 / 成本

       与

准确性
```

（[Thinking Machines Lab][1]）

---

### B. 智能体编码

该模型针对以下场景优化：

* 编码智能体
* 工具使用
* 终端任务
* RAG 系统

据报道：

* SWE-bench Verified：约 80% 范围

这意味着它可以自主修改代码仓库。（[Thinking Machines Lab][1]）

典型工作流程：

```
用户：

"修复这个 bug"

       |
       v

Inkling-Small

       |
       +-- 读取仓库
       |
       +-- 运行测试
       |
       +-- 编辑文件
       |
       +-- 验证
```

---

### C. 原生多模态

不同于旧的 LLM + 独立视觉模型：

```
旧方式：

图像
 |
视觉编码器
 |
LLM


新方式：

文本 tokens
图像 tokens
音频 tokens

       |
       v

同一 transformer
```

Inkling-Small 直接处理：

* 文本
* 图像
* 音频

（[Thinking Machines Lab][4]）

---

## 3. 与其他开源模型对比

大致定位：

| 模型            | 总参数量 | 激活参数量  | 类型   |
| --------------- | -------- | ----------- | ------ |
| Llama 3.1 405B  | 405B     | 405B        | 密集   |
| Qwen3 235B      | 235B     | 235B        | 密集   |
| DeepSeek MoE    | 大       | 较小激活    | MoE    |
| Inkling         | 975B     | 41B         | MoE    |
| Inkling-Small   | 276B     | 12B         | MoE    |

（[Thinking Machines Lab][2]）

Inkling-Small 的诀窍：

```
知识容量 ≈ 巨大模型

推理成本 ≈ 12B 模型
```

---

## 4. 硬件影响

对于本地部署：

### BF16

276B 权重：

```
276B * 2 字节

≈ 552GB 显存
```

普通 GPU 无法实现。

但由于 MoE 推理仅激活 12B：

你仍然需要存储所有专家。

典型部署：

```
8x H100 / H200
或
多 GPU 服务器
```

对于消费级 GPU：

```
RTX 4090 24GB
RTX 5090 32GB
RTX 6000 Ada 48GB

不足以加载完整 BF16
```

量化版本有所帮助：

```
NVFP4 / FP8

内存占用显著减小
```

（[Hugging Face][5]）

---

## 5. 这对 AI 工程师为何重要

对于构建智能体的人来说，这比基准测试分数更重要。

未来架构：

```
        用户
         |
         v
    AI 智能体
         |
 +-------+-------+
 |               |
推理           工具
模型          浏览器
 |               |
编码          API
模型          数据库
```

小而高效的前沿模型将成为智能体的"CPU"。

示例：

* 编码助手
* 企业自动化
* 客户支持智能体
* AI 导师
* 研究智能体

---

## 6. 与你本地实验的对比

考虑到你训练 GPT-2/nanochat 的背景：

Inkling-Small 展示了 GPT 式扩展之后的发展方向。

GPT-2：

```
密集 Transformer

124M 参数
760M 参数
```

现代前沿：

```
MoE Transformer

276B 参数
12B 激活参数
```

发展历程：

```
GPT-2 (2019)

所有参数始终激活


↓

GPT-3

更大的密集模型


↓

Mixtral / DeepSeek / Inkling

条件计算


↓

未来模型

推理 + 智能体 + 多模态
```

核心研究问题从：

> "如何让模型变得更大？"

转变为：

> "如何只在需要智能的地方投入计算力？"

---

参考文献：

* （[Thinking Machines Lab][1]）
* （[Thinking Machines Lab][2]）
* （[Thinking Machines Lab][4]）
* （[Hugging Face][5]）

[1]: https://thinkingmachines.ai/news/inkling-small/?utm_source=chatgpt.com "Introducing Inkling-Small - Thinking Machines Lab"
[2]: https://thinkingmachines.ai/news/introducing-inkling/?utm_source=chatgpt.com "Inkling: Our Open-Weights Model - Thinking Machines Lab"
[3]: https://thinkingmachines.ai/inkling/?utm_source=chatgpt.com "Inkling - Thinking Machines Lab"
[4]: https://thinkingmachines.ai/model-card/inkling-small/?utm_source=chatgpt.com "Inkling-Small Model Card - Thinking Machines Lab"
[5]: https://huggingface.co/thinkingmachines/Inkling-Small?utm_source=chatgpt.com "thinkingmachines/Inkling-Small · Hugging Face"