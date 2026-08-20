---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Inkling-Small: Efficient MoE Model"
translated: false
type: note
---

## Question: Intro to Thinking Machines Lab's **Inkling-Small**

## Answer:

Thinking Machines Lab released **Inkling-Small**, an open-weight multimodal Mixture-of-Experts (MoE) language model designed to bring frontier-model capabilities into a much cheaper and more deployable size. ([Thinking Machines Lab][1])

The key idea:

> **Take a ~1T parameter frontier model (Inkling), compress the useful capability into a much smaller active model, and make it practical for developers.** ([Thinking Machines Lab][2])

---

## 1. Model architecture

Inkling-Small:

```
Total parameters:     276B
Active parameters:     12B
Architecture:          Sparse MoE Transformer
Context window:        up to 1M tokens
Inputs:                text + image + audio
Output:                text
License:               Apache 2.0
```

([Thinking Machines Lab][3])

The important number is **12B active**, not 276B.

During inference:

```
Input token
    |
    v
Router
    |
    +--> Expert 17
    +--> Expert 92
    +--> Expert 201
    +--> ...
    |
    v
Output
```

Only a small subset of experts execute.

Similar idea:

* Mixtral 8x7B
* DeepSeek MoE models
* Switch Transformer

Instead of:

```
Dense model:

Every token
   |
   v
All parameters execute

70B model = 70B compute
```

MoE:

```
Every token
   |
   v
Choose experts

276B total
but ~12B compute
```

This gives:

* large knowledge capacity
* lower inference cost
* better scaling

---

## 2. Why is it interesting?

The AI industry is moving from:

```
Bigger model
      |
      v
More parameters
```

towards:

```
Better architecture
      |
      v
Efficient reasoning + agents
```

Inkling-Small focuses on:

### A. Reasoning

It supports **controllable thinking effort**.

Meaning:

```
cheap mode:

question
  |
  v
few reasoning tokens
  |
answer


expensive mode:

question
  |
  v
long chain-of-thought
  |
better answer
```

You trade:

```
latency / cost

       vs

accuracy
```

([Thinking Machines Lab][1])

---

### B. Agent coding

The model is optimized for:

* coding agents
* tool usage
* terminal tasks
* RAG systems

Reported:

* SWE-bench Verified: ~80% range

Meaning it can autonomously modify code repositories. ([Thinking Machines Lab][1])

A typical workflow:

```
User:

"Fix this bug"

       |
       v

Inkling-Small

       |
       +-- read repo
       |
       +-- run tests
       |
       +-- edit files
       |
       +-- verify
```

---

### C. Native multimodal

Unlike old LLM + separate vision model:

```
Old:

Image
 |
Vision encoder
 |
LLM


New:

text tokens
image tokens
audio tokens

       |
       v

same transformer
```

Inkling-Small directly handles:

* text
* images
* audio

([Thinking Machines Lab][4])

---

## 3. Comparison with other open models

Rough positioning:

| Model          | Total Params | Active Params  | Type  |
| -------------- | ------------ | -------------- | ----- |
| Llama 3.1 405B | 405B         | 405B           | Dense |
| Qwen3 235B     | 235B         | 235B           | Dense |
| DeepSeek MoE   | large        | smaller active | MoE   |
| Inkling        | 975B         | 41B            | MoE   |
| Inkling-Small  | 276B         | 12B            | MoE   |

([Thinking Machines Lab][2])

Inkling-Small's trick:

```
Knowledge capacity ≈ huge model

Inference cost ≈ 12B model
```

---

## 4. Hardware implications

For local deployment:

### BF16

276B weights:

```
276B * 2 bytes

≈ 552GB VRAM
```

Impossible for normal GPUs.

But because MoE inference only activates 12B:

You still need to store experts.

Typical deployment:

```
8x H100 / H200
or
multi-GPU server
```

For consumer GPUs:

```
RTX 4090 24GB
RTX 5090 32GB
RTX 6000 Ada 48GB

not enough for full BF16
```

Quantized versions help:

```
NVFP4 / FP8

much smaller memory footprint
```

([Hugging Face][5])

---

## 5. Why this matters for AI engineers

For someone building agents, this is more important than benchmark numbers.

The future stack:

```
        User
         |
         v
    AI Agent
         |
 +-------+-------+
 |               |
Reasoning      Tools
Model          Browser
 |               |
Coding         APIs
Model          Database
```

Small efficient frontier models become the "CPU" of agents.

Examples:

* coding assistant
* enterprise automation
* customer support agent
* AI tutor
* research agent

---

## 6. Compared with your local experiments

Given your GPT-2/nanochat training background:

Inkling-Small shows the direction after GPT-style scaling.

GPT-2:

```
Dense Transformer

124M params
760M params
```

Modern frontier:

```
MoE Transformer

276B params
12B active
```

The evolution:

```
GPT-2 (2019)

all parameters always active


↓

GPT-3

bigger dense


↓

Mixtral / DeepSeek / Inkling

conditional computation


↓

Future models

reasoning + agents + multimodal
```

The core research question changed from:

> "How do we make the model bigger?"

to:

> "How do we spend compute only where intelligence is needed?"

---

References:

* ([Thinking Machines Lab][1])
* ([Thinking Machines Lab][2])
* ([Thinking Machines Lab][4])
* ([Hugging Face][5])

[1]: https://thinkingmachines.ai/news/inkling-small/?utm_source=chatgpt.com "Introducing Inkling-Small - Thinking Machines Lab"
[2]: https://thinkingmachines.ai/news/introducing-inkling/?utm_source=chatgpt.com "Inkling: Our Open-Weights Model - Thinking Machines Lab"
[3]: https://thinkingmachines.ai/inkling/?utm_source=chatgpt.com "Inkling - Thinking Machines Lab"
[4]: https://thinkingmachines.ai/model-card/inkling-small/?utm_source=chatgpt.com "Inkling-Small Model Card - Thinking Machines Lab"
[5]: https://huggingface.co/thinkingmachines/Inkling-Small?utm_source=chatgpt.com "thinkingmachines/Inkling-Small · Hugging Face"
