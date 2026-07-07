---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大型语言模型训练流程中的有监督微调
translated: true
type: note
---

问题：LLM中的SFT是什么？

答案：

**SFT（监督微调）** 是这样一个阶段：你使用标准的监督学习，在（**提示，回答**）数据对上训练一个预训练语言模型。

从数学上讲，它仍然是**下一个词元预测**，只不过训练数据是高质量的指令数据，而非互联网文本。

---

## LLM 训练流程

```
原始互联网文本
        │
        ▼
预训练
（下一个词元预测）
        │
        ▼
基础模型
        │
        ▼
SFT
（指令数据集）
        │
        ▼
指令模型
        │
        ▼
偏好优化
（RLHF / DPO / GRPO / 等）
        │
        ▼
对话模型
```

---

## 在预训练期间

模型看到的内容

```
法国的首都是巴黎。

Python 是一种编程语言。

...
```

目标函数：

[
L = -\sum \log P(x_t|x_{<t})
]

没有什么特别的。

模型只是预测下一个词元。

---

## 在 SFT 期间

现在你的数据集看起来像这样

```json
{
    "instruction": "翻译成法语",
    "input": "你好",
    "output": "Bonjour"
}
```

或者

```text
用户：
如何在 Python 中反转一个列表？

助手：
使用 list.reverse() 或 reversed()。
```

训练样本变成

```
<用户>
如何在 Python 中反转一个列表？
</用户>

<助手>
使用 list.reverse() 或 reversed()。
</助手>
```

损失**仅计算在助手的词元上**。

---

## 掩码

假设词元是

```
用户：
你好吗？

助手：
我很好。
```

训练标签

```
用户：
X X X X X

助手：
我很好。
```

其中

```
X = ignore_index (-100)
```

损失是

```
预测 "我"
预测 "很"
预测 "好"
```

而不是

```
预测 用户：
预测 你
预测 好
...
```

在 PyTorch 中

```python
labels = input_ids.clone()

labels[user_tokens] = -100
```

然后

```python
loss = cross_entropy(
    logits.view(-1, vocab_size),
    labels.view(-1)
)
```

---

## SFT 为什么有效？

预训练教会

> “语言看起来是什么样子。”

SFT 教会

> “助手应该如何回应。”

示例：

基础模型

```
Q：2+2 等于多少？

这个问题问的是...
```

经过 SFT 后

```
用户：2+2 等于多少？

助手：4
```

模型学会了对话格式和回答风格。

---

## 示例数据集

一个 SFT 示例：

```json
{
  "messages": [
    {
      "role": "user",
      "content": "用 Python 写一个斐波那契数列。"
    },
    {
      "role": "assistant",
      "content": "def fib(n): ..."
    }
  ]
}
```

成千上万个这样的示例会被拼接起来并进行词元化。

---

## 训练循环

与预训练相比，变化非常小。

```python
for batch in dataloader:

    logits = model(batch["input_ids"])

    loss = cross_entropy(
        logits,
        batch["labels"]   # 用 -100 掩码
    )

    loss.backward()
    optimizer.step()
```

模型架构是相同的。

唯一不同的是**训练数据**和**标签掩码**。

---

## 常见的 SFT 数据集

常用的开放数据集包括：

* OpenAssistant 对话
* Hugging Face H4 数据集
* LMSYS Chat 数据集
* OpenMathInstruct
* Tulu
* 来自 OpenAI、Anthropic 和 Google 等公司的专有指令数据集。

---

## SFT 与 RLHF 与 DPO 的比较

| 方法      | 训练信号                             | 目标                                         |
| --------- | -------------------------------------- | -------------------------------------------- |
| 预训练    | 互联网文本                             | 学习语言和世界知识                           |
| SFT       | 人工编写的示例                         | 学习遵循指令                                 |
| RLHF      | 奖励模型 + 强化学习                    | 根据人类偏好优化回答                         |
| DPO       | 偏好回答 vs 非偏好回答对               | 无需强化学习，直接学习偏好                   |

SFT 通常是**后训练的第一阶段**，因为它能在偏好优化之前提供一个强大的监督式初始化。

参考文献：

* [TRL（Transformer 强化学习）文档](https://huggingface.co/docs/trl?utm_source=chatgpt.com)
* [Hugging Face LLM 课程 – 监督微调](https://huggingface.co/learn/llm-course?utm_source=chatgpt.com)
* [Stanford Alpaca 论文与项目](https://crfm.stanford.edu/2023/03/13/alpaca.html?utm_source=chatgpt.com)
