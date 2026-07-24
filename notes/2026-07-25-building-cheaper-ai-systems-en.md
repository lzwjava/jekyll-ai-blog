---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building Cheaper AI Systems
translated: false
type: note
---

Question: Is it still possible to build another DeepSeek or Kimi today to reduce AI costs?

Answer:

Short answer: **yes, but not by simply training another frontier foundation model from scratch.** The opportunity has shifted from "build a bigger GPT" to **build a cheaper AI system**.

DeepSeek and Kimi are good examples because their advantage is not only model size. It is the whole stack:

```
data
 ↓
training recipe
 ↓
architecture
 ↓
distributed training
 ↓
inference optimization
 ↓
product + user feedback loop
```

A new company can still attack parts of this stack.

---

## 1. Another DeepSeek-scale model? Very hard

DeepSeek-V3 scale:

```
671B total parameters
37B active parameters (MoE)
14.8T training tokens
thousands of H100-class GPUs
months of engineering
```

The capital requirement is enormous.

The moat is:

```
GPU cluster
+
research talent
+
training infrastructure
+
data pipeline
+
evaluation
+
post-training
```

A small startup cannot compete head-on.

---

## 2. But "AI cost reduction" is a huge opportunity

The next wave is probably not:

> "We train a 10T parameter model"

It is:

> "We make intelligence 10x cheaper"

Examples:

### A. Better inference

Current LLM inference:

```
request
 |
token generation
 |
KV cache
 |
GPU memory bandwidth bottleneck
```

Huge cost.

Companies can win with:

* speculative decoding
* quantization
* KV cache compression
* sparsity
* MoE routing
* model distillation

Example:

```
Teacher model:

Claude/GPT-5
     |
     v
small specialized model

70B → 7B
quality loss: small
cost reduction: 10x
```

---

## 3. Vertical models are still open

Instead of:

```
general intelligence
```

build:

```
real estate AI
legal AI
finance AI
coding AI
medical AI
```

A 7B-30B model with excellent data can beat a general 400B model.

Example:

```
General model:

GPT-5
100% capability
$1/query


Vertical model:

RealEstateGPT
85% capability
$0.01/query
```

For business, the second wins.

---

## 4. The "Kimi opportunity" is interesting

Kimi's advantage historically:

* long context
* efficient inference
* Chinese market
* product execution

Long context itself is a cost problem.

Naive:

```
1M tokens
 ↓
attention

O(n²)
```

Expensive.

Better:

```
retrieval
+
memory
+
compression
+
agent planning
```

The future may not be:

```
100M context window
```

but:

```
AI memory system
```

---

## 5. A small team can build something meaningful now

The recipe:

```
Open models
(Qwen / Llama / DeepSeek)

        +

fine tuning

        +

synthetic data

        +

RL

        +

agent system

        +

cheap inference
```

Example:

A 5-person team:

```
Qwen3-32B
       |
       |
domain SFT
       |
       |
GRPO/RL
       |
       |
vLLM serving
       |
       |
AI product
```

Can beat much larger companies in a narrow domain.

---

## 6. Hardware is changing the game

Previously:

```
Only hyperscalers can train
```

because:

```
10000 H100
```

Now:

```
8x RTX 5090
8x MI300X
cloud GPU rental
```

is accessible.

Especially for:

* fine tuning
* distillation
* small MoE
* reasoning models

Your own experiments are already close to this direction:

```
GPT-2 124M from scratch
RTX 4070
15B tokens dataset
```

The next step is not training GPT-5.

It is:

```
small model
+
better data
+
reasoning training
+
agent loop
```

---

## My view:

The next DeepSeek is unlikely to be:

> "We trained a larger model."

It will probably be:

> "We discovered a way to get GPT-5-level useful intelligence at 1/50 cost."

Possible areas:

1. **AI inference optimization**
2. **agent architecture**
3. **domain-specific models**
4. **synthetic data generation**
5. **model compression/distillation**
6. **open-source AI infrastructure**

The opportunity is actually larger now because intelligence is becoming a commodity. The bottleneck moves from **model training** to **efficient deployment**.

References:

* DeepSeek-V3 technical report: [https://arxiv.org/abs/2412.19437](https://arxiv.org/abs/2412.19437)
* Kimi/Moonshot AI: [https://www.moonshot.cn/](https://www.moonshot.cn/)
* vLLM inference engine: [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
* Qwen open models: [https://github.com/QwenLM/Qwen](https://github.com/QwenLM/Qwen)
* Mixture-of-Experts overview: [https://arxiv.org/abs/1701.06538](https://arxiv.org/abs/1701.06538)