---
audio: false
generated: true
image: false
lang: en
layout: post
title: FreeToken Efficient Local MoE
translated: false
type: note
---

Question: What is the FreeToken paper?

Answer:

**FreeToken** is a paper about making **very large Mixture-of-Experts (MoE) LLMs run locally on normal computers**, by optimizing the inference system rather than changing the model. The paper title is:

> **“FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution”**
> arXiv:2608.16157 ([arXiv][1])

The key idea:

> Treat your PC as a small distributed system: GPU VRAM + CPU RAM + PCIe bandwidth + model cache, instead of thinking “my GPU is too small.”

([Hugging Face][2])

---

## The problem

Modern MoE models are huge.

Example:

```
GLM-5.2
753B parameters
```

A naive calculation:

```
753B params × 2 bytes (BF16)

≈ 1.5 TB memory
```

Impossible for:

```
RTX 4090 24GB
RTX 5090 32GB
```

Normally you need:

```
8 × H100
16 × H100
large datacenter
```

---

## But MoE has a trick

Mixture-of-Experts model:

```
              Input token

                  |
                  v

        Router chooses experts

          /       |       \

     Expert 1  Expert 2  Expert 3
                  ^
                  |
              only a few active
```

A 700B model might have:

```
Total experts:
700B parameters

Active per token:
30B parameters
```

So computation is small, but memory is the problem.

The question:

> How do we move the right experts to GPU fast enough?

---

## Previous approach: static offloading

Example:

```
GPU VRAM:

Expert 1
Expert 2
Expert 3


CPU RAM:

Expert 4
Expert 5
Expert 6
...
```

Problem:

The router changes every token.

Token 1:

```
needs Expert 1,2,3
```

Token 2:

```
needs Expert 20,21,22
```

Now PCIe transfer becomes the bottleneck.

---

## FreeToken's idea

FreeToken makes GPU memory a **dynamic cache**.

Like CPU cache:

```
RAM
 |
 |  slower
 v

GPU VRAM
 |
 | faster
 v

Tensor Core
```

The system watches:

```
Which experts are frequently used?
```

Then keeps hot experts:

```
GPU:

Expert 7
Expert 15
Expert 21

(cache)
```

Moves cold experts:

```
CPU RAM
```

This is similar to:

* OS page cache
* CPU L1/L2 cache
* Redis hot-key caching

---

## Another important idea: bandwidth-aware execution

They measure:

```
GPU compute speed

vs

PCIe transfer speed

vs

CPU memory bandwidth
```

Then decide:

```
Should CPU calculate this expert?

or

Should we move it to GPU?
```

Not a fixed rule.

The hardware decides.

([FreeToken Wiki][3])

---

## Why MIT/Berkeley people are mentioned?

The author list includes researchers such as:

* Song Han
* Matei Zaharia
* Ion Stoica

([arXiv][1])

These are people behind important systems:

```
Deep learning hardware optimization
+
distributed systems
+
cloud infrastructure
```

For example:

* Song Han → efficient neural networks, TensorRT-related ecosystem
* Matei Zaharia → Spark, ML systems
* Ion Stoica → Apache Spark, Ray, distributed systems

---

## Why it matters for someone like you building local AI

Your current setup:

```
RTX 4070 Ti 12GB
```

Traditional thinking:

```
12GB VRAM
      |
      v
cannot run huge models
```

FreeToken thinking:

```
RTX 4070 Ti
+
64/128GB RAM
+
PCIe
+
smart caching

=
larger model possible
```

The future stack becomes:

```
Model
 |
 v
Inference engine
 |
 +-- vLLM
 +-- SGLang
 +-- FreeToken
 +-- llama.cpp
 |
 v
Hardware abstraction
 |
 v
Consumer GPU
```

The breakthrough is not a new Transformer layer. It is **systems engineering**.

Similar to what happened with databases:

```
Hardware improved
+
software improved

=
new possibilities
```

LLM inference is entering that phase.

([github.com][4])

References:

* FreeToken paper: ([arXiv][1])
* FreeToken GitHub: ([github.com][5])
* Paper summary: ([Hugging Face][2])

[1]: https://arxiv.org/abs/2608.16157?utm_source=chatgpt.com "FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution"
[2]: https://huggingface.co/papers/2608.16157?utm_source=chatgpt.com "Paper page - FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution"
[3]: https://www.freetoken.wiki/architecture/FreeToken-paper?utm_source=chatgpt.com "FreeToken paper: MoE Serving Comparison and Setup Guide - FreeToken Wiki"
[4]: https://github.com/FlashML-org/FreeToken/blob/main/README.md?utm_source=chatgpt.com "FreeToken/README.md at main · FlashML-org/FreeToken · GitHub"
[5]: https://github.com/FlashML-org/FreeToken?utm_source=chatgpt.com "GitHub - FlashML-org/FreeToken · GitHub"
