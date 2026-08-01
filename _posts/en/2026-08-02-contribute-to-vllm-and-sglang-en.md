---
audio: false
generated: true
image: false
lang: en
layout: post
title: Contribute to vLLM and SGLang
translated: false
type: note
---

**Question: Should I spend the next months contributing to open source projects like SGLang and vLLM?**

**Answer: Yes. For your current direction, this is probably one of the highest-leverage things you can do.**

Given your background:

* You already trained GPT-2/nanoGPT models.
* You have touched ROCm, MI300X, CUDA, vLLM, nano-vLLM.
* You are aiming for AI infra / LLM engineering roles.
* You lack a traditional CS degree, so **public proof of ability matters a lot**.

Contributing to projects like vLLM and SGLang can create stronger evidence than another certificate or course.

The reason is simple:

A company hiring AI infra engineers asks:

> "Can this person understand a large distributed ML system and improve it?"

A merged PR answers that better than a resume bullet.

---

## Good targets for you

### 1. Start with vLLM

Do not immediately try to rewrite CUDA kernels.

First understand the stack:

```
API server
    |
engine
    |
scheduler
    |
worker
    |
model executor
    |
attention backend
    |
CUDA kernels
```

Your first contributions can be:

* documentation fixes
* bug reproduction
* tests
* performance benchmarks
* small scheduler improvements
* ROCm compatibility
* AMD GPU support

Given your AMD MI300X/ROCm interest, this is actually a niche.

---

### 2. SGLang is also very interesting

SGLang focuses heavily on:

* structured generation
* serving efficiency
* RadixAttention
* KV cache management
* speculative decoding

You already explored KV cache and inference internals, so it matches your learning path.

---

## A realistic 3-month plan

### Month 1: Become a user

Run everything locally.

Example:

```bash
git clone https://github.com/vllm-project/vllm
cd vllm

pip install -e .

python examples/offline_inference/basic.py
```

Then trace:

```
request
 -> scheduler
 -> sequence groups
 -> KV cache allocation
 -> attention
 -> logits
```

Write notes.

---

### Month 2: Pick one subsystem

For example:

KV cache.

Understand:

```
tokens
 |
attention
 |
K,V tensors

K = [num_layers, heads, seq_len, head_dim]
V = [num_layers, heads, seq_len, head_dim]
```

Then study:

* PagedAttention
* block manager
* memory allocation

Make a small improvement.

---

### Month 3: Submit PRs

Good first PR examples:

```
Fix ROCm build issue
Add benchmark
Improve error message
Add test case
Optimize small bottleneck
Update documentation
```

The goal is not fame.

The goal:

```
GitHub profile:
    vLLM PR #xxxxx
    SGLang PR #xxxxx
    CUDA benchmark repo
    nano-vLLM implementation
```

That changes how engineers evaluate you.

---

## A possible personal project combination

I think your strongest portfolio would be:

```
1. nanoGPT
    |
    v
2. nano-vLLM
    |
    v
3. contribute to vLLM/SGLang
    |
    v
4. build an AMD ROCm inference demo
```

This tells a coherent story:

> "I understand training, inference, kernels, and deployment."

Very few engineers can explain the whole pipeline.

---

One warning:

Do not spend 6 months only reading code.

The loop should be:

```
read 20%
modify 30%
break things 30%
submit 20%
```

Large open-source systems are learned by touching them.

For your situation, a merged vLLM/SGLang PR in the next few months is likely worth more than another AI course.