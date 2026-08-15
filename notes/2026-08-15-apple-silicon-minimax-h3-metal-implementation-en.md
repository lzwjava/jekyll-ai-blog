---
audio: false
generated: true
image: false
lang: en
layout: post
title: Apple Silicon MiniMax-H3 Metal Implementation
translated: false
type: note
---

Question: Intro to [`antirez/h3.c`](https://github.com/antirez/h3.c)

Answer:

One important thing first: **this repository is not the old Redis/C projects you may associate with antirez.** It is a **native Apple-Silicon implementation of MiniMax-H3**, using **Metal** to run the model locally. The README describes it as `h3-metal`.

![Image](https://images.openai.com/static-rsc-4/S_qsC2wXm9SqRD0cMSvoUgA61r1rksQ6LnN-U5tPJm2uriAvPJ31obxOtdEbahxSRGhWvS9271lDE4o0hso_uaGdBGVfhv05ErqVoQwPhWkhJk1EJ0K46gG6mWs1JBR7zvrLf1RDFDggvj7JRpNoNXp7zFnClEHSleVq4HI9FKGRZmXIzS7bQhKmyQi0onlq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/kOGw0CkLYCW3BZmZfbuLbvYxV6wrrDIQ0D0EJ-Nat2h7t_ccuuW3PtFefCpjXrHeCi0MhRK1AT4JglQA2BDHnNRaQsp0HSfcjjFnKfPD8lb1RtZX0ZIZ5C4nbZlJibNkIYO1xedV8uT1EntnkfdTBNpbEU8oV_drRL1VJN7IQDp7_KVvphdw9iFQm9PhGQ6_?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/QEaaqYwEIFHqodujJbR6DoJqUO3PSQf3iJ8tyExeVQAwSJyhglUopSbAkCTxud7No5LV5zMmc-susLVuzaGuc9Q7Abae0fP5BY0B2dc3kXC_GDFsU7e6njhaZ8LxjUzklqVsNxFAN4pDA3mTYTrtutrzfCMnPUwNPA_XxvZ_evnLkag0bOo_Qy7oXxNNZxFl?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/n1cDlH2pC-XNZrPtgY6TYRijmVo-z_b7111UbSp5OOGVIpAGrM8slUfBZNqfFcNP8L0xzoGr9HJ5SxE3n25uQFeWyKau3HJ_iFJDPDQXl9j1zxz4Masp3XPDG4-qQGPYtX5SFOB_IkV-vf3WU1eSA47S3ipAyRkP_DzPpfORCl6mE8iWosV_7iPE8zo_d9d-?purpose=fullsize)

### 1. What is it?

Think of the stack as:

```text
MiniMax-H3 checkpoint
        │
        ▼
┌─────────────────────┐
│      h3.c           │
│ C / C++ host code   │
└──────────┬──────────┘
           │
           ▼
      Apple Metal
           │
           ▼
   Apple Silicon GPU
           │
           ▼
     generated video
```

The interesting part is that it is **not simply calling MLX/PyTorch**. The project is implementing the model's computation directly against Apple's GPU stack.

The README says the project is being developed as a sequence of vertical slices:

```text
model metadata
     ↓
Metal block parity
     ↓
prompt encoding
     ↓
video/audio generation
     ↓
first/last-frame conditioning
     ↓
ordered image/video/audio references
     ↓
Metal performance optimization
```

That makes it a pretty interesting repository for someone studying **LLM/video-model inference implementation from scratch**.

---

## 2. The really interesting part: model → Metal

At a high level, a transformer block looks like:

```python
x
│
├── RMSNorm
│
├── Attention
│     ├── Q = x @ Wq
│     ├── K = x @ Wk
│     ├── V = x @ Wv
│     └── softmax(QKᵀ / √d)V
│
├── residual
│
├── RMSNorm
│
├── MLP
│     ├── gate
│     ├── up
│     └── down
│
└── residual
```

Normally you'd let:

```text
PyTorch
   ↓
CUDA / ROCm
   ↓
GPU
```

do this.

`h3.c` is much closer to:

```text
C/C++
   ↓
Metal kernels
   ↓
Apple GPU
```

So the repository is useful because you can inspect the **actual inference machinery**, rather than only looking at a Python model wrapper.

---

## 3. Why the project is interesting

The strongest part IMO isn't merely "run MiniMax-H3 on a Mac."

It's the **systems optimization work**.

For example, it supports **SSD streaming**:

```text
                 SSD
                  │
          load next transformer block
                  │
                  ▼
       ┌─────────────────────┐
       │ Apple unified memory│
       │                     │
       │ Block N             │
       │ Block N+1           │
       └──────────┬──────────┘
                  │
                  ▼
               GPU
```

Instead of keeping all transformer blocks resident in memory, it keeps only a small number of blocks and streams the next one from SSD.

The README reports roughly:

```text
DiT tracked tensor storage

normal BF16:
    ~36.5 GiB

SSD streaming:
    ~2.0 GiB
```

at 512×512 on M5 Max, at the cost of slower execution.

That's a very nice example of a **memory ↔ bandwidth ↔ compute tradeoff**.

---

## 4. They also attack inference compute

There are several interesting techniques.

### Denoising reuse

Normally:

```text
step 1 → DiT
step 2 → DiT
step 3 → DiT
...
step 20 → DiT
```

With reuse:

```text
step 1 → DiT
step 2 → extrapolate
step 3 → DiT
step 4 → extrapolate
...
```

The project exposes:

```bash
--steps 20
--reuse 2
```

and says this turns 20 denoising steps into **11 fresh DiT evaluations**.

Conceptually:

```text
v_t = f(x_t, t)

instead of computing:

v_1
v_2
v_3
v_4
...

you approximate some:

v_{t+1} ≈ function(v_t, v_{t-1})
```

This is basically exploiting the fact that neighboring diffusion/denoising states are correlated.

---

## 5. Layer thinning

It also supports:

```bash
--layers 45
```

instead of all 50 transformer blocks.

So:

```text
50 blocks
██████████████████████████████████████████████████

45 blocks
█████████████████████████████████████████████
```

This is a very crude approximation compared with quantization or distillation, but it is extremely simple:

```text
compute less → finish faster
```

The README reports that the default fast profile uses 45/50 blocks.

---

## 6. Token reduction

Another optimization is:

```bash
--token-reduction
```

The idea is essentially to reduce the amount of spatial-token computation inside the transformer.

If you have:

```text
H × W video representation
        ↓
      tokens
        ↓
    Transformer
```

then reducing tokens changes the quadratic-ish attention / large matrix-operation workload.

This is the kind of optimization that is particularly interesting for video models because:

```text
image:

H × W

video:

T × H × W
```

The temporal dimension makes the token count explode.

---

# 7. Why `h3.c` is especially interesting for you

I'd rank this repository fairly high for **learning inference engineering**.

You've already been looking at:

* DeepSeek MLA
* PyTorch internals
* Inductor
* GPU kernels
* model training
* inference engines
* Apple Silicon

This repo gives you another perspective:

```text
                    Model
                      │
          ┌───────────┴───────────┐
          │                       │
       PyTorch                  h3.c
          │                       │
       CUDA/ROCm                Metal
          │                       │
       NVIDIA/AMD             Apple GPU
```

You can learn the same mathematical model from two very different systems perspectives.

---

# 8. The best way to read the repo

Don't start by reading every C file.

I'd do:

```bash
git clone https://github.com/antirez/h3.c
cd h3.c

find . -maxdepth 2 -type f | sort
```

Then:

```bash
grep -R "attention" -n .
grep -R "matmul" -n .
grep -R "rmsnorm" -n .
grep -R "softmax" -n .
grep -R "transformer" -n .
grep -R "Metal" -n .
```

The key learning path should be:

```text
CLI
 ↓
model loading
 ↓
tensor representation
 ↓
weight mapping
 ↓
prompt encoding
 ↓
transformer block
 ↓
attention
 ↓
MLP
 ↓
Metal kernel
 ↓
GPU execution
 ↓
denoising loop
 ↓
VAE decode
 ↓
video encoding
```

**That path is much more educational than just trying to run it.**

---

## 9. One particularly useful experiment

If you want to understand it deeply, take one operation and trace it end-to-end.

For example:

```text
Linear:

Y = XW
```

Follow:

```text
MiniMax-H3 weight
      ↓
BF16 tensor
      ↓
C representation
      ↓
Metal buffer
      ↓
Metal kernel
      ↓
Apple GPU
      ↓
output tensor
```

Then do the same for:

```text
RMSNorm
attention
RoPE
MLP / FC
residual
```

That's essentially learning how a real inference runtime is constructed.

---

## 10. Performance philosophy

The project is basically doing:

```text
                    inference cost
                         │
       ┌─────────────────┼──────────────────┐
       ▼                 ▼                  ▼
    compute            memory            bandwidth
       │                 │                  │
   fewer layers      SSD streaming      smaller tensors
   fewer steps       fewer resident      token reduction
   reuse             weights
       │                 │                  │
       └─────────────────┴──────────────────┘
                         │
                         ▼
                    faster inference
```

And importantly, these optimizations aren't free.

For example:

```text
less compute
    ↓
possibly lower quality

less memory
    ↓
more SSD traffic
    ↓
slower inference
```

That's the real lesson of the project.

---

### Bottom line

**`h3.c` is a small but unusually valuable inference-engineering project.**

It's interesting because it sits at the intersection of:

```text
MiniMax-H3
   +
Transformer inference
   +
Diffusion/video generation
   +
C/C++
   +
Metal
   +
Apple Silicon
   +
memory optimization
   +
GPU optimization
```

If your goal is to understand **"how does a giant neural network actually become executable GPU code?"**, this is probably much more educational than another Python inference wrapper.

[antirez/h3.c on GitHub](https://github.com/antirez/h3.c?utm_source=chatgpt.com)

References:

* [Repository README](https://github.com/antirez/h3.c/blob/main/README.md?utm_source=chatgpt.com)
* [MiniMax AI](https://www.minimaxi.com/?utm_source=chatgpt.com)
