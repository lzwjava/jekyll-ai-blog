---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tensor Parallelism in MiniSGL Code
translated: false
type: note
---

Question: What does `tp` mean in this MiniSGL code?

Answer: **`TP` stands for Tensor Parallelism**.

In LLM inference/training code, it usually means splitting a model's computation across multiple GPUs.

For example:

```python
from minisgl.distributed import get_tp_info
```

`get_tp_info()` likely returns information about the **tensor-parallel group**, such as:

```text
tp_size   = 4    # 4 GPUs participate
tp_rank   = 0    # this process is GPU 0
```

Conceptually:

```text
                Transformer layer
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
            GPU 0    GPU 1    GPU 2    GPU 3
            TP rank  TP rank  TP rank  TP rank
              │        │        │        │
              └────────┴────────┴────────┘
                       │
                    combine
```

For a linear layer:

$$
Y = XW
$$

with tensor parallelism, you can split `W` across GPUs:

$$
W = [W_0, W_1, W_2, W_3]
$$

so each GPU computes:

$$
Y_i = XW_i
$$

and then the outputs are combined.

So in your code:

```python
tp = get_tp_info()
```

think:

> **"Give me the information about how this process participates in Tensor Parallelism."**

And:

```python
div_even(...)
```

is probably related to dividing work/tensors **evenly among TP ranks**.

The common LLM parallelism vocabulary is:

```text
TP = Tensor Parallelism       ← split tensors/layers across GPUs
PP = Pipeline Parallelism     ← split layers across GPUs
DP = Data Parallelism         ← split batches across GPUs
EP = Expert Parallelism       ← split MoE experts across GPUs
CP = Context Parallelism      ← split sequence/context across GPUs
```

I can also walk through a real `MiniSGL` TP implementation line-by-line and show exactly where the tensor gets split and where the NCCL communication happens.