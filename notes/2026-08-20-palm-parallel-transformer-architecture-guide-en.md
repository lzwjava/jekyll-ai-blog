---
audio: false
generated: true
image: false
lang: en
layout: post
title: PaLM Parallel Transformer Architecture Guide
translated: false
type: note
---

Question: Introduction to **PaLM: Scaling Language Modeling with Pathways** — especially the **parallel attention + FFN** architecture.

Answer:

PaLM: Scaling Language Modeling with Pathways is a Google paper that introduced a **540B parameter language model** and demonstrated that scaling Transformer models with better architecture and training methods could significantly improve reasoning, coding, multilingual understanding, and few-shot learning.

Paper:
[https://arxiv.org/abs/2204.02311](https://arxiv.org/abs/2204.02311)

The interesting part you mentioned is the **parallel attention + feed-forward network (FFN)** design.

## 1. Standard Transformer block

Classic GPT-style Transformer uses:

```
x
|
|---- LayerNorm
|
Attention
|
Add residual
|
LayerNorm
|
FFN
|
Add residual
|
y
```

Mathematically:

Attention:

[
h_1 = x + Attention(LN(x))
]

FFN:

[
h_2 = h_1 + FFN(LN(h_1))
]

The two sublayers are **sequential**.

The FFN cannot start until attention finishes.

---

## 2. PaLM parallel Transformer block

PaLM changed this:

Instead of:

```
x
 |
 Attention
 |
 FFN
 |
 y
```

it does:

```
             Attention
                |
x ------------ + ------------ y
                |
              FFN
```

Both branches see the same input:

[
y = x + Attention(LN(x)) + FFN(LN(x))
]

So:

```
input x

       +----------------+
       |                |
       v                v

 Multi-head        Feed Forward
 Attention           Network

       |                |
       +-------+--------+
               |
               v

          Residual output
```

---

## 3. Why does this help?

### Reason 1: Better hardware utilization

Large models spend huge compute on:

* matrix multiplications
* memory movement
* communication between GPUs

Sequential:

```
Attention
(wait)
FFN
(wait)
```

Parallel:

```
Attention
   \
    +---- combine
   /
FFN
```

The GPU can execute more independent operations.

For TPU pods, this matters.

---

## 4. Mathematical view

Normal Transformer:

[
x_{l+1}=x_l+FFN(LN(x_l+Attention(LN(x_l))))
]

PaLM:

[
x_{l+1}=x_l+Attention(LN(x_l))+FFN(LN(x_l))
]

The gradient path becomes shorter.

Instead of:

```
x
 |
attention
 |
FFN
 |
output
```

you have:

```
x
 |\
 | \
A  F
|   |
+---+
 |
output
```

This can improve optimization at very large scale.

---

## 5. Related PaLM architecture changes

PaLM was not only parallel attention.

Major changes:

### SwiGLU activation

Instead of:

[
FFN(x)=W_2 ReLU(W_1x)
]

PaLM uses:

[
FFN(x)=W_2(SiLU(W_1x)\odot W_3x)
]

Same family used in:

* LLaMA
* Qwen
* Mistral

---

### Multi-query attention (MQA)

Normal attention:

```
head1: Q K V
head2: Q K V
head3: Q K V
...
```

MQA:

```
head1: Q
head2: Q
head3: Q

       shared K,V
```

Benefits:

* lower KV cache
* faster inference

Important for serving large models.

---

### Pathways system

The name comes from Google's distributed AI infrastructure.

Goal:

One model can run across:

* TPU pods
* multiple tasks
* multiple modalities

Instead of training separate systems.

Conceptually:

```
many TPU devices

       |
       v

Pathways runtime

       |
       +---- language
       |
       +---- vision
       |
       +---- robotics
```

---

## 6. Why PaLM mattered

Before PaLM:

```
GPT-3:
175B parameters
```

PaLM:

```
540B parameters
```

The scaling trend:

```
model size ↑
data ↑
compute ↑

↓

better reasoning ability
```

PaLM showed:

* chain-of-thought emergence
* code generation improvement
* multilingual ability
* arithmetic reasoning

It influenced later models:

```
PaLM
 |
 +--> PaLM 2
 |
 +--> Gemini
 |
 +--> many modern decoder LLM designs
```

---

## 7. Minimal PyTorch implementation

A PaLM-style block:

```python
class PaLMBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()

        self.norm = nn.LayerNorm(dim)

        self.attn = Attention(dim)

        self.ffn = SwiGLU(dim)

    def forward(self, x):

        h = self.norm(x)

        attn_out = self.attn(h)

        ffn_out = self.ffn(h)

        return x + attn_out + ffn_out
```

Compared with GPT:

```python
x = x + attention(norm(x))
x = x + ffn(norm(x))
```

PaLM:

```python
h = norm(x)

x = x + attention(h) + ffn(h)
```

---

For someone training nanoGPT-style models: the PaLM block is a very small code change but becomes important when scaling from **hundreds of millions → hundreds of billions parameters**, because the bottleneck shifts from pure FLOPs to **parallelism, memory bandwidth, and optimization stability**.
