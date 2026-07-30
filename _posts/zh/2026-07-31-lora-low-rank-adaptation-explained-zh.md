---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LoRA：低秩适应原理解析
translated: true
type: note
---

## 问题：在LLM中，LoRA是什么意思？

## 答案：

**LoRA = Low-Rank Adaptation（低秩适配）**。它是一种微调大型语言模型（LLM）的技术，通过仅训练少量额外参数，而不是更新所有模型权重。

原论文：LoRA: Low-Rank Adaptation of Large Language Models

---

## 1. 问题：全量微调成本高昂

一个 Transformer 层包含权重矩阵：

```
W ∈ R^(d × d)
```

示例：

Llama-70B：

```
700 亿参数
≈ 140 GB BF16 权重
```

训练时需要：

* 模型权重
* 梯度
* 优化器状态（Adam 保持动量 + 方差）

内存：

```
权重          ~140 GB
梯度          ~140 GB
Adam 状态     ~560 GB

总计          ~840 GB+
```

因此，微调 70B 模型需要庞大的 GPU 集群。

---

## 2. LoRA 的思路

不再修改原始权重：

```
W
```

将其冻结。

添加一个小的更新：

```
W' = W + ΔW
```

但不存储完整的：

```
ΔW ∈ R^(d × d)
```

LoRA 将其分解为：

```
ΔW = B × A
```

其中：

```
A ∈ R^(r × d)

B ∈ R^(d × r)
```

`r` 是秩。

通常：

```
r = 4, 8, 16, 32
```

要小得多。

---

示例：

假设：

```
d = 4096
```

完整更新：

```
4096 × 4096

= 16,777,216 个参数
```

LoRA：

```
r = 8

A：
8 × 4096
= 32,768

B：
4096 × 8
= 32,768

总计：
65,536
```

缩小比例：

```
16M → 65K

~缩小 250 倍
```

---

## 3. 前向传播

标准 Transformer 线性层：

```
x
 |
 v
Linear

y = Wx
```

LoRA：

```
             冻结的
              W
              |
x ----------> Linear --------+
                             |
                             v
                          y1 + y2
                             ^
                             |
x --> A --> B --------------+
       可训练

y2 = BAx
```

数学上：

```
y = Wx + BAx
```

训练期间：

```
W：冻结
A：更新
B：更新
```

只有 LoRA 权重接收梯度。

---

## 4. 为什么低秩有效？

关键观察：

在适配预训练模型时，权重变化通常具有低内在维度。

这意味着：

拥有数十亿参数的模型可能只需要一个小的“方向变化”。

示例：

原始知识：

```
W = 通用英语模型
```

微调：

```
ΔW = 医疗风格调整
```

所需的变化不是随机的。

它位于一个小子空间中：

```
高维空间

        *
       /
      /
-----*------------->
    低秩方向
```

LoRA 学习这个方向。

---

## 5. 实际示例

基础模型：

```
Llama-8B
```

不再保存：

```
llama-8b-finetuned.bin

80 亿参数
```

而是保存：

```
adapter.bin

约 10-100 MB
```

部署：

```
Llama-8B
+
my_lawyer_LoRA

= 律师模型
```

您可以切换适配器：

```
Llama-8B
 |
 +-- coding LoRA
 |
 +-- medical LoRA
 |
 +-- customer service LoRA
 |
 +-- Chinese LoRA
```

一个基础模型，多种性格。

---

## 6. LoRA 与全量微调对比

|                  | 全量微调       | LoRA          |
| ---------------- | -------------- | ------------- |
| 更新             | 所有权重       | 小型适配器    |
| GPU 内存         | 巨大           | 小            |
| 训练速度         | 较慢           | 更快          |
| 质量             | 最优可能       | 接近          |
| 存储             | GB-TB          | MB-GB         |
| 多个领域         | 昂贵           | 容易          |

---

## 7. LoRA 在现代 LLM 训练栈中的应用

典型流程：

```
基础模型
    |
    v
SFT 数据集
    |
    v
LoRA 训练
    |
    v
适配器
    |
    v
合并（可选）
    |
    v
生产模型
```

工具：

* [Hugging Face PEFT](https://github.com/huggingface/peft?utm_source=chatgpt.com)
* [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory?utm_source=chatgpt.com)
* [Axolotl](https://github.com/axolotl-ai-cloud/axolotl?utm_source=chatgpt.com)

---

## 8. LoRA 变体

### QLoRA

量化 LoRA：

```
基础模型：
FP16 → 4-bit

LoRA：
FP16
```

允许：

```
70B 模型
+
单张 48GB GPU
```

训练。

论文：

QLoRA: Efficient Finetuning of Quantized LLMs

---

### DoRA

权重分解 LoRA：

```
W = magnitude × direction
```

提高了质量，更接近全量微调。

---

## 9. 对于您的配置

鉴于您拥有：

* RTX 4070 12GB
* 已训练过 GPT-2 124M
* 正在试验 nanoGPT/vLLM

LoRA 正是下一步。

示例：

```
Qwen3-8B
+
LoRA 适配器
+
您的 SEC 文件数据集
```

您的 RTX 4070 无法全量微调 8B 模型，但可以做：

```
4-bit QLoRA

8B 模型
12GB VRAM
```

大致：

```
基础模型     ~5GB
LoRA         <1GB
优化器       几 GB

可容纳
```

一个最小的训练命令：

```bash
pip install transformers peft bitsandbytes trl
```

概念上：

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=[
        "q_proj",
        "v_proj"
    ]
)

model = get_peft_model(model, config)

model.print_trainable_parameters()
```

输出：

```
trainable params:
~10M

total params:
8B
```

这就是 LoRA 的神奇之处。

参考文献：

* LoRA 论文： [https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)
* QLoRA 论文： [https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)
* Hugging Face PEFT： [https://github.com/huggingface/peft](https://github.com/huggingface/peft)