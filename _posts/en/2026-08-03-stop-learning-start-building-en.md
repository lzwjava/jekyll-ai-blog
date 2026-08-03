---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stop Learning, Start Building
translated: false
type: note
---

Question: What should I do now, given my current AI engineering path?

Answer:

Given where you are now — you have already trained GPT-2 from scratch, played with nano-vLLM/vLLM, CUDA/ROCm, MI300X, local GPUs, agents, and you are building AI products — the highest-leverage move is **not more random learning**. It is to turn your scattered experiments into a visible AI engineering portfolio.

I would focus on the next 3–6 months like this:

## 1. Pick one "deep engineering mountain": LLM inference stack

Your direction should be:

```
Transformer basics
        ↓
nanoGPT
        ↓
nano-vLLM
        ↓
vLLM / SGLang contribution
        ↓
CUDA kernels / GPU optimization
        ↓
AI infra engineer
```

You already touched many pieces. Now go deeper.

Concrete:

```bash
git clone https://github.com/vllm-project/vllm
git clone https://github.com/sgl-project/sglang
```

Read:

* attention implementation
* KV cache
* paged attention
* continuous batching
* tensor parallelism
* CUDA kernels

Then contribute small PRs:

* documentation improvements
* benchmarks
* bug fixes
* ROCm support
* performance tests

The goal is not just knowledge. The goal is:

> "My GitHub shows I improve the infrastructure used by millions of AI users."

That is a different signal from "I trained another toy model."

---

## 2. Build your own "mini AI infra stack"

You have enough hardware.

Example project:

```
lzw-ai-runtime

model
 |
transformer.py
 |
attention.py
 |
kv_cache.py
 |
scheduler.py
 |
cuda_kernel.cu
 |
benchmark.py
```

Start ugly.

Something like:

```python
while requests:
    batch = scheduler.next_batch()

    logits = model.forward(
        input_ids,
        kv_cache
    )

    next_token = sample(logits)

    update_kv_cache()
```

Then add:

* batching
* streaming output
* OpenAI compatible API
* quantization
* speculative decoding

This becomes your personal vLLM.

---

## 3. Publish everything

You already have an advantage:

Your blog has traffic.

Turn experiments into engineering articles:

Examples:

```
How I trained GPT-2 124M on RTX 4070

Building nano-vLLM from scratch

Understanding PagedAttention by implementing it

CUDA Matrix Multiplication: from naive kernel to Tensor Core

Running LLM inference on AMD ROCm
```

The AI community values:

```
builder + explanation + code
```

more than certificates.

---

## 4. Don't spend too much time on general AI apps

Agents are interesting, but the moat is moving downward.

Thousands of people can build:

```
LangChain + GPT API + UI
```

Far fewer people can explain:

```
Why does vLLM achieve higher throughput?

How does KV cache memory layout work?

How does FlashAttention reduce HBM traffic?
```

Your previous GPU/memory questions are actually pointing in the right direction.

---

## 5. Hardware direction

Your RTX 4070 is enough.

Don't optimize by buying GPUs now.

A good learning setup:

```
RTX 4070
+
cloud MI300X / H100 occasionally
+
AMD ROCm experiments
```

Learn:

```
CUDA
HIP
Triton
CUTLASS
FlashAttention
```

The future AI stack is:

```
Models
   ↓
Inference engines
   ↓
Compiler
   ↓
GPU kernels
   ↓
ASIC hardware
```

You are naturally moving toward the bottom.

---

## 6. Career positioning

Your strongest story is not:

> "I am learning AI."

Your story is:

> "I am a software engineer who built models from scratch, implemented inference engines, optimized GPU workloads, and contributes to open-source AI infrastructure."

That is a rare profile.

---

My suggested immediate next 7 days:

```
Day 1-2:
Read vLLM architecture

Day 3:
Implement simple paged KV cache

Day 4:
Benchmark against naive KV cache

Day 5:
Write blog post

Day 6-7:
Open PR / share project
```

The next step is not another tutorial.

It is shipping something that makes people say:

> "This person understands the AI stack end-to-end."
