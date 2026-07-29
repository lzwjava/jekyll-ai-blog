---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix flash-attn CUDA version mismatch
translated: false
type: note
---

Question: How to fix the `flash-attn` install issue (Python 3.14 + CUDA 13.2 vs PyTorch CUDA 12.8 mismatch) and run nano-vLLM experiments with optimized attention?

Answer:

Your current setup is **not broken**. The experiment result is valid. You are running PyTorch SDPA attention, which is the correct fallback.

The issue is:

```
flash-attn
    requires:
        PyTorch CUDA build == system CUDA compatibility
        supported Python version
        matching CUDA toolkit

Your environment:
    Python 3.14
    PyTorch CUDA 12.8
    System CUDA 13.2
```

`flash-attn` is a CUDA extension. It compiles custom kernels against your PyTorch CUDA ABI. The mismatch causes build failure.

---

## Option 1 (recommended): use PyTorch SDPA + Flash backend

Modern PyTorch already contains FlashAttention kernels.

Check:

```python
import torch

print(torch.__version__)
print(torch.version.cuda)

print(torch.backends.cuda.flash_sdp_enabled())
print(torch.backends.cuda.mem_efficient_sdp_enabled())
```

You want:

```
True
True
```

Then in your attention code:

```python
import torch.nn.functional as F

out = F.scaled_dot_product_attention(
    q,
    k,
    v,
    is_causal=True
)
```

PyTorch automatically chooses:

1. FlashAttention kernel
2. Memory efficient attention
3. Math fallback

depending on hardware.

For RTX 4070:

* SDPA Flash kernel should work
* No need for `flash-attn` pip package

---

## Option 2: create a Python 3.12 environment for flash-attn

Python 3.14 is very new. Most CUDA ML packages lag behind.

Create:

```bash
conda create -n vllm python=3.12
conda activate vllm
```

Install PyTorch matching CUDA:

For CUDA 12.8:

```bash
pip install torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu128
```

Verify:

```python
import torch

print(torch.cuda.is_available())
print(torch.version.cuda)
```

Expected:

```
True
12.8
```

Then:

```bash
pip install flash-attn --no-build-isolation
```

---

## Option 3: build flash-attn from source

If you insist on CUDA 13:

```bash
git clone https://github.com/Dao-AILab/flash-attention

cd flash-attention

pip install packaging ninja
pip install .
```

But currently CUDA 13 support is still immature.

---

## For nano-vLLM experiments: keep SDPA

Actually your experiment result is interesting:

```
Short prompt:
~30 ms/token

Long prompt (2K):
~1000+ ms/token
```

This is exactly the KV-cache motivation.

Decode step:

```
new token:
        q

previous tokens:
        K,V

attention:

softmax(qK^T)V
```

Without KV cache:

```
step 1000:

recompute:

K,V:
token1
token2
...
token999
```

Complexity:

```
O(n²)
```

With KV cache:

```
K,V stored:

step 1000:

only compute:

q1000 × cached(K,V)
```

per token:

```
O(n)
```

PagedAttention solves the memory side:

```
GPU memory:

before:

[sequence A KV][sequence B KV][unused gap]


Paged:

block table:

seq A -> block 1,5,9
seq B -> block 2,3,8
```

This is why vLLM does not primarily depend on flash-attn. The bigger win is:

* KV cache
* continuous batching
* paged memory management

---

For your RTX 4070 lab, I would use:

```
Python 3.12
PyTorch cu128
SDPA
nano-vLLM experiments
```

Only move to `flash-attn` when benchmarking kernel-level performance.

Your current experiment is actually closer to understanding vLLM internals because you are seeing the raw transformer bottleneck.

References:

* PyTorch scaled dot product attention: [https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html](https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
* FlashAttention: [https://github.com/Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)
* vLLM PagedAttention paper: [https://arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180)
