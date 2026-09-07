---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MiniSGL代码中的张量并行
translated: true
type: note
---

Question: 在这段 MiniSGL 代码中，`tp` 是什么意思？

Answer: **`TP` 代表 Tensor Parallelism（张量并行）**。

在 LLM 推理/训练代码中，它通常表示将模型的计算拆分到多个 GPU 上。

例如：

```python
from minisgl.distributed import get_tp_info
```

`get_tp_info()` 很可能返回关于 **张量并行组** 的信息，例如：

```text
tp_size   = 4    # 4 个 GPU 参与
tp_rank   = 0    # 当前进程是 GPU 0
```

概念上：

```text
                Transformer 层
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
            GPU 0    GPU 1    GPU 2    GPU 3
            TP rank  TP rank  TP rank  TP rank
              │        │        │        │
              └────────┴────────┴────────┘
                       │
                    合并
```

对于一个线性层：

$$
Y = XW
$$

通过张量并行，你可以将 `W` 拆分到多个 GPU 上：

$$
W = [W_0, W_1, W_2, W_3]
$$

因此每个 GPU 计算：

$$
Y_i = XW_i
$$

然后将输出合并。

所以在你的代码中：

```python
tp = get_tp_info()
```

可以理解为：

> **“告诉我当前进程如何参与 Tensor Parallelism（张量并行）的信息。”**

而：

```python
div_even(...)
```

很可能与**在 TP ranks 之间均匀划分**工作/张量有关。

常见的 LLM 并行词汇表：

```text
TP = Tensor Parallelism（张量并行）      ← 将张量/层拆分到多个 GPU
PP = Pipeline Parallelism（流水线并行）  ← 将层拆分到多个 GPU
DP = Data Parallelism（数据并行）        ← 将批次拆分到多个 GPU
EP = Expert Parallelism（专家并行）      ← 将 MoE 专家拆分到多个 GPU
CP = Context Parallelism（上下文并行）   ← 将序列/上下文拆分到多个 GPU
```

我还可以逐行讲解一个真实的 `MiniSGL` TP 实现，并精确展示张量在哪里被拆分以及 NCCL 通信发生在哪里。
