---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding GLM-3.5 Flash Local Performance
translated: false
type: note
---

Question: How to understand “GLM-3.5 Flash local run, single stream 30–40 tokens/s, thanks to MIT and Berkeley scholars for FreeToken work”?

Answer:

This sentence is basically saying:

> “We successfully deployed GLM-3.5 Flash on our own local hardware. The inference speed is about 30–40 tokens per second for one request stream. I and our student/community group want to thank researchers from MIT and Berkeley for publishing the FreeToken work.”

Break it down:

### 1. “GLM3.5 Flash 我们在本地已经跑通了”

Meaning they did **local inference**, not calling an API.

Example:

```
User
 |
 v
Local machine
 |
 v
GLM-3.5 Flash weights
 |
 v
Generated tokens
```

They probably downloaded the model weights and ran something like:

```bash
python generate.py \
  --model glm-3.5-flash \
  --prompt "hello"
```

Instead of:

```
Your app
   |
   v
OpenAI API / Zhipu API
   |
   v
Cloud GPU
```

Local means they control:

* GPU
* memory
* quantization
* inference engine
* latency

---

### 2. “单流三四十”

This is an inference benchmark.

A language model generates text token by token:

```
Input:
"Explain transformer"

Model forward pass:

token 1
token 2
token 3
...
token N
```

Speed:

```
tokens / second
```

So:

```
30-40 tok/s
```

means:

```
one user
one conversation
one generation stream

≈ 30-40 tokens every second
```

For human chat, this feels very fast.

Example:

A normal answer:

```
500 tokens
```

At 40 tok/s:

```
500 / 40 = 12.5 seconds
```

---

### 3. Why mention “single stream”?

Because throughput and latency are different.

Single stream:

```
GPU
 |
 User A
 |
 40 tok/s
```

Multiple users:

```
GPU
 |
 + User A
 + User B
 + User C
```

The same GPU may achieve:

```
single:
40 tok/s

batch:
200 tok/s total
```

but each person may get:

```
10-20 tok/s
```

Production systems care about:

* latency
* throughput
* concurrent users

---

### 4. “FreeToken” probably means inference optimization

The interesting part is thanking MIT/Berkeley researchers.

The reason is likely some optimization technique that reduces inference cost.

Modern LLM inference bottleneck:

```
Transformer forward:

Attention:
Q K V

+
MLP

+
memory movement
```

Especially during decoding:

```
token 1 -> token 2 -> token 3
```

The model repeatedly reads weights and KV cache.

The problem is often:

```
GPU compute < GPU memory bandwidth limitation
```

Optimization papers try to reduce:

* KV cache size
* memory movement
* redundant computation
* token generation overhead

So a research idea can turn:

```
A100:
20 tok/s
```

into:

```
40 tok/s
```

without changing the model.

---

### 5. Why this is interesting from an engineering perspective

This is the same pattern as Linux/open source:

Researchers publish:

```
paper
+
code
+
weights
```

Then students and engineers can build:

```
paper
      |
      v
implementation
      |
      v
local deployment
      |
      v
startup/product
```

The AI ecosystem is moving closer to the Linux ecosystem.

A small team can now do things that previously required Google/OpenAI scale.

Example:

2018:

```
Train transformer:
Google only
```

2026:

```
Fine tune 7B/30B model:
one person + GPUs
```

---

Given your own experiments (GPT-2 124M from scratch, nanochat, local Qwen/vLLM), the key thing to notice is:

**The model architecture is only half the battle. The inference stack is becoming a major competitive layer.**

The stack is:

```
Model architecture
        |
        v
Training data
        |
        v
Weights
        |
        v
Inference engine
        |
        v
Kernel optimization
        |
        v
Hardware utilization
```

FreeToken-type work lives around:

```
Inference engine + memory efficiency
```

which is exactly why a small group can run a strong model locally.

References:

* GLM models: [https://github.com/THUDM/GLM-4](https://github.com/THUDM/GLM-4)
* vLLM inference engine: [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
* FlashAttention: [https://github.com/Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)
