---
audio: false
generated: true
image: false
lang: en
layout: post
title: JIT in Computer Science and LLMs
translated: false
type: note
---

**Question:** What does "JIT" mean in computer science, and specifically in the context of LLMs?

---

**Answer:**

JIT stands for **Just-In-Time** (compilation). It appears in two overlapping ways relevant to your question:

---

### 1. General Computer Science — JIT Compilation

JIT compilation is a technique where code is **compiled at runtime** (just before execution) rather than ahead-of-time (AOT). Instead of pre-compiling everything to machine code before running, the runtime compiles code "on the fly" as it's needed.

**Classic examples:**

- **JVM (Java)** — Java bytecode is JIT-compiled to native machine code at runtime
- **V8 (JavaScript)** — Chrome's engine JIT-compiles JS for performance
- **.NET CLR** — C# IL code is JIT-compiled
- **PyPy** — A JIT-compiled Python runtime (much faster than CPython)

**Trade-off:** Some warmup overhead at startup, but faster sustained execution vs. interpreting.

---

### 2. In ML / LLM Frameworks

JIT is heavily used in modern deep learning stacks, especially for LLM inference optimization:

#### **PyTorch JIT (TorchScript)**

```python
import torch

@torch.jit.script
def my_fn(x: torch.Tensor) -> torch.Tensor:
    return x * 2 + 1
```

`torch.jit` compiles a PyTorch model/function into an **intermediate representation (IR)** that can be optimized, serialized, and run without Python overhead. Used for deploying LLMs in production.

#### **JAX `@jax.jit`**

```python
import jax
import jax.numpy as jnp

@jax.jit
def forward(x):
    return jnp.dot(x, weights)
```

JAX's `jit` traces and compiles functions via **XLA** (Accelerated Linear Algebra) to optimized GPU/TPU kernels. This is central to high-performance LLM training (Gemma, Flax-based models, etc.).

#### **Triton / Custom CUDA Kernels**

GPU kernel libraries like [Triton](https://triton-lang.org/) use JIT to compile custom kernels at runtime for LLM attention layers, softmax, etc.

#### **`torch.compile` (PyTorch 2.0+)**

The modern successor to TorchScript — a one-liner JIT compilation:

```python
model = torch.compile(my_llm)  # JIT-compiles the whole model graph
```

Used to speed up inference for models like LLaMA, Mistral, etc.

---

### Summary Table

| Context | What JIT does |
| --- | --- |
| JVM / V8 / .NET | Compiles bytecode → native machine code at runtime |
| `torch.jit` | Compiles PyTorch graph → optimized IR for deployment |
| `jax.jit` | Traces + compiles via XLA for GPU/TPU |
| `torch.compile` | Whole-model JIT for faster LLM inference |
| Triton kernels | JIT-compiles GPU kernels for attention/FFN layers |

In the LLM world, you'll most often encounter JIT in the context of **inference optimization** — making model forward passes run faster by compiling computation graphs ahead of serving.

---

**References:**

- [PyTorch JIT / TorchScript Documentation](https://pytorch.org/docs/stable/jit.html)
- [JAX JIT Compilation Guide](https://jax.readthedocs.io/en/latest/jit-compilation.html)
- [torch.compile (PyTorch 2.0)](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)
- [Triton JIT Compiler](https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html)
- [Wikipedia: Just-in-time compilation](https://en.wikipedia.org/wiki/Just-in-time_compilation)
