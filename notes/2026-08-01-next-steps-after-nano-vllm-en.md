---
audio: false
generated: true
image: false
lang: en
layout: post
title: Next Steps After Nano-vLLM
translated: false
type: note
---

Question: After learning nano-vLLM, what should I learn next?

Answer:

Given your trajectory (training GPT-2 from scratch, nanochat, nano-vLLM, vLLM experiments, GPU debugging), the highest ROI next step is **not another toy project**. You should move one layer deeper and connect the full LLM serving/training stack.

A good path:

```
nano-vllm
    |
    v
vLLM internals
    |
    +--> PagedAttention
    +--> KV cache manager
    +--> CUDA kernels
    +--> Continuous batching
    |
    v
Distributed inference
    |
    +--> Tensor Parallel
    +--> Pipeline Parallel
    +--> Expert Parallel (MoE)
    |
    v
Training systems
    |
    +--> DeepSpeed
    +--> Megatron-LM
    +--> FSDP
    |
    v
Production AI Infra
    |
    +--> Kubernetes
    +--> GPU scheduling
    +--> observability
```

## 1. Read real vLLM source code

After nano-vLLM, move to:

vLLM

Focus files:

```
vllm/
├── engine/
│   ├── llm_engine.py
│   └── async_llm_engine.py
│
├── worker/
│   ├── worker.py
│
├── attention/
│   ├── backend.py
│
├── core/
│   ├── block_manager.py
│   └── scheduler.py
```

Understand the forward path:

```
HTTP request
      |
      v
AsyncLLMEngine
      |
      v
Scheduler
      |
      +---- waiting queue
      |
      +---- running queue
      |
      v
KV Cache allocation
      |
      v
Model forward()
      |
      v
Sampler
      |
      v
Token response
```

The key insight:

LLM serving is mostly a **memory management problem**, not a compute problem.

---

## 2. Implement your own PagedAttention

This is probably the most valuable exercise.

Normal KV cache:

```
Request A:
[0][1][2][3][4][5]

Request B:
[0][1][2][3]
```

Problem:

Different requests have different lengths.

Memory fragmentation.

PagedAttention:

```
GPU KV memory:

Block 0 -> A token 0-15
Block 1 -> B token 0-15
Block 2 -> A token 16-31
Block 3 -> C token 0-15
```

Like OS virtual memory:

```
Virtual address
        |
        v
Page table
        |
        v
Physical GPU memory
```

This is where your systems background becomes valuable.

---

## 3. Learn CUDA kernels

You don't need to become a CUDA researcher, but understand:

* memory coalescing
* shared memory
* warp
* occupancy
* tensor cores

Example:

Naive attention:

```python
scores = Q @ K.T
weights = softmax(scores)
out = weights @ V
```

Memory:

```
Q
K
scores   <-- huge
weights  <-- huge
V
```

FlashAttention:

```
Q,K,V
 |
 v
tiles in SRAM
 |
 v
output
```

No giant attention matrix.

Read:

FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

---

## 4. Build a mini distributed inference engine

Use your GPUs.

Example:

```
RTX 4070 12GB
        |
        |
Tensor Parallel
        |
        |
RTX 3060 12GB
```

Split:

```
Linear layer:

Y = XW

W:

GPU0:
W0

GPU1:
W1


Y = concat(
      XW0,
      XW1
)
```

Learn:

* NCCL
* torch.distributed
* tensor parallel

---

## 5. Learn training infrastructure

You already trained GPT-2. Next:

Train a small model with:

* FSDP
* DeepSpeed ZeRO
* Megatron

Understand:

### Data parallel

```
GPU0:
model copy
batch 0


GPU1:
model copy
batch 1


gradient sync
```

### Tensor parallel

```
Layer split across GPUs
```

### Pipeline parallel

```
GPU0:
layers 0-10

GPU1:
layers 11-20
```

---

## 6. Build an AI infra portfolio project

Something like:

```
mini-vllm
+
distributed serving
+
Kubernetes deployment
+
metrics dashboard
```

Architecture:

```
             Client
               |
               v
        FastAPI Gateway
               |
               v
          Scheduler
               |
       +-------+-------+
       |               |
    GPU Worker     GPU Worker
       |               |
       +-------+-------+
               |
            NCCL
```

Deploy:

```
docker-compose
      |
      v
k8s
      |
      v
GPU cluster
```

This is closer to real AI infra jobs.

---

## Recommended 3-month roadmap

### Month 1

```
nano-vllm
    |
    v
vLLM source
    |
    v
PagedAttention implementation
```

Deliverable:

GitHub repo:

```
mini-vllm-paged-attention
```

---

### Month 2

```
CUDA
FlashAttention
Triton
```

Implement:

* layernorm kernel
* softmax kernel
* attention kernel

---

### Month 3

```
distributed inference
+
Kubernetes GPU serving
```

Deploy:

```
Qwen3-8B
or
Llama-3.1-8B
```

with:

* tensor parallel
* metrics
* autoscaling

---

For your background, the strongest positioning is:

> "Backend engineer who understands LLM internals, trained models from scratch, implemented inference engines, and can operate GPU clusters."

That combination is rare. nano-vLLM is a good first step; the next jump is **vLLM internals + CUDA/Triton + distributed systems**.
