---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build Crude Implementations for Learning
translated: false
type: note
---

Question: Should I build my own vLLM, nanoGPT, CUDA kernels even if they are crude and slow?

Answer:

Yes. For your situation, this is probably one of the highest-leverage things you can do.

The important distinction:

* **Knowing concepts** → you can explain Transformer, KV cache, attention, LoRA, vLLM architecture.
* **Owning the implementation** → you understand why every design choice exists.

Deep AI infra people usually have both.

You don't need to build a production vLLM. You need to build a **small complete stack where every layer is yours**:

```
text
 |
tokenizer
 |
dataset
 |
model.py
 |
attention.py
 |
training loop
 |
optimizer
 |
checkpoint
 |
inference
 |
KV cache
 |
continuous batching
 |
CUDA kernel
```

A crude implementation teaches more than reading 100 papers.

For example:

### 1. nanoGPT level

You already trained GPT-2 124M. Next:

Implement your own:

```python
class CausalSelfAttention(nn.Module):
    def forward(self, x):
        qkv = self.c_attn(x)
        q, k, v = qkv.split(self.n_embd, dim=2)

        att = q @ k.transpose(-2,-1)
        att = att / math.sqrt(q.size(-1))

        mask = torch.tril(torch.ones(T,T))
        att = att.masked_fill(mask == 0, -inf)

        att = softmax(att)

        return att @ v
```

Then ask:

* Why does FlashAttention exist?
* Why does memory become the bottleneck?
* Why does O(N²) attention hurt?
* Why does KV cache change inference complexity?

---

### 2. Mini-vLLM

A tiny vLLM is an excellent project.

Start:

```python
while True:
    request = queue.pop()

    tokens = model.generate(
        input_ids,
        kv_cache
    )

    yield tokens
```

Then add:

**Paged KV cache**

Instead of:

```
request A
[###########........]

request B
[#####.............]
```

use blocks:

```
GPU memory:

block 0 -> request A
block 1 -> request B
block 2 -> request A
block 3 -> request C
```

This teaches why vLLM changed serving.

---

### 3. CUDA kernel

Don't start with FlashAttention.

Start with something embarrassing:

Python:

```python
C = A @ B
```

then CUDA:

```cuda
__global__
void matmul(float *A,float *B,float *C)
{
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    float sum=0;

    for(int k=0;k<N;k++)
        sum += A[row*N+k]*B[k*N+col];

    C[row*N+col]=sum;
}
```

It will be slower than PyTorch.

That is fine.

Then you learn:

* global memory
* shared memory
* warp
* occupancy
* tensor cores
* CUDA graph

---

Your current background actually fits this path:

* Java/backend → distributed systems intuition
* Kubernetes/cloud → serving knowledge
* GPT-2 training → model understanding
* nano-vLLM → inference understanding
* GPU experiments → hardware intuition

The missing piece is not intelligence. It is **time spent implementing the primitives**.

A good 6-month target:

```
Month 1:
  nanoGPT rewrite

Month 2:
  mini-vLLM inference engine

Month 3:
  CUDA extensions

Month 4:
  distributed training toy version

Month 5:
  LoRA + RLHF pipeline

Month 6:
  contribute PRs to vLLM / llama.cpp / PyTorch ecosystem
```

The funny thing about AI infra is that the people who seem "not lost" usually just have 5-10 years of accumulated scars:

* "why is my kernel slow?"
* "why did NCCL hang?"
* "why OOM at batch size 2?"
* "why is GPU utilization 40%?"

Building ugly versions creates those scars.

A slow homemade vLLM running at 5 tokens/s teaches you more than running a perfect vLLM at 200 tokens/s.

For someone aiming at AI infra, "I built a tiny vLLM and CUDA kernels" is a much stronger signal than "I read the vLLM paper."
