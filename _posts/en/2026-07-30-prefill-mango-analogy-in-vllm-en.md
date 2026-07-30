---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prefill Mango Analogy in vLLM
translated: false
type: note
---

**Question:**
“切 mango 就是 prefill（预填充）吗？token 预填充在 vLLM 里面是什么？”

**Answer:**

Yes. In LLM inference, **prefill（预填充）** is basically the phase where the model processes the **input prompt tokens all at once** before it starts generating new tokens.

Think of an LLM request:

```
User:
"Explain transformer attention in detail"

Tokens:
[Explain, transformer, attention, in, detail]
```

Inference has two phases:

```
             Prompt tokens                 Output tokens
                  |                             |
                  v                             v

        +----------------+          +----------------+
        |    Prefill     |          |    Decode      |
        | process input  |--------->| generate 1 by 1|
        +----------------+          +----------------+
```

## 1. Prefill = compute prompt KV cache

During prefill:

```
Input:
x1 x2 x3 x4 x5

Transformer forward:

x1 -> hidden
x2 -> hidden
x3 -> hidden
x4 -> hidden
x5 -> hidden

Generate:

K1 V1
K2 V2
K3 V3
K4 V4
K5 V5
```

The model stores:

```
KV cache:

Layer 0:
 K: [k1,k2,k3,k4,k5]
 V: [v1,v2,v3,v4,v5]

Layer 1:
 K: [...]
 V: [...]

...

Layer 32:
 K: [...]
 V: [...]
```

This is why it is called:

> pre-fill the attention cache

The Chinese "预填充" is a good translation.

---

## 2. Decode = generate new tokens

After prefill:

Generate token 6:

```
Input:
x6 only

Attention:

Q6 attends to:

K1 K2 K3 K4 K5

plus new:

K6 V6
```

Then token 7:

```
x7

attend:

K1 ... K6
```

Decode is sequential.

---

## 3. Why prefill is fast?

Because it is a big matrix operation.

Example:

Prompt:

```
4096 tokens
```

During prefill:

```
4096 tokens together

matmul:

[4096,d_model]
       *
[d_model,d_model]

GPU loves this.
```

High GPU utilization.

---

Decode:

```
1 token

[1,d_model]
      *
[d_model,d_model]
```

Small matrix.

GPU is underutilized.

This is why LLM serving has:

* prefill bottleneck → compute bound
* decode bottleneck → memory bandwidth bound

---

## 4. vLLM architecture

vLLM separates these:

```
                Scheduler

                    |
          +---------+---------+
          |                   |
          v                   v

      Prefill batch        Decode batch

      prompt tokens        generated tokens

          |                   |
          +---------+---------+

                    |
                    v

              GPU execution
```

Example:

Requests:

```
Request A:
prompt = 4000 tokens


Request B:
prompt = 2000 tokens
```

vLLM does:

```
Prefill batch:

A:
4000 tokens

B:
2000 tokens


Total:
6000 tokens
```

GPU runs one large forward.

Then:

```
Decode:

A -> next token
B -> next token
```

---

## 5. vLLM PagedAttention connection

The KV cache is huge.

Example:

Llama 70B:

```
layers: 80
heads: 64
head_dim:128
tokens: 8192
```

KV cache:

```
2 * layers * tokens * heads * head_dim * bytes
```

roughly:

```
2*80*8192*64*128*2 bytes

≈ 21 GB
```

For many users:

```
User1:
8192 tokens

User2:
4096 tokens

User3:
16000 tokens
```

Memory fragmentation happens.

vLLM solves this with:

```
PagedAttention

KV cache:

GPU memory:

[block][block][block][block]

Request A:
block 1
block 7
block 9

Request B:
block 2
block 3
```

Like OS virtual memory.

---

## 6. "切 mango" analogy

If you mean the Chinese phrase:

> 切 mango

Imagine eating mango:

### Prefill

Cut the whole mango:

```
🥭 -> 🔪 -> many pieces
```

You process all existing tokens.

### Decode

Eat one piece at a time:

```
piece1
piece2
piece3
...
```

But the mango itself is the context.

---

For vLLM, the important mental model:

```
Request arrives

          Prompt
            |
            v
       PREFILL
       - process all tokens
       - create KV cache
       - expensive compute

            |
            v

       DECODE LOOP

       token -> token -> token

       - reuse KV cache
       - memory bandwidth limited
```

Understanding this is the key to understanding why vLLM has **continuous batching**, **PagedAttention**, **chunked prefill**, and why modern inference systems are designed around the prefill/decode split.
