---
audio: false
generated: true
image: false
lang: en
layout: post
title: Implementing DeepSeek MLA from Scratch
translated: false
type: note
---

Question: Good GitHub projects to learn DeepSeek MLA (Multi-Head Latent Attention)?

Answer:

For learning MLA deeply, I would go in this order:

## 1. Best starting point: implement MLA yourself

### [LLMs-from-scratch MLA chapter](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/05_mla/README.md?utm_source=chatgpt.com)

This is probably the best educational resource.

Why:

* starts from normal MHA
* compares GQA → MLA
* explains KV cache reduction
* small PyTorch code

The learning path:

```
MHA
 |
 v
GQA
 |
 v
MLA
 |
 v
DeepSeek-V2/V3 optimized MLA
```

Understand this first:

Normal MHA KV cache:

[
K,V \in R^{seq \times n_{heads}\times d}
]

MLA:

[
c_{KV}=xW_{down}
]

store:

[
c_{KV}
]

instead of:

[
K,V
]

At decode time:

[
K=c_{KV}W_k
]

[
V=c_{KV}W_v
]

So memory changes:

```
MHA:

seq × heads × head_dim


MLA:

seq × latent_dim
```

---

## 2. Clean PyTorch implementation

### [Multi-Head-Latent-Attention-MLA-](https://github.com/joey00072/Multi-Head-Latent-Attention-MLA-?utm_source=chatgpt.com)

Repository:

```
joey00072/Multi-Head-Latent-Attention-MLA-
```

Good because:

```
mla.py
modeling_mla.py
train_mla.py
```

are small.

You can literally read:

```python
class MLA(nn.Module):
```

and trace:

```
x
 |
 +--> q compression
 |
 +--> kv compression
 |
 latent cache
 |
 reconstruct k/v
 |
 attention
```

This is closer to "nanoGPT style learning".

---

## 3. MiniGPT + MLA

### [MiniGPT-and-DeepSeek-MLA-Multi-Head-Latent-Attention](https://github.com/junfanz1/MiniGPT-and-DeepSeek-MLA-Multi-Head-Latent-Attention?utm_source=chatgpt.com)

Good for understanding integration:

```
miniGPT.py

        |
        v

Self Attention

        |
        v

GQA

        |
        v

MLA
```

It contains:

```
Multi-Head Self Attention.py
Group Query Attention.py
Multi-Head Latent Attention.py
```

Very good for comparing architectures.

---

## 4. The real DeepSeek implementation

### [DeepSeek-V3 GitHub MLA implementation](https://github.com/deepseek-ai/DeepSeek-V3/blob/main/inference/model.py?utm_source=chatgpt.com)

Eventually read:

```
DeepSeek-V3/inference/model.py

class MLA(nn.Module)
```

This is the real thing.

Important lines:

```python
self.wkv_a =
    Linear(
        self.dim,
        self.kv_lora_rank + self.qk_rope_head_dim
    )
```

This is the key idea:

Instead of:

```
x
 |
 +--> Wk
 |
 +--> Wv
```

DeepSeek:

```
x
 |
 Wkv_down
 |
 latent c_kv
 |
 +--> Wk_up
 |
 +--> Wv_up
```

The latent vector is the KV cache.

---

## 5. Production kernel implementation

After understanding math:

### [FlashMLA](https://github.com/deepseek-ai/FlashMLA/blob/main/README.md?utm_source=chatgpt.com)

This is not for first learning.

It is CUDA optimization:

```
PyTorch MLA
      |
      v
FlashMLA kernel
      |
      v
H100/B200 optimized inference
```

You will see:

* memory layout
* fused kernels
* FP8 KV cache
* decode optimization

---

## My recommended study route for you

Given you already trained GPT-2/nanoGPT, I would do:

### Day 1

Read:

```
LLMs-from-scratch MLA
```

Implement:

```python
class MLA(nn.Module):
    def forward(self,x):
        c = self.kv_down(x)

        k = self.k_up(c)
        v = self.v_up(c)

        attn = q @ k.transpose(-2,-1)

        return attn @ v
```

---

### Day 2

Modify nanoGPT:

Replace:

```python
self.key = nn.Linear(n_embd,n_embd)
self.value = nn.Linear(n_embd,n_embd)
```

with:

```python
self.kv_down = nn.Linear(
    n_embd,
    kv_rank
)

self.k_up = nn.Linear(
    kv_rank,
    n_embd
)

self.v_up = nn.Linear(
    kv_rank,
    n_embd
)
```

Train on TinyStories.

Compare:

```
MHA
vs
GQA
vs
MLA
```

Measure:

* KV cache size
* throughput
* validation loss

---

The deepest conceptual connection to your previous Q/K/V discussion:

MLA is basically saying:

> Since KV projection is already a lossy learned information filter, why store the expanded K/V? Store the latent compressed representation before expansion.

So instead of:

[
x \rightarrow K,V
]

store:

[
x \rightarrow z_{KV}
]

where:

[
dim(z_{KV}) << dim(K,V)
]

Then reconstruct the attention space when needed.

This is why MLA is a very natural next step after understanding Q/K/V as learned low-rank information filtering.
