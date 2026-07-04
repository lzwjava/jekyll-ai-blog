---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SFT将下一个词元模型转化为聊天机器人
translated: true
type: note
---

问题：SFT（监督微调）如何将像 nanoGPT 这样的下一个词元预测模型转变为聊天机器人？我们是直接训练 JSON 格式的对话，还是将其转换为 `User:` / `Assistant:` 文本，并训练模型来预测助手的回答？

回答：

是的，这基本上就是这个思路。关键点在于：

> **即便是聊天模型，本质上仍然是下一个词元预测模型。**

神经网络本身并没有发生根本性变化。唯一改变的是**训练数据的格式**。

## 步骤一：预训练（nanoGPT）

在 nanoGPT 中，你使用的可能是纯文本：

```text
The capital of France is Paris.
```

模型看到的是

```
输入： The capital of France is
目标： capital of France is Paris .
```

或者更准确地说

```
输入词元：
The capital of France is Paris .

预测：

The -> capital
capital -> of
of -> France
France -> is
is -> Paris
Paris -> .
```

每个词元都预测下一个词元。

---

## 步骤二：SFT 数据集

假设你有如下 JSON 数据：

```json
{
  "messages": [
    {
      "role": "user",
      "content": "2+2 等于多少？"
    },
    {
      "role": "assistant",
      "content": "4。"
    }
  ]
}
```

**模型并非直接基于 JSON 对象进行训练。**

相反，JSON 会被转换为文本。

例如，

```text
<|user|>
2+2 等于多少？

<|assistant|>
4。
```

或者

```text
User: 2+2 等于多少？
Assistant: 4。
```

或者对于某些模型：

```text
<|im_start|>user
2+2 等于多少？
<|im_end|>

<|im_start|>assistant
4。
<|im_end|>
```

每个模型家族都有自己特定的**聊天模板**。

---

## 步骤三：词元化

格式化之后，

```text
User: 2+2 等于多少？

Assistant: 4。
```

会变成类似这样的词元：

```
[User]
[:]
[2]
[+]
[2]
[等于]
[多少]
[？]

[Assistant]
[:]

[4]
[。]
```

Transformer 并不理解这些词元在语义上是“角色”。它只会看到词元序列。

---

## 步骤四：损失掩码（关键部分）

大多数 SFT 训练**不会**对用户的词元计算损失。

示例：

```
User: 2+2 等于多少？
Assistant: 4。
```

内部会变成

```
输入：

User:
2
+
2
等于
多少
？
Assistant:
4
。
```

标签会被掩码，变为：

```
User        -> 忽略
:           -> 忽略
2           -> 忽略
+           -> 忽略
2           -> 忽略
等于        -> 忽略
多少        -> 忽略
？          -> 忽略
Assistant   -> 忽略

4           -> 预测
。          -> 预测
```

在许多实现中：

```
labels =
[-100,
 -100,
 -100,
 ...
 -100,
 token("4"),
 token("。")]
```

其中 `-100` 告诉损失函数（例如 PyTorch 中的交叉熵损失）忽略这些位置。

这教会模型：

> 根据已有的对话历史，生成助手的回复。

---

## 步骤五：推理

在推理过程中，你输入

```text
User: 给我讲个笑话。

Assistant:
```

模型会预测出

```
为什么
鸡
要
过
马路
...
```

因为在 SFT 阶段，它见过数百万个以

```
Assistant:
```

之后紧跟回答的示例。

因此它已经学会了这种模式。

---

## 多轮对话

训练数据也可以像这样：

```text
User: 你好

Assistant: 你好！

User: 谁发明了 Python？

Assistant: Guido van Rossum。
```

损失通常**仅对助手的消息**进行计算。

概念上：

```
User: 你好                     忽略

Assistant: 你好！              训练

User: 谁发明了 Python？        忽略

Assistant: Guido van Rossum。  训练
```

这教会模型如何在多轮对话中维持上下文。

---

## 为什么 JSON 仍然有用

JSON 格式主要用于组织数据集：

```json
[
  {"role":"system","content":"你很有帮助。"},
  {"role":"user","content":"你好"},
  {"role":"assistant","content":"你好！"}
]
```

在训练之前，预处理步骤会应用模型的聊天模板，生成一个单一的文本序列，例如

```text
<System>
你很有帮助。

<User>
你好

<Assistant>
你好！
```

然后，这段文本会被词元化，并用于下一个词元预测。

---

## 与 nanoGPT 的联系

这是关键的联系：

**预训练**

```
维基百科文章

↓

预测下一个词元
```

**SFT**

```
User:
问题

Assistant:
回答

↓

预测助手的下一个词元
```

训练目标仍然完全相同：**下一个词元预测**。唯一的区别是：

* 现在的输入包含角色标记（`User`、`Assistant` 或特殊的聊天词元）。
* 损失通常被掩码，只有助手的词元参与训练。
* 数据集由对话组成，而不是纯文本。

所以你的理解是正确的：对话 JSON 被转换为格式化的文本序列，进行词元化，然后模型再次通过下一个词元预测进行训练。SFT 中主要的附加技术是**损失掩码**，它确保模型学会生成助手的回答，而不是简单地预测提示中的每一个词元。