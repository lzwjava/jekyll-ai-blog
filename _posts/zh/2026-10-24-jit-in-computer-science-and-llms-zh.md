---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 计算机科学与大语言模型中的JIT
translated: true
type: note
---

**问题：** 在计算机科学中，特别是在 LLMs 的背景下，“JIT”是什么意思？

---

**答案：**

JIT 代表 **Just-In-Time**（即时编译）。它出现在与您的问题相关的两个重叠方面：

---

### 1. 一般计算机科学 — JIT 编译

JIT 编译是一种在运行时（就在执行之前）**编译代码**的技术，而不是预先编译（AOT）。不是在运行前将所有内容预先编译为机器代码，而是运行时根据需要“即时”编译代码。

**经典例子：**

- **JVM (Java)** — Java 字节码在运行时被 JIT 编译为本地机器代码
- **V8 (JavaScript)** — Chrome 的引擎 JIT 编译 JS 以提高性能
- **.NET CLR** — C# IL 代码被 JIT 编译
- **PyPy** — 一个 JIT 编译的 Python 运行时（比 CPython 快得多）

**权衡：** 启动时有一些预热开销，但与解释执行相比，持续执行更快。

---

### 2. 在 ML / LLM 框架中

JIT 在现代深度学习堆栈中被大量使用，尤其是用于 LLM 推理优化：

#### **PyTorch JIT (TorchScript)**

```python
import torch

@torch.jit.script
def my_fn(x: torch.Tensor) -> torch.Tensor:
    return x * 2 + 1
```

`torch.jit` 将 PyTorch 模型/函数编译成 **中间表示（IR）**，可以优化、序列化并在没有 Python 开销的情况下运行。用于在生产中部署 LLM。

#### **JAX `@jax.jit`**

```python
import jax
import jax.numpy as jnp

@jax.jit
def forward(x):
    return jnp.dot(x, weights)
```

JAX 的 `jit` 通过 **XLA**（加速线性代数）跟踪并编译函数为优化的 GPU/TPU 内核。这对于高性能 LLM 训练（Gemma、基于 Flax 的模型等）至关重要。

#### **Triton / 自定义 CUDA 内核**

GPU 内核库如 [Triton](https://triton-lang.org/) 使用 JIT 在运行时编译自定义内核，用于 LLM 注意力层、softmax 等。

#### **`torch.compile` (PyTorch 2.0+)**

TorchScript 的现代后继者 — 一行代码的 JIT 编译：

```python
model = torch.compile(my_llm)  # JIT-compiles the whole model graph
```

用于加速 LLaMA、Mistral 等模型的推理。

---

### 总结表

| 上下文 | JIT 的作用 |
| --- | --- |
| JVM / V8 / .NET | 在运行时将字节码编译为本地机器代码 |
| `torch.jit` | 将 PyTorch 图编译为优化的 IR 以用于部署 |
| `jax.jit` | 通过 XLA 跟踪和编译以用于 GPU/TPU |
| `torch.compile` | 全模型 JIT 以加快 LLM 推理 |
| Triton 内核 | JIT 编译 GPU 内核以用于注意力/FFN 层 |

在 LLM 世界中，你最常在 **推理优化** 的背景下遇到 JIT — 通过在服务之前编译计算图来使模型前向传播运行得更快。

---

**参考文献：**

- [PyTorch JIT / TorchScript Documentation](https://pytorch.org/docs/stable/jit.html)
- [JAX JIT Compilation Guide](https://jax.readthedocs.io/en/latest/jit-compilation.html)
- [torch.compile (PyTorch 2.0)](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)
- [Triton JIT Compiler](https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html)
- [Wikipedia: Just-in-time compilation](https://en.wikipedia.org/wiki/Just-in-time_compilation)
