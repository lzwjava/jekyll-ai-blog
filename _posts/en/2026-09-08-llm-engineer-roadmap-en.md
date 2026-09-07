---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Engineer Roadmap
translated: false
type: note
---

## Question: Give me a serious plan to learn AI/LLM engineering

## Answer:

Given your current level, **do not follow a beginner “learn AI” curriculum**. You already have PyTorch, CUDA/GPU, GPT training, vLLM, KV cache, and distributed-training exposure.

I would structure your next **12 months around one goal**:

> **Become the engineer who can understand, modify, train, optimize, and serve an LLM from CUDA kernel → distributed training → model architecture → inference system.**

The key is to learn by **building progressively larger systems**, not by collecting courses.

### The roadmap

```text
                 AI / LLM Engineer
                        │
        ┌───────────────┼────────────────┐
        ↓               ↓                ↓
    MODEL/ML         TRAINING          SYSTEMS
        │               │                │
 Transformer       PyTorch DDP       CUDA
 MoE               FSDP/ZeRO         Triton
 Attention         TP/PP             NCCL
 MTP               Checkpointing     FlashAttention
 RL/Post-training  Scaling laws      GPU memory
        │               │                │
        └───────────────┼────────────────┘
                        ↓
                    INFERENCE
                        │
               KV Cache / PagedAttention
               Continuous batching
               Quantization
               Speculative decoding
               vLLM / SGLang
                        ↓
                 FRONTIER RESEARCH
                        │
             MoE / MLA / MTP / FP4
             distributed inference
             training efficiency
```

---

# Phase 0 — 1 week: consolidate fundamentals

Don't spend months here.

You should be able to derive these from memory:

### Transformer

```text
X
 ↓
Q = XWq
K = XWk
V = XWv
 ↓
Attention(Q,K,V)
    = softmax(QKᵀ / √d)V
 ↓
O projection
 ↓
MLP / MoE
 ↓
residual
 ↓
LayerNorm/RMSNorm
```

Then understand:

* BPE/tokenization
* embeddings
* positional encoding / RoPE
* MHA
* MQA
* GQA
* RMSNorm
* SwiGLU
* residual connections
* logits
* cross entropy
* autoregressive training
* teacher forcing

But **implement everything yourself**.

Your minimum project:

```bash
nano transformer.py
```

Implement:

```python
class Attention(nn.Module):
    ...

class MLP(nn.Module):
    ...

class TransformerBlock(nn.Module):
    ...

class GPT(nn.Module):
    ...
```

Then train it on a tiny corpus.

Your existing GPT-2-from-scratch work means this should be very fast for you.

---

# Phase 1 — 2–3 weeks: understand GPT deeply

Use **nanoGPT → nanochat** as the main curriculum.

Karpathy's current GitHub lineup is unusually good for this: `nanoGPT`, `nanochat`, `llm.c`, `llama2.c`, `micrograd`, and `microgpt` are all explicitly designed around minimal implementations. ([GitHub][1])

