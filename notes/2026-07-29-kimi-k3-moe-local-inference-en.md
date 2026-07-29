---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kimi K3 MoE Local Inference
translated: false
type: note
---

Question: What is the Kimi K3 local Mac inference story, and why does the architecture make it possible?

Answer:

This article is describing a **new direction for running extremely large LLMs locally**: instead of shrinking a giant model until it fits, design the model so that only a small part needs to be active at inference time.

The key idea:

> **Kimi K3 is huge (2.8T parameters), but MoE architecture means you don't need all 2.8T parameters in memory for every token.**

This is the same fundamental idea behind models like Mixtral, DeepSeek-V3, etc., but pushed further.

---

## 1. First: what is Kimi K3?

Kimi K3 (according to the article) is:

* ~2.8 trillion parameters
* MoE (Mixture of Experts)
* MXFP4 native training
* 1.6TB weight size
* Hybrid architecture:

  * KDA (Kimi Delta Attention)
  * LatentMoE
  * NoPE (No Rotary Position Embedding)

The important number is not 2.8T.

The important number is:

**How many parameters are activated per token?**

A dense model:

```
GPT-4 style:

token
 |
all parameters
 |
output
```

If you have:

```
2T parameters
```

you need:

```
2T parameters active every token
```

Impossible locally.

---

MoE:

```
                 Expert 1
                /
token -> router -> Expert 37
                \
                 Expert 2000
```

Only a few experts run.

Example:

```
Total:
2.8T parameters

Activated:
~30B-100B parameters
```

The rest can sit on disk.

This is why the Mac trick works.

---

## 2. Why can a Mac run a 1.6TB model?

A naive approach:

```
load model

RAM:
[1.6TB weights]

compute
```

Impossible.

Even Mac Studio max:

```
512GB unified memory
```

cannot fit.

---

Deltafin does something closer to:

```
               SSD / HTTP storage
                     |
                     v

              expert weights

                     |
                     v

                RAM cache

                     |
                     v

              Metal GPU / NEON CPU

                     |
                     v

                next token
```

Only fetch the experts needed.

Like virtual memory for LLMs.

Operating systems did this 50 years ago:

```
Disk
 |
swap
 |
RAM
 |
CPU
```

Now:

```
Huge LLM storage
 |
expert paging
 |
GPU
 |
token generation
```

---

## 3. LatentMoE is the interesting part

Normal MoE:

```
expert:

FFN:
7680 -> 30000 -> 7680
```

Huge matrices.

LatentMoE compresses the expert representation.

Conceptually:

Normal:

```
hidden
  |
big matrix
  |
output
```

Latent:

```
hidden
 |
small latent space
 |
expert computation
 |
output
```

Similar philosophy to:

* LoRA
* latent diffusion
* low-rank factorization

The model keeps capability while reducing active compute.

---

## 4. MXFP4 native training

This is actually a big deal.

Normally:

Train:

```
BF16 model

↓

quantize

↓

INT4 / FP4
```

Problem:

quantization can hurt quality.

Kimi K3:

```
training itself
       |
       v
     MXFP4
       |
       v
 deployment
```

The model learns to live in low precision.

This is similar philosophy to NVIDIA's FP8 training.

The future direction:

```
old:

train big
then compress


new:

train for deployment format
```

---

## 5. NoPE: removing RoPE

Most modern transformers:

```
token embedding

+

RoPE position encoding

+

attention
```

RoPE gives:

"token 100 is different from token 500"

because attention alone has no explicit position.

Kimi says:

Maybe we don't need it.

Why?

Because KDA is recurrent-like.

A simplified view:

Traditional attention:

```
Q K V

compare every token with every token
```

Complexity:

```
O(n²)
```

KDA:

```
state_t = update(state_t-1, token_t)

output = f(state)
```

Like RNN:

```
position information naturally appears
```

So:

```
remove RoPE
+
KDA layers before attention
```

The model learns order without explicit position embeddings.

---

## 6. Why this matters for local AI

The historical pattern:

### Old way

Big model:

```
70B

↓

community quantization

↓

4-bit

↓

runs locally
```

You lose quality.

---

Kimi K3 approach:

```
architecture

↓

already optimized for sparse activation

↓

local inference possible
```

The analogy:

Old:

```
Make Ferrari lighter until bicycle tires fit
```

New:

```
Design Ferrari with detachable modules
```

---

## 7. Is 0.3 token/sec useful?

For chat:

No.

Human:

```
Question
(wait 10 seconds)
one sentence
```

painful.

But batch jobs:

Very interesting.

Example:

Evaluation:

```
1 million prompts

run overnight

compare models

```

Speed matters less.

A local K3 becomes:

```
private GPT-5-class evaluator
```

without API cost.

---

## 8. The bigger picture

The important trend is:

### Model architecture is becoming hardware-aware.

2020:

```
Transformer
+
GPU
```

2026:

```
Transformer
+
MoE
+
sparse activation
+
low precision training
+
memory hierarchy
+
consumer hardware
```

The future local AI stack may look like:

```
Mac Studio
     |
     |
Thunderbolt cluster
     |
     |
MoE model
     |
     |
local agent system
```

Not every person needs a 2.8T model in RAM.

They need:

* storage cheap
* bandwidth enough
* smart routing
* sparse activation

---

For your setup (RTX 4070 12GB + local experiments), the practical lesson is not "run Kimi K3 tomorrow". It is:

**MoE changes the game.**

Your nanoGPT experiments are dense models:

```
124M parameters

every token:
124M active
```

Future local models:

```
2.8T total

maybe:
50B active
```

The research question shifts from:

> "How do we fit a bigger model?"

to:

> "How do we make the model touch less of itself per token?"

That is exactly why DeepSeek-V3, Kimi K3, Mixtral-style models are important.

References:

* Sebastian Raschka, "Kimi K3 Architecture Notes" — [https://sebastianraschka.com/blog/2026/kimi-k3-architecture-notes.html](https://sebastianraschka.com/blog/2026/kimi-k3-architecture-notes.html)
* Deltafin GitHub — [https://github.com/gavamedia/deltafin](https://github.com/gavamedia/deltafin)
* Hacker News discussion: Running Kimi K3 on M1 Max — [https://news.ycombinator.com/item?id=49090233](https://news.ycombinator.com/item?id=49090233)
