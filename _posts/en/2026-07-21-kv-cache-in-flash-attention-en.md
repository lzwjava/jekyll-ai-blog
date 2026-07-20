---
audio: false
generated: true
image: false
lang: en
layout: post
title: KV Cache in Flash Attention
translated: false
type: note
---

Question: What does KV cache mean in this Flash Attention code?

Answer:

**KV cache = Key/Value cache.** It is an inference optimization for autoregressive LLM generation that avoids recomputing previous tokens' attention keys and values.

In a Transformer attention layer:

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
]

For a prompt:

```
"The capital of France is"
```

the model processes tokens:

```
T1  T2  T3  T4  T5
```

At every layer it computes:

```
K1 V1
K2 V2
K3 V3
K4 V4
K5 V5
```

When generating the next token:

```
"The capital of France is Paris"
```

the new query is only for:

```
T6 = "Paris"
```

Without KV cache:

```
Compute K,V for:

T1 T2 T3 T4 T5 T6

again
```

With KV cache:

```
Cache:
K1 V1
K2 V2
K3 V3
K4 V4
K5 V5

Only compute:

K6 V6

Then attention:

Q6 attends to:

[K1 K2 K3 K4 K5 K6]
[V1 V2 V3 V4 V5 V6]
```

---

## In your code

The key function:

```python
def flash_attn_with_kvcache(
    q,
    k_cache,
    v_cache,
    k=None,
    v=None,
    cache_seqlens=None,
    ...
):
```

is the inference path.

### Shapes

```python
q:        (B, T_new, H, D)
k_cache:  (B, T_max, H_kv, D)
v_cache:  (B, T_max, H_kv, D)
```

Example:

```
B = 1              batch size
T_max = 32768      maximum context length
H = 32             attention heads
D = 128            head dimension
```

Memory:

```
k_cache:

[
 token0: [head0...head31]
 token1: [head0...head31]
 token2: ...
]
```

It is basically a big tensor storing the history.

---

## This part writes new tokens into cache

```python
if k is not None and v is not None:
    k_cache[:, pos:pos+T_new, :, :] = k
    v_cache[:, pos:pos+T_new, :, :] = v
```

Example:

Before:

```
k_cache

position:
0  1  2  3  4  5  6  7
K  K  K  K  K  ?  ?  ?
```

Generate token 5:

```
pos = 5
```

Insert:

```
0  1  2  3  4  5  6  7
K  K  K  K  K  K5 ?  ?
```

---

## Then attention uses the whole history

```python
k_full = k_cache[:, :end_pos, :, :]
v_full = v_cache[:, :end_pos, :, :]
```

So:

```
k_full:

K0 K1 K2 K3 K4 K5
```

Then:

```python
Attention(
    Q5,
    K0..K5,
    V0..V5
)
```

The model can "remember" previous tokens.

---

## Why training does not need KV cache

Your comment:

```python
# Training (no KV cache)
y = flash_attn.flash_attn_func(...)
```

During training:

Input:

```
hello world this is GPT
```

You process all tokens together:

```
Q:
q1 q2 q3 q4 q5

K:
k1 k2 k3 k4 k5

V:
v1 v2 v3 v4 v5
```

Flash Attention computes the whole matrix efficiently:

```
       k1 k2 k3 k4 k5

q1     x
q2     x  x
q3     x  x  x
q4     x  x  x  x
q5     x  x  x  x  x
```

because causal masking prevents looking forward.

No need to store KV.

---

## Why KV cache matters for long-context agents

For agents like:

* Claude Code
* OpenClaw
* Hermes
* long-context Qwen
* GPT-style chat

generation is usually:

```
prompt:
50k tokens

output:
2k tokens
```

Without KV cache:

Each output token:

```
recompute 50k tokens
```

Cost:

```
50k + 50k + 50k + ...
```

With KV cache:

```
initial prompt:
compute K/V once

then:

token1 -> only new K/V
token2 -> only new K/V
token3 -> only new K/V
```

Cost becomes roughly:

```
50k + 2k
```

instead of:

```
50k * 2k
```

---

## The tradeoff

KV cache speeds inference but consumes VRAM.

Memory:

[
KV\ memory =
2 \times layers \times sequence_length \times heads \times head_dim \times bytes
]

Example:

Llama 70B:

```
80 layers
64 KV heads
128 dim
128k context
bf16
```

KV cache can be:

```
hundreds of GB
```

This is why newer models use:

* GQA (Grouped Query Attention)
* MQA (Multi Query Attention)
* KV quantization
* paged attention (vLLM)

to reduce KV memory.

---

## Relation to your RTX 4070 / local inference

Your RTX 4070:

```
12GB VRAM
```

The limiting factor for long context is often not model weights but KV cache.

Example:

Qwen 32B:

```
weights:
~64GB bf16
```

impossible locally.

But even smaller models:

```
Qwen3 8B
128k context
```

may hit:

```
KV cache > several GB
```

before weights are the problem.

This is why inference engines like:

* vLLM
* llama.cpp
* TensorRT-LLM

have sophisticated KV cache management.

In your code, `flash_attn_with_kvcache()` is essentially the low-level primitive that those engines build on.
