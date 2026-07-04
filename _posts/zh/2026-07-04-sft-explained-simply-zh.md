---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SFT通俗解释
translated: true
type: note
---

**问题：** 什么是 SFT？我刚刚看到一次 PyTorch 调用，但它底层是如何工作的？

**回答：**

**SFT** 代表 **监督式微调（Supervised Fine-Tuning）**。它是训练或适配大型语言模型（LLM）最简单、最常用的方法。

其核心就是在指令-回复对数据集上进行 **下一个词元预测**。这里没有神奇算法——它本质上与预训练阶段使用的训练流程相同，只不过是在一个更小、经过精心整理的数据集上运行。

例如，假设你的数据集包含：

```text
用户：2 + 2 等于多少？
助手：4
```

模型实际看到的内容类似：

```text
<user>
2 + 2 等于多少？
</user>

<assistant>
4
</assistant>
```

分词器会将其转换为 ID：

```
[123, 456, 789, 234, ...]
```

模型预测过程如下：

```
输入：
2 + 2 等于

预测：
多

下一步：

输入：
2 + 2 等于多

预测：
少

...

最终：

输入：
助手：

预测：
4
```

它通过最小化对助手回复的预测误差来进行学习。

---

## 底层实现

假设你有

```python
input_ids = tokenizer(text).input_ids
```

模型会执行

```python
logits = model(input_ids)
```

其中

```
input_ids
     ↓
嵌入层
     ↓
Transformer 块
     ↓
线性投影
     ↓
logits
```

输出形状为

```
(batch, sequence_length, vocab_size)
```

对于一个 5 万词元的词表：

```
(8, 512, 50000)
```

每个位置预测下一个词元。

---

## 损失计算

PyTorch 通常使用

```python
loss = F.cross_entropy(
    logits.view(-1, vocab_size),
    labels.view(-1)
)
```

其内部实现为

```
Softmax
↓
负对数似然
↓
对所有词元取平均
```

损失为

[
-\log(p(\text{正确词元}))
]

如果正确的下一个词元是

```
"dog"
```

并且模型预测为

```
cat : 0.20
dog : 0.60
bird: 0.10
```

那么

```
loss = -log(0.6)
```

如果它预测为

```
dog : 0.99
```

损失就会变得非常小。

---

## 为什么叫“监督式”？

因为人类提供了期望的输出。

示例：

```
问题：
如何对列表进行排序？

期望答案：
使用 Python 的 sorted() 函数...
```

模型被直接告知正确的响应应该是什么。

这与强化学习不同，在强化学习中，模型只收到奖励信号，而不是确切的目标输出。

---

## 对提示进行掩码

现代 SFT 中的一个重要细节是，我们通常 **不会在用户的提示上训练**。相反，我们只计算助手回复部分的损失。

例如：

```text
用户：
给我讲个笑话。

助手：
为什么鸡要过马路？
```

标签可能如下：

```
用户词元       -> -100
助手词元       -> 实际词元 ID
```

在 PyTorch 中：

```python
labels = input_ids.clone()
labels[user_part] = -100
```

`-100` 值告诉 `CrossEntropyLoss` 忽略那些位置。

这意味着模型 **以提示为条件**，但只根据它预测助手回复的准确度来受到惩罚。

---

## 反向传播

一旦计算出损失：

```
loss
 ↓
backward()
 ↓
计算梯度
 ↓
optimizer.step()
 ↓
更新权重
```

Transformer 中的每个权重都会通过梯度下降进行微调。

---

## 实际的 PyTorch 训练循环

简化版本如下：

```python
for batch in dataloader:
    outputs = model(
        input_ids=batch["input_ids"],
        labels=batch["labels"]
    )

    loss = outputs.loss

    loss.backward()

    optimizer.step()

    optimizer.zero_grad()
```

在

```python
outputs = model(...)
```

内部，Hugging Face 模型通常会执行类似以下操作：

```python
logits = transformer(input_ids)

shift_logits = logits[:, :-1]
shift_labels = labels[:, 1:]

loss = F.cross_entropy(
    shift_logits.reshape(-1, vocab_size),
    shift_labels.reshape(-1),
    ignore_index=-100
)
```

标签会偏移一个位置，因为模型预测的是 **下一个** 词元。

---

## Hugging Face 如何隐藏复杂性

当你编写：

```python
outputs = model(
    input_ids=input_ids,
    labels=labels
)
```

模型会自动：

1. 通过 Transformer 执行前向传播。
2. 移位 logits 和标签以进行下一个词元预测。
3. 计算交叉熵损失。
4. 对掩码位置应用 `ignore_index=-100`。
5. 同时返回 `loss` 和 `logits`。

这就是为什么 SFT 训练脚本看起来非常简单。

---

## 整体流程

```
指令数据集
        │
        ▼
分词器
        │
        ▼
词元 ID
        │
        ▼
Transformer 前向传播
        │
        ▼
Logits
        │
        ▼
偏移一个词元
        │
        ▼
交叉熵损失
        │
        ▼
反向传播
        │
        ▼
AdamW 优化器
        │
        ▼
更新后的模型权重
```

总之，**SFT 本质上与预训练阶段使用的下一个词元预测目标相同**，但应用于高质量的指令遵循样本。关键区别在于数据（指令-回复对而非原始文本），以及通常对提示进行掩码，使得只有助手的回复贡献于训练损失。