[Karpathy's GitHub](https://github.com/karpathy?utm_source=chatgpt.com)

Don't merely run nanochat.

Read it in this order:

```text
tokenizer
   ↓
dataset
   ↓
model
   ↓
forward()
   ↓
loss
   ↓
backward()
   ↓
optimizer
   ↓
distributed training
   ↓
checkpoint
   ↓
inference
   ↓
serving
```

The current nanochat project actually recommends following the code according to the training pipeline, starting with distributed setup and tokenizer implementation. 

### Your assignment

Modify nanochat.

For example:

```text
Experiment 1:
    change RoPE

Experiment 2:
    change RMSNorm

Experiment 3:
    change attention implementation

Experiment 4:
    add GQA

Experiment 5:
    add a different activation

Experiment 6:
    change tokenizer vocabulary

Experiment 7:
    change optimizer

Experiment 8:
    change learning-rate schedule
```

Every experiment should produce:

```text
git commit
training log
validation loss
tokens/sec
GPU memory
short note explaining result
```

This is how you transition from **LLM user → LLM engineer**.

---

# Phase 2 — 1 month: GPU + CUDA

This is where I would spend significant time given your interests.

You don't need to become a CUDA compiler engineer immediately.

You need to understand:

```text
Python
 ↓
PyTorch
 ↓
ATen
 ↓
CUDA kernel
 ↓
GPU SM
 ↓
Tensor Core
 ↓
HBM
```

Learn:

### GPU architecture

```text
SM
├── CUDA cores
├── Tensor cores
├── registers
├── shared memory
└── L1 cache

GPU
├── SM
├── SM
├── SM
└── ...

        ↓

       HBM
```

Understand:

* occupancy
* warps
* threads
* blocks
* registers
* shared memory
* coalesced memory access
* memory bandwidth
* arithmetic intensity
* Tensor Cores
* FP32 / BF16 / FP16 / FP8 / FP4
* GEMM

Then write CUDA.

Start with:

```cpp
vector_add.cu
```

then:

```text
matmul
 ↓
tiled matmul
 ↓
softmax
 ↓
layernorm
 ↓
attention
```

The important question becomes:

> **Why is this kernel slow?**

rather than:

> How do I call this PyTorch API?

---

# Phase 3 — 1 month: implement FlashAttention

This should be one of your major milestones.

Start from:

```python
Q @ K.T
softmax()
@ V
```

Then understand why the naive implementation materializes:

```text
QKᵀ
```

which is:

```text
O(N²)
```

in memory.

Then derive tiled attention.

The fundamental idea:

```text
HBM
 ↓
load Q/K/V tiles
 ↓
SRAM/shared memory
 ↓
compute
 ↓
don't materialize full attention matrix
 ↓
write output
```

Then implement a simplified CUDA version.

After that read real implementations.

This will make later topics like:

* FlashInfer
* FlashAttention
* MLA
* PagedAttention
* attention backends

much easier.

---

# Phase 4 — 1 month: distributed training

Now learn how one GPU becomes 8 → 64 → 1,000 GPUs.

Order:

```text
single GPU
    ↓
DDP
    ↓
FSDP
    ↓
Tensor Parallel
    ↓
Pipeline Parallel
    ↓
3D parallelism
```

PyTorch's current distributed stack explicitly covers DDP, FSDP2, Tensor Parallel, DeviceMesh, RPC, and related distributed mechanisms. ([PyTorch Documentation][2])

Start with DDP:

```bash
torchrun \
  --nproc_per_node=8 \
  train.py
```

Understand exactly what happens:

```text
GPU 0                    GPU 1

forward                  forward
   ↓                        ↓
loss                     loss
   ↓                        ↓
backward                 backward
   ↓                        ↓
gradient ───── NCCL ───── gradient
             all-reduce
                 ↓
          synchronized grads
```

Then FSDP.

The important difference:

```text
DDP:

GPU0: full model
GPU1: full model
GPU2: full model
GPU3: full model


FSDP:

GPU0: shard
GPU1: shard
GPU2: shard
GPU3: shard
```

FSDP shards parameters, gradients, and optimizer states, using all-gather during computation and reduce-scatter for gradients. ([PyTorch Documentation][3])

Then implement:

```text
8 GPU GPT training
```

yourself.

---

# Phase 5 — 1 month: LLM inference

You have already started this area. Go much deeper.

Learn:

```text
prefill
decode
KV cache
continuous batching
PagedAttention
prefix caching
chunked prefill
quantization
speculative decoding
```

The mental model:

```text
Prompt
  │
  ▼
PREFILL
  │
  ├── compute all tokens
  └── create KV cache
          │
          ▼
       DECODE
          │
       token 1
          │
       token 2
          │
       token 3
          │
          ...
```

Then understand why inference is frequently **memory-bandwidth/KV-cache constrained**, rather than simply FLOP constrained.

Then read vLLM source.

Current vLLM has a substantial inference stack around PagedAttention, continuous batching, prefix caching, chunked prefill, quantization, CUDA/HIP graphs, optimized attention/GEMM/MoE kernels, and speculative decoding. ([vLLM][4])

Your project:

```text
mini-vllm/
    scheduler.py
    kv_cache.py
    block_manager.py
    attention.py
    worker.py
    engine.py
```

Implement:

```text
request queue
     ↓
scheduler
     ↓
KV cache manager
     ↓
batch
     ↓
model forward
     ↓
sample
     ↓
return token
```

You will understand vLLM much more deeply afterward.

---

# Phase 6 — 1 month: MoE

This should be your next major architecture project.

You recently asked about learning MoE. I think it's **exactly the right direction for you now**.

Start with:

```text
Dense FFN

x
│
▼
W1
│
activation
│
▼
W2
│
▼
output
```

Then:

```text
MoE

             ┌── Expert 1
             ├── Expert 2
x → Router ──┼── Expert 3
             ├── Expert 4
             └── Expert N
```

Learn:

* top-k routing
* expert capacity
* auxiliary loss
* load balancing
* expert parallelism
* all-to-all communication
* token dispatch
* token combine
* expert parallel + tensor parallel
* MoE inference

Then implement:

```python
class MoE(nn.Module):
    def forward(self, x):
        scores = self.router(x)
        experts = topk(scores)

        ...
```

Then benchmark:

```text
Dense 7B
vs
MoE 8x1B
```

Compare:

```text
FLOPs
active parameters
total parameters
tokens/sec
memory
communication
quality
```

This teaches you why modern LLM architecture increasingly looks like a **distributed systems problem**.

---

# Phase 7 — 1–2 months: post-training

Only after understanding pretraining should you go deep here.

Learn:

```text
SFT
 ↓
Preference data
 ↓
Reward modeling
 ↓
DPO
 ↓
RL
 ↓
GRPO / PPO-like methods
 ↓
reasoning models
```

Understand the mathematical objective.

For SFT:

```text
L = -Σ log pθ(y_t | x, y_<t)
```

For DPO, understand the relationship between:

```text
policy
reference model
chosen response
rejected response
```

Don't start by memorizing frameworks.

Implement a minimal version in PyTorch.

---

# Phase 8 — 1–2 months: modern LLM architecture

Then start reading papers and source code aggressively.

Priority:

### Architecture

```text
Transformer
RoPE
GQA
MoE
MLA
MTP
Long context
```

### Efficiency

```text
FlashAttention
PagedAttention
Quantization
FP8
FP4/NVFP4
Speculative decoding
MTP
```

### Training

```text
Scaling laws
Data mixture
Data quality
Distributed training
Checkpointing
Fault tolerance
```

### Systems

```text
CUDA
Triton
CUTLASS
NCCL
PyTorch compiler
vLLM
SGLang
```

---

# Your 12-month project sequence

I would literally put these in GitHub:

```text
01-micrograd
02-microgpt
03-tiny-transformer
04-gpt-from-scratch
05-gpt-pretraining
06-cuda-matmul
07-cuda-attention
08-flash-attention
09-ddp-training
10-fsdp-training
11-tensor-parallel-gpt
12-mini-vllm
13-moe
14-moe-distributed
15-speculative-decoding
16-mtp
17-quantization
18-llm-post-training
19-research-project
```

That portfolio is much more valuable than:

```text
10 certificates
50 courses
300 papers bookmarked
```

---

# The weekly schedule I'd use

If you can dedicate ~20 hours/week:

```text
Monday
  2h paper/source reading
  1h math

Tuesday
  3h implementation

Wednesday
  3h CUDA/PyTorch internals

Thursday
  3h implementation

Friday
  2h benchmarking/profiling

Saturday
  5h serious project

Sunday
  1h write notes
```

The ratio should be roughly:

```text
70% coding
20% reading
10% theory
```

For you, **not**:

```text
70% courses
20% videos
10% coding
```

---

# The most important learning loop

For every new technology:

```text
READ
 ↓
IMPLEMENT
 ↓
BENCHMARK
 ↓
BREAK IT
 ↓
PROFILE
 ↓
READ SOURCE
 ↓
MODIFY
 ↓
BENCHMARK AGAIN
```

For example, don't learn KV cache by watching a video.

Build:

```python
# naive
generate(prompt)

# cached
generate_with_kv_cache(prompt)
```

Then measure:

```text
tokens/sec
GPU memory
prefill latency
decode latency
```

Then break the implementation.

Then fix it.

**That is real LLM engineering.**

---

# What I would prioritize specifically for you

I would **not** spend much time on:

```text
❌ classical ML
❌ sklearn
❌ basic CNNs
❌ generic AI courses
❌ prompt engineering
❌ RAG tutorials
❌ LangChain tutorials
❌ "AI agent 101"
```

Your highest-value path is:

```text
                 YOU
                  │
          Transformer internals
                  │
          CUDA / GPU architecture
                  │
        Distributed training
                  │
             MoE / MTP
                  │
          Inference systems
                  │
        Quantization / kernels
                  │
          Post-training / RL
                  │
             Research
```

And your existing hardware experience is actually an advantage here: **GPU memory, PCIe, CUDA failures, multi-GPU topology, VRAM limitations, kernel performance, and model offloading are not side topics—they are the actual engineering constraints.**

For distributed training, learn DDP → FSDP2 → TP rather than jumping straight into a giant framework; PyTorch's current documentation provides exactly this progression. ([PyTorch Documentation][2])

### Your immediate next 30 days

If I were you, I'd do exactly this:

```text
Week 1
  nanochat source
  Transformer internals
  tokenizer
  training loop

Week 2
  modify nanochat
  implement GQA
  implement RoPE variant
  benchmark

Week 3
  CUDA
  tiled GEMM
  softmax
  LayerNorm
  profiling

Week 4
  FlashAttention
  KV cache
  read vLLM attention implementation
```

Then:

```text
Month 2 → DDP + FSDP + NCCL
Month 3 → Tensor Parallel + Pipeline Parallel
Month 4 → MoE
Month 5 → MoE distributed
Month 6 → vLLM / inference
Month 7 → CUDA/Triton kernels
Month 8 → quantization + FP8/FP4
Month 9 → speculative decoding + MTP
Month 10 → SFT/DPO/RL
Month 11 → reproduction of a recent paper
Month 12 → your own research/optimization project
```

The end goal isn't to know every LLM technique.

It's to be able to take a paper saying:

> "We introduce a new attention/MoE/training optimization"

and within a few days **understand the math, find the relevant code, implement a minimal version, run an experiment, profile it on a GPU, and explain whether it actually works.**

That's the level I'd target.

I can also turn this into a **concrete 6-month repo-by-repo curriculum**, with exactly which GitHub projects to clone, which files to read, and what code you should implement each week.

[1]: https://github.com/karpathy?utm_source=chatgpt.com "karpathy (Andrej) · GitHub"
[2]: https://docs.pytorch.org/tutorials/distributed.html?utm_source=chatgpt.com "Distributed — PyTorch Tutorials 2.14.0+cu130 documentation"
[3]: https://docs.pytorch.org/tutorials/intermediate/FSDP1_tutorial.html?utm_source=chatgpt.com "Getting Started with Fully Sharded Data Parallel(FSDP) — PyTorch Tutorials 2.14.0+cu130 documentation"
[4]: https://docs.vllm.ai/en/stable/?utm_source=chatgpt.com "vLLM"