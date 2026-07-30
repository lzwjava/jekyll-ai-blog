---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PEFT高效微调大语言模型
translated: true
type: note
---

问题：Hugging Face PEFT（`huggingface/peft`）介绍

答案：

Hugging Face PEFT（**参数高效微调**）是在不更新全部模型权重的情况下适配大语言模型的主要库。

仓库：[Hugging Face PEFT GitHub](https://github.com/huggingface/peft?utm_source=chatgpt.com)

核心思想：

> 全量微调：更新数十亿参数。
> PEFT：冻结基础模型，训练极少的额外参数。

示例：

```
Llama/Qwen 模型
        |
        | 冻结
        v
+----------------+
| 预训练 LLM     |
| 70亿参数       |
+----------------+
        |
        +---- 添加 LoRA 适配器
              |
              v
        训练约 1 千万参数
```

而不是：

```
7,000,000,000 参数
全部需要梯度
```

你训练的是：

```
约 5,000,000 - 50,000,000 参数
```

成本低得多。

---

## 为什么需要 PEFT

假设你拥有：

* Qwen3-8B
* Llama-3-8B
* Mistral-7B

全量微调：

```
80亿参数 × fp16
≈ 16GB 权重

优化器状态 (Adam)
≈ 32GB+

梯度
≈ 16GB+

总计：
60GB-100GB VRAM
```

普通 GPU 难以承受。

使用 LoRA：

```
基础模型：
80亿参数
冻结

LoRA：
1000万-1亿参数
可训练
```

你的 RTX 4070 12GB 也能进行有效的微调。

---

# PEFT 支持的主要算法

## 1. LoRA（最流行）

低秩适配。

原始权重：

```
W
```

不直接修改 W：

```
W' = W + ΔW
```

LoRA 表示为：

```
ΔW = A × B
```

其中：

```
W:
4096 × 4096

A:
4096 × r

B:
r × 4096

r = 8 / 16 / 32
```

示例：

```
4096 * 4096
= 1600万参数

LoRA 秩为 8：

4096*8 + 8*4096
= 6.5万参数
```

大幅减少。

---

## 2. QLoRA

组合：

```
4-bit 量化基础模型
+
LoRA 适配器
```

架构：

```
         冻结
       4-bit Qwen
            |
            |
        前向传播
            |
            v
       LoRA 适配器
            |
            |
       仅此处有梯度
```

常用技术栈：

```
transformers
      |
      |
     PEFT
      |
      |
 bitsandbytes
```

示例：

```python
from transformers import AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-8B"
)

config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=[
        "q_proj",
        "v_proj"
    ],
)

model = get_peft_model(model, config)

model.print_trainable_parameters()
```

输出：

```
可训练参数：
约 1 千万

全部参数：
80亿

可训练比例：
0.1%
```

---

# PEFT 架构

高层结构：

```
transformers
     |
     |
     v
+-------------+
| 基础模型    |
| Llama/Qwen  |
+-------------+
       |
       |
       v

+-------------+
| PEFT 封装器 |
+-------------+
       |
       |
       +---- LoRA
       |
       +---- Prefix tuning
       |
       +---- Prompt tuning
       |
       +---- IA3
```

---

# 其他 PEFT 方法

## Prefix tuning

不修改权重：

添加虚拟 token：

```
输入：

[system][user][question]

变为：

[prefix tokens][system][user][question]
```

仅训练 prefix 嵌入。

---

## Prompt tuning

更小：

```
训练：

soft prompt embeddings

而不是模型权重
```

---

## IA3

调整激活值：

```
hidden_state * learned_vector
```

非常小。

---

# 典型的现代 LLM 训练流程

如今许多开源模型采用：

```
预训练
    |
    |
    v
基础模型
    |
    |
    +---- SFT
    |       |
    |       +-- PEFT LoRA
    |
    |
    +---- RLHF / DPO / GRPO
            |
            +-- PEFT
```

示例：

```
Qwen3-8B base
       |
       |
       v
指令数据集
       |
       |
       v
LoRA SFT
       |
       |
       v
Qwen3-8B-my-domain
```

---

# 针对你的配置（RTX 4070 12GB）

PEFT 正是适合探索的工具。

好的实验：

## 1. 微调一个小型编码模型

```
Qwen3-4B
+
LoRA
+
你的 Java/Python 代码数据集
```

## 2. 推理过程训练

你之前问过关于 RL/推理训练的问题。

一个实际路径：

```
基础模型
(Qwen3-8B)

        |
        |
        v

使用推理轨迹进行 SFT
        |
        |
        v

LoRA 适配器

        |
        |
        v

GRPO/DPO
```

你不需要重新训练整个模型。

---

# 2026 年最小训练技术栈

大多数人使用：

```
transformers
      +
datasets
      +
peft
      +
trl
      +
accelerate
      +
bitsandbytes
```

示例：

```
pip install transformers peft trl accelerate bitsandbytes
```

---

# PEFT 如何融入你的学习路径

鉴于你已经：

* 从零训练了 GPT-2 124M
* 玩过 nanoGPT
* 在本地运行了 Qwen 模型
* 拥有 RTX 4070

下一步合理的跳跃是：

```
nanoGPT
   |
   |
   v
transformers 内部机制
   |
   |
   v
PEFT LoRA
   |
   |
   v
TRL (DPO/GRPO)
   |
   |
   v
智能体 / 模型对齐
```

PEFT 不是关于“从零训练一个模型”。

它是关于**将通用 LLM 低成本地变成你的专用模型**。

参考资料：

* Hugging Face PEFT GitHub：[https://github.com/huggingface/peft](https://github.com/huggingface/peft)
* LoRA 论文：[https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)
* QLoRA 论文：[https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)
