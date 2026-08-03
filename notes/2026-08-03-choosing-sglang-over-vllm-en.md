---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choosing SGLang Over vLLM
translated: false
type: note
---

Question: Which repo should I contribute to: SGLang or vLLM?

Answer:

For your background (Java backend → LLM training → nanoGPT → vLLM experiments → CUDA/GPU curiosity), I would prioritize:

**1. Start with SGLang**
SGLang

Why:

* Smaller and faster-moving codebase than vLLM.
* More opportunity for meaningful contributions.
* Strong focus on **agent workloads, structured generation, reasoning models**, which matches where LLM applications are going.
* Easier to understand the full stack:

  ```
  API request
      ↓
  scheduler
      ↓
  tokenizer
      ↓
  KV cache
      ↓
  attention backend
      ↓
  CUDA kernels
      ↓
  GPU
  ```

Good first contributions:

```bash
git clone https://github.com/sgl-project/sglang
cd sglang
```

Study:

```
python/sglang/srt/
├── managers/        # server lifecycle
├── mem_cache/       # KV cache
├── models/          # model wrappers
├── layers/          # transformer layers
├── server_args.py
└── engine/
```

Potential contribution path:

### Level 1: Python engineering

Examples:

* Add model support
* Improve error messages
* Add benchmarks
* Fix compatibility issues

Good because you already have production backend experience.

---

### Level 2: LLM serving internals

Learn:

* continuous batching
* paged attention
* prefix cache
* speculative decoding

Then contribute:

```
scheduler.py
scheduler_output.py
tokenizer_manager.py
```

---

### Level 3: GPU kernel work

Later:

```
sgl-kernel/
flashinfer/
triton kernels
```

Learn:

```python
# simple idea
Q @ K.T -> attention scores
scores @ V -> output
```

GPU optimization:

```
matrix
  ↓
tile
  ↓
shared memory
  ↓
tensor core
  ↓
CUDA kernel
```

---

**2. Then contribute to vLLM**
vLLM

vLLM is the "Linux kernel" of LLM serving.

It has huge industry adoption.

But:

* Larger codebase
* More mature
* Harder for first PR

Architecture:

```
vllm/
├── engine/
├── worker/
├── executor/
├── attention/
├── distributed/
├── model_executor/
└── cuda/
```

The core idea:

```
User request
    |
AsyncLLMEngine
    |
Scheduler
    |
KV Cache Manager
    |
Worker
    |
CUDA Attention Kernel
    |
GPU
```

Good vLLM contribution areas:

* AMD ROCm support
* CUDA kernels
* quantization
* new model architectures
* performance benchmarks

---

My suggested 6-month path:

```
Month 1:
  SGLang
  - run locally
  - read architecture
  - submit docs/tests/small fixes

Month 2-3:
  SGLang internals
  - scheduler
  - KV cache
  - batching

Month 4:
  CUDA/Triton kernel contribution

Month 5-6:
  vLLM contribution
  - deeper inference engine work
```

Your current advantage:

You already have:

* trained GPT-2 from scratch
* used nanoGPT
* touched vLLM
* understand GPU memory limits
* own RTX 4070 environment

Many contributors only know Python APIs. Your path should be:

```
model training
      ↓
PyTorch
      ↓
CUDA kernels
      ↓
inference engine
      ↓
distributed serving
```

That combination is rare.

If your goal is **AI infra engineer job (Hong Kong/Singapore/US)**, a few merged PRs in SGLang/vLLM are probably worth more than another course or another toy chatbot.

References:

* [SGLang GitHub](https://github.com/sgl-project/sglang?utm_source=chatgpt.com)
* [vLLM GitHub](https://github.com/vllm-project/vllm?utm_source=chatgpt.com)
* [SGLang documentation](https://docs.sglang.ai/?utm_source=chatgpt.com)
* [vLLM documentation](https://docs.vllm.ai/?utm_source=chatgpt.com)
