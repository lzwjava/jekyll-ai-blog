---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learning LLMs on a 2017 MacBook
translated: false
type: note
---

Question: How can you seriously learn LLMs/PyTorch if this 2017 MacBook Pro is your only machine?

Answer: **Very well, actually — if you separate “learning the mechanics” from “running large models.”**

Your machine is weak for training, but it is **excellent as a CPU development + experimentation machine**:

* 2C/4T i5-7360U
* 15 GB RAM
* Iris Plus 640 — **not useful for modern PyTorch GPU training**
* ~228 GB SSD
* Linux/Ubuntu
* Python 3.13

The key is: **don't try to make this laptop your GPU cluster. Make it your laboratory.**

### 1. Learn PyTorch from first principles locally

Start with tiny tensors and models.

```bash
python3 -m venv ~/venvs/torch
source ~/venvs/torch/bin/activate

pip install torch torchvision torchaudio
```

Then:

```python
import torch

x = torch.randn(4, 8)
W = torch.randn(8, 16, requires_grad=True)

y = x @ W
loss = y.pow(2).mean()

loss.backward()

print(y.shape)
print(W.grad.shape)
```

You can learn almost all of the fundamental PyTorch machinery here:

```text
Tensor
  ↓
matmul
  ↓
forward
  ↓
loss
  ↓
autograd
  ↓
backward
  ↓
gradient
  ↓
optimizer
  ↓
parameter update
```

The computation is tiny, so CPU is completely sufficient.

---

### 2. Build a tiny Transformer

This machine can absolutely train something like:

```text
vocab       10K
context     256
layers      4
hidden      256
heads       4
parameters  ~10–20M
```

For example, implement:

```python
class CausalSelfAttention(nn.Module):
    ...
    
class MLP(nn.Module):
    ...
    
class TransformerBlock(nn.Module):
    ...
    
class GPT(nn.Module):
    ...
```

Then train it on a small corpus.

You don't need an H100 to understand:

```text
token
 ↓
embedding
 ↓
Q K V
 ↓
attention
 ↓
residual
 ↓
LayerNorm
 ↓
MLP
 ↓
residual
 ↓
logits
 ↓
cross entropy
```

In fact, **a slow machine can be pedagogically useful** because you are forced to understand what every operation does rather than throwing a 7B model at a GPU.

---

### 3. Train GPT-2-style models at progressively larger scales

I would use a progression like:

```text
1M       parameters
  ↓
5M
  ↓
10M
  ↓
50M
  ↓
100M
```

The first three are quite realistic on your laptop.

For example:

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT

python train.py \
    --dataset=shakespeare \
    --n_layer=4 \
    --n_head=4 \
    --n_embd=256 \
    --block_size=256 \
    --batch_size=8
```

The point isn't achieving a good benchmark.

The point is being able to inspect:

```python
logits.shape
loss
tokens/sec
memory
gradient norms
parameter count
```

and understand exactly where the compute goes.

---

### 4. You can reproduce the important Transformer mathematics

Your laptop is enough to experiment with things like:

**Attention**

```python
scores = Q @ K.transpose(-2, -1)
scores /= math.sqrt(d_k)

attn = torch.softmax(scores, dim=-1)

out = attn @ V
```

Then investigate:

```text
What happens when d_k changes?
What happens when sequence length doubles?
Why divide by sqrt(d_k)?
What does causal masking actually do?
What does softmax do to information?
```

You can literally print the matrices.

That is much more educational than simply running:

```python
model.generate(...)
```

---

### 5. Learn LLM internals with tiny controlled experiments

For example, study KV caching.

Start with:

```text
Q = x_q W_Q
K = x W_K
V = x W_V

Attention(Q,K,V)
```

Then implement:

```text
prefill
   ↓
K_cache, V_cache
   ↓
decode token 1
   ↓
append K,V
   ↓
decode token 2
   ↓
