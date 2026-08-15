---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FlashAttention: Fast IO-Aware Exact Attention"
translated: false
type: note
---

Question: What does arXiv paper 2205.14135 say?

Answer: This paper is **"FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"** by Tri Dao et al. It introduced **FlashAttention**, one of the most important optimizations behind modern LLM training/inference. ([Hugging Face][1])

The core idea:

> Transformer attention is not mainly slow because of FLOPs. It is slow because GPUs spend too much time moving data between memory levels.

They redesign attention to be **IO-aware**. ([SciSpace][2])

---

## 1. Problem: Standard attention wastes GPU memory bandwidth

Normal attention:

Given:

```
Q = XWq
K = XWk
V = XWv
```

Attention:

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
]

For sequence length `N`:

```
Q: N × d
K: N × d
V: N × d

QK^T:
N × N
```

The attention matrix is huge.

Example:

```
sequence length = 4096
head dimension = 128

attention matrix:

4096 × 4096
= 16,777,216 elements

FP16:
~32 MB per head
```

For many heads and layers:

```
GPU HBM memory explodes
```

---

## 2. The surprising observation: compute is not the bottleneck

Modern GPUs:

```
GPU SRAM (fast)
       |
       |
HBM VRAM (slow)
       |
       |
CPU memory
```

The GPU can do trillions of operations/sec.

But moving data:

```
HBM → SRAM
SRAM → HBM
```

is expensive.

The paper says:

> Attention algorithms should consider IO complexity, not only computational complexity. ([SciSpace][2])

---

# 3. Standard attention implementation

Usually:

```python
scores = Q @ K.T

attention = softmax(scores)

output = attention @ V
```

GPU does:

```
1. Compute QK^T
2. Write NxN matrix to HBM
3. Read NxN matrix
4. Softmax
5. Write result
6. Read again
7. Multiply V
```

The huge NxN matrix is materialized.

---

# 4. FlashAttention idea: never store the full attention matrix

Instead:

```
split Q,K,V into blocks
```

Example:

```
Q:

[ block ]
[ block ]
[ block ]


K,V:

[ block ]
[ block ]
[ block ]
```

Compute:

```
Q_block × K_block^T
```

inside GPU SRAM.

Then immediately:

```
softmax
multiply V
discard temporary result
```

Never write:

```
NxN attention matrix
```

to VRAM.

---

Visual:

Normal:

```
Q
 \
  \
   QK^T  ---> HBM
              |
              |
           softmax
              |
              |
              V
```

FlashAttention:

```
Q block
   \
    \
     SRAM
      |
      |
   softmax
      |
      |
      V

(no NxN matrix stored)
```

---

# 5. The mathematical trick: online softmax

The problem:

Softmax needs:

[
softmax(x_i)=\frac{e^{x_i}}{\sum e^{x_i}}
]

Normally you need all values.

FlashAttention uses an online algorithm.

Maintain:

```
running max m
running sum l
running output O
```

For every block:

```
new block arrives

update:
    max
    normalization
    output
```

So attention can be computed block-by-block.

---

# 6. Result

The paper reports: ([Hugging Face][1])

Training speed improvements:

```
BERT-large:
+15%

GPT-2 sequence length 1K:
~3x faster

Long Range Arena:
~2.4x faster
```

It also enables much longer contexts:

```
16K tokens
64K tokens
```

---

# 7. Why it changed LLM engineering

Before FlashAttention:

```
Long context = impossible

because:

memory ∝ sequence_length²
```

After:

```
Long context becomes practical
```

Modern models use variants:

* FlashAttention-1 (this paper)
* FlashAttention-2
* FlashAttention-3

Used in:

* GPT-style models
* LLaMA
* Qwen
* DeepSeek
* Mistral
* diffusion transformers

---

# 8. Code intuition

Without FlashAttention:

```python
def attention(Q,K,V):
    scores = Q @ K.transpose(-2,-1)
    probs = softmax(scores)
    return probs @ V
```

Memory:

```
O(N²)
```

---

With FlashAttention:

```python
def flash_attention(Q,K,V):
    for q_block in Q:
        for k_block,v_block in KV:
            update_online_softmax(q_block,k_block,v_block)

    return output
```

Memory:

```
O(N)
```

---

# 9. Why this matters for your GPU experiments

For your RTX 4070 / Qwen / nanoGPT training:

Without FlashAttention:

```
long context
+
large batch
=
OOM
```

With FlashAttention:

```
same GPU

can train:
- larger sequence length
- larger batch
- bigger models
```

The bottleneck moves from:

```
VRAM capacity
```

toward:

```
GPU compute
```

This is why FlashAttention is considered a foundational LLM infrastructure breakthrough, similar in importance to:

* CUDA kernels
* cuBLAS
* NCCL
* fused optimizers

References:

* FlashAttention paper: ([Hugging Face][1])
* DBLP entry: ([DBLP][3])
* Paper summary and abstract: ([SciSpace][2])

[1]: https://huggingface.co/papers/2205.14135?utm_source=chatgpt.com "Paper page - FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
[2]: https://scispace.com/papers/flashattention-fast-and-memory-efficient-exact-attention-1cickunc?utm_source=chatgpt.com "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (2022) | Tri Dao | 1035 Citations"
[3]: https://dblp.org/rec/journals/corr/abs-2205-14135.html?utm_source=chatgpt.com "dblp: FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness."
