---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Data and Compute: LLM Bottleneck"
translated: false
type: note
---

Question: Is LLM progress more likely to come from architecture innovation, or is the main bottleneck still data?

Answer:

Yes, architecture innovation is worth exploring, but for current LLMs the bottleneck is often **data + compute + scaling recipe**, not just the Transformer block.

A useful decomposition:

```
Model quality ≈ Architecture × Data × Optimization × Compute
```

For GPT-scale models, architecture improvements usually give **10–30% gains**, while better data can give **multiples**.

---

## 1. Why data became the hard part

Early GPT:

```
GPT-2 (2019)
parameters: 1.5B
training tokens: ~40B
```

Today:

```
Large models:
parameters: hundreds of billions
tokens: trillions
```

The internet is finite. High-quality text is even more finite.

The problem is not:

> "Can we collect more text?"

It is:

> "Can we create more high-quality learning signal?"

Examples:

### Bad data

```
"The cat sat on the mat."
"The cat sat on the mat."
(repeated 1 million times)
```

No new information.

### Good data

```
A textbook explaining physics
A GitHub repo with bugs and fixes
A mathematical proof
A scientific paper
A long reasoning trace
A high-quality conversation
```

The model learns the underlying distribution.

---

## 2. Architecture still has huge opportunities

Transformer is probably not the final architecture.

Current Transformer:

```
Token
 |
Embedding
 |
Attention
 |
MLP
 |
Attention
 |
MLP
 |
...
 |
Output
```

The core limitation:

Attention:

$$
O(n^2)
$$

For context length:

```
4K tokens     OK
128K tokens   expensive
1M tokens     painful
```

Possible directions:

---

### A. Better memory systems

Human brain does not store everything in working memory.

Current LLM:

```
Input context
     |
Transformer
     |
Answer
```

Future:

```
Short-term memory
        |
        v
Reasoning engine
        |
        v
Long-term memory database
```

This is why agent systems are interesting.

---

### B. Mixture of Experts (MoE)

Instead of:

```
Every token uses all parameters

70B model
==========
70B active
```

Use:

```
70B total

Token 1 -> expert 3
Token 2 -> expert 7
Token 3 -> expert 12
```

Only activate part.

This gives:

```
larger knowledge
lower inference cost
```

---

### C. Neural + symbolic hybrids

Current LLM:

```
weights = memory
```

Problem:

Updating knowledge requires retraining.

Future:

```
LLM
 |
 +-- neural reasoning
 |
 +-- database
 |
 +-- code execution
 |
 +-- simulator
```

Similar to how humans work.

---

### D. New training objectives

Current:

Predict next token:

$$
P(x_{t+1}|x_1...x_t)
$$

Maybe not optimal.

Humans learn:

* predict future
* interact
* experiment
* fail
* correct

A baby does not learn by reading 10 trillion tokens.

Future:

```
world model
+
simulation
+
action
+
feedback
```

---

## 3. For someone like you, architecture exploration is actually reasonable

Because you already trained:

* GPT-2 124M
* nanoGPT experiments
* small models

The next step is not necessarily "train another GPT-2".

More interesting:

Build tiny models that test ideas.

Example:

```
my-model/
 ├── transformer.py
 ├── moe.py
 ├── memory.py
 ├── retrieval.py
 ├── trainer.py
```

Experiments:

### Experiment 1: Add external memory

Baseline:

```
GPT-124M
```

Compare:

```
GPT-124M
+
vector memory
```

Measure:

* perplexity
* long-context recall
* QA accuracy

---

### Experiment 2: Replace attention

Implement:

```
Attention
      |
      v
Linear Attention
      |
      v
State Space Model (Mamba style)
```

Compare:

```
speed
memory
quality
```

---

### Experiment 3: Data engineering

This may actually produce bigger gains.

Example:

Take your FineWeb dataset:

```
100B tokens
```

Instead of random sampling:

```
raw web
 |
quality filter
 |
dedup
 |
education score
 |
code score
 |
reasoning score
 |
train
```

A 10B-token high-quality dataset can beat 100B-token garbage.

---

My view:

For the next few years:

```
Foundation model labs:
    architecture + huge data + compute

Small teams / individuals:
    data innovation + agent architecture + specialized models
```

A single person probably won't beat NVIDIA/OpenAI at inventing the next Transformer.

But a person can absolutely discover:

* a better dataset
* a better training recipe
* a better memory system
* a better small model architecture

Your current path (training small models + understanding hardware + distributed training) is actually closer to how many important ideas are born: build small, measure, iterate.