append K,V
```

You can measure:

```text
sequence length
↓
KV-cache memory
↓
attention computation
↓
decode latency
```

The laptop doesn't need to be fast.

You are studying **the algorithm**.

---

### 6. For large models, use your laptop as the control plane

This is the important architecture:

```text
                    YOUR MACBOOK
                 Ubuntu / Python / Git
                         │
             ┌───────────┴───────────┐
             │                       │
        local CPU               remote GPU
             │                       │
       1–50M models            7B/14B/70B
       tiny datasets           LoRA/QLoRA
       debugging               training
       profiling               inference
```

SSH into a GPU machine:

```bash
ssh <USER>@<GPU_HOST>
```

Then:

```bash
rsync -av ./project/ <USER>@<GPU_HOST>:~/project/
```

or just use Git:

```bash
git push
ssh <GPU_HOST>
git pull
```

This is actually a **very good professional workflow**.

Your laptop doesn't need to own the GPU.

---

### 7. Don't install enormous models locally

Don't do this:

```text
Qwen3-235B
DeepSeek-V3
Llama 405B
```

on this machine.

Instead:

```text
Laptop
  ↓
small models / toy models

Cloud GPU
  ↓
7B / 14B / 32B

Large cluster
  ↓
70B+
```

For inference, you can occasionally use a **small quantized model** locally, but 15 GB RAM means you should think in terms of roughly **1B–7B-class models**, depending heavily on quantization and context length.

---

### 8. You can learn CUDA concepts without CUDA

Your Iris Plus 640 isn't a useful CUDA device.

That's okay.

Understand the abstraction first:

```text
CPU
 ├── cores
 ├── cache
 └── RAM

GPU
 ├── many parallel execution units
 ├── HBM/VRAM
 └── massive memory bandwidth
```

Then understand why:

```python
x @ W
```

is so much faster on a GPU.

Eventually you can move the exact same PyTorch program:

```python
device = "cpu"
```

to:

```python
device = "cuda"
```

on a remote GPU.

That makes the performance difference **meaningful**, because you already understand the computation.

---

### 9. What I would actually study on this laptop

A very strong progression would be:

```text
Week 1
│
├── PyTorch Tensor
├── autograd
├── nn.Module
├── optimizer
└── training loop

Week 2
│
├── linear regression
├── MLP
├── CNN
└── embeddings

Week 3
│
├── attention
├── multi-head attention
├── causal mask
└── positional encoding

Week 4
│
├── Transformer block
├── GPT
├── tokenizer
└── cross entropy

Week 5
│
├── train tiny GPT
├── inspect loss
├── inspect activations
└── inspect gradients

Week 6
│
├── KV cache
├── RoPE
├── RMSNorm
├── GQA/MQA
└── FlashAttention concept

Week 7+
│
├── LoRA
├── QLoRA
├── distributed training concepts
├── quantization
└── inference engines
```

Then use remote GPUs for:

```text
Qwen
Llama
DeepSeek
MoE
LoRA
RLHF/DPO
distributed training
```

---

### 10. The most important thing

Your laptop's limitation can actually force the right learning strategy:

**Don't optimize for model size. Optimize for understanding.**

A 20M-parameter Transformer where you understand every tensor:

```text
[B,T]
 ↓
[B,T,C]
 ↓
Q,K,V
 ↓
[B,H,T,D]
 ↓
QKᵀ
 ↓
[B,H,T,T]
 ↓
softmax
 ↓
attention @ V
 ↓
MLP
 ↓
logits
 ↓
cross entropy
 ↓
backward
```

is vastly more educational than downloading a 32B model and running `ollama run`.

And once you understand that 20M model, the 7B model is mostly **the same mathematics + much more compute + engineering around memory/bandwidth/distribution**.

So yes: **with only this MacBook, you can learn PyTorch and essentially all the mathematical/core architectural foundations of modern LLMs.** You only need rented/remote GPUs when the experiment becomes compute-bound.

References:

* [PyTorch](https://pytorch.org/?utm_source=chatgpt.com)
* [nanoGPT — Andrej Karpathy](https://github.com/karpathy/nanoGPT?utm_source=chatgpt.com)
* [Attention Is All You Need](https://arxiv.org/abs/1706.03762?utm_source=chatgpt.com)
