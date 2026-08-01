---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open Source Contributions for AI Career
translated: false
type: note
---

**Question: Should I participate in open source projects like SGLang and vLLM to build my AI career?**

**Answer: Yes. For your direction (LLM infra / AI engineering), contributing to open source is one of the highest-leverage things you can do.**

For AI infra, a GitHub history is often stronger evidence than a certificate or even a degree because it shows:

* you can read a large codebase
* you understand systems deeply
* you can debug real production problems
* you can collaborate with researchers/engineers globally

Projects like vLLM and SGLang are exactly in the area you are targeting.

A good path:

```
nanoGPT
   |
   v
nano-vLLM
   |
   v
vLLM / SGLang internals
   |
   +--> CUDA kernels
   |
   +--> KV cache
   |
   +--> scheduler
   |
   +--> distributed inference
   |
   v
AI infra engineer
```

You already have a good foundation:

* trained GPT-2 from scratch
* used nano-vLLM
* ran Qwen models
* touched ROCm / MI300X
* understand GPU memory constraints

The next step is not another tutorial. It is **becoming a contributor**.

---

## Start small: don't try to rewrite vLLM

Large projects have thousands of lines. First contributions should be:

### 1. Documentation fixes

Example:

```
docs/
  installation.md
  troubleshooting.md
```

Find:

* outdated CUDA version
* missing environment variables
* confusing instructions

Submit PR.

This teaches the workflow.

---

### 2. Bug reproduction

Example:

```
Issue:
vLLM crashes with Qwen3 + long context + RTX 4090

Your contribution:

1. reproduce
2. create minimal script
3. identify stack trace
4. propose fix
```

This is very valuable.

---

### 3. Small code improvements

Examples:

Python:

```python
# before
if x is not None:
    do_work(x)

# after
if x:
    do_work(x)
```

or better error messages.

Not glamorous, but it gets you into the project.

---

## Then move toward core areas

For your background, I would focus on:

### KV cache

Understand:

```
Attention:

Q = XWq
K = XWk
V = XWv


Attention(Q,K,V)

= softmax(QK^T / sqrt(d))V
```

During decoding:

```
token 1:
K1,V1

token 2:
K1,K2
V1,V2

token 3:
K1,K2,K3
V1,V2,V3
```

Instead of recomputing:

```
KV cache
```

stores previous K/V.

vLLM's major innovation:

```
PagedAttention

GPU memory
+
OS virtual memory idea

=
KV cache pages
```

This is a beautiful area.

---

### Scheduler

LLM serving is not just GPU compute.

You need:

```
requests:

A: 1000 tokens
B: 20 tokens
C: 500 tokens


scheduler decides:

who gets GPU time?
how many tokens per batch?
when to preempt?
```

This is where companies need engineers.

---

### CUDA kernels

Eventually:

```cpp
__global__
void attention_kernel(
    float* Q,
    float* K,
    float* V
)
{
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
}
```

You don't need to become a CUDA expert immediately.

But understanding:

```
thread
warp
block
shared memory
tensor core
memory bandwidth
```

is a huge advantage.

---

## A realistic 6-month target

Given your current level:

### Month 1

```
clone vllm
build locally
run tests
read architecture
submit docs PR
```

### Month 2-3

```
fix small bugs
add tests
understand scheduler
understand KV cache
```

### Month 4-6

```
contribute feature/performance improvement

example:

- new model support
- ROCm improvement
- memory optimization
- benchmark improvement
```

A GitHub profile showing:

```
lzwjava
 |
 +-- nanoGPT experiments
 +-- nano-vLLM implementation
 +-- vLLM PRs
 +-- CUDA kernels
 +-- inference benchmarks
```

is a very strong AI infra portfolio.

The key mindset shift:

Don't only **consume** AI papers and repositories.

Become part of the ecosystem that creates them. That is how you move from "learning AI" to "being an AI engineer."
