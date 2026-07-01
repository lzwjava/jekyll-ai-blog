---
audio: false
generated: true
image: false
lang: en
layout: post
title: BF16 Format in Large Language Models
translated: false
type: note
---

**Question:** What is BF16, and how is it used in LLMs?

**Answer:**

## BF16 from First Principles

### Bit Layout

Float formats are defined by three fields: sign, exponent, mantissa.

```
FP32:  [1 sign][8 exponent][23 mantissa] = 32 bits
FP16:  [1 sign][5 exponent][10 mantissa] = 16 bits
BF16:  [1 sign][8 exponent][7 mantissa]  = 16 bits  ← same exp as FP32
```

BF16 = "Brain Float 16", developed at Google Brain. The key insight: **keep FP32's exponent range, truncate mantissa**.

```python
import struct

def fp32_bits(x):
    return struct.pack('f', x).hex()

def show_format(x):
    b = struct.unpack('I', struct.pack('f', x))[0]
    sign     = (b >> 31) & 0x1
    exponent = (b >> 23) & 0xFF
    mantissa = b & 0x7FFFFF
    print(f"FP32  {x}: sign={sign} exp={exponent:08b}({exponent-127:+d}) mantissa={mantissa:023b}")
    # BF16 is just the top 16 bits of FP32
    bf16_mantissa = mantissa >> 16  # keep only top 7 bits
    print(f"BF16  {x}: sign={sign} exp={exponent:08b}({exponent-127:+d}) mantissa={bf16_mantissa:07b}")

show_format(3.14)
show_format(0.0001)
show_format(65504.0)  # FP16 max
show_format(3.4e38)   # near FP32 max — BF16 handles this, FP16 overflows
```

### Dynamic Range Comparison

| Format | Exp bits | Max value | Min normal | Precision (decimal digits) |
|--------|----------|-----------|------------|---------------------------|
| FP32   | 8        | ~3.4e38   | ~1.2e-38   | ~7.2                      |
| FP16   | 5        | 65504     | ~6.1e-5    | ~3.3                      |
| BF16   | 8        | ~3.4e38   | ~1.2e-38   | ~2.3                      |

**BF16 has the same range as FP32, but only ~2 decimal digits of precision.** FP16 has better precision but catastrophically small range — gradients and weights easily overflow to `inf` or underflow to 0.

---

## Why This Matters for LLMs

### 1. Training Stability

The classic training problem with FP16:

```
gradient = 1e-6   # small but valid
FP16 min normal ≈ 6e-5
→ gradient underflows to 0 → vanishing gradients → training diverges
```

BF16 handles this because exponent range = FP32:

```
BF16 min normal ≈ 1.2e-38  ← gradient 1e-6 is totally fine
```

This is why BF16 training usually needs **no loss scaling** (unlike FP16 which requires `GradScaler`).

```python
# FP16 training — needs loss scaling
scaler = torch.cuda.amp.GradScaler()
with torch.autocast(device_type='cuda', dtype=torch.float16):
    loss = model(x)
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()

# BF16 training — simpler, no scaler needed
with torch.autocast(device_type='cuda', dtype=torch.bfloat16):
    loss = model(x)
loss.backward()
optimizer.step()
```

### 2. Memory Savings

```
FP32 7B param model: 7e9 * 4 bytes = 28 GB
BF16 7B param model: 7e9 * 2 bytes = 14 GB  ← fits on 2x A100 40GB instead of 4x
```

During training you still have optimizer states (Adam: 2x FP32 copies of params = another 28 GB), but **mixed precision** keeps weights in BF16 for forward/backward and FP32 master copy for optimizer update.

### 3. Hardware Acceleration

Modern GPUs have native BF16 tensor cores:

| GPU | BF16 TFLOPS | FP32 TFLOPS | Speedup |
| ----- | ------------- | ------------- | --------- |
| A100 80GB | 312 | 19.5 | 16x |
| H100 SXM | 989 | 67 | ~15x |
| RTX 4090 | 165 | 82.6 | 2x |

A100/H100 have massive BF16 acceleration. This is the primary reason BF16 is standard for LLM training — you get free 10-16x throughput improvement over FP32.

---

## Mixed Precision Training: The Full Picture

```
┌─────────────────────────────────────────────────────────┐
│  FORWARD PASS                                           │
│  weights (BF16) → activations (BF16)                   │
│                           ↓                            │
│  LOSS (FP32 accumulation in matmul outputs)            │
│                           ↓                            │
│  BACKWARD PASS                                         │
│  gradients computed in BF16                            │
│                           ↓                            │
│  OPTIMIZER STEP                                        │
│  FP32 master weights ← BF16 gradients cast to FP32     │
│  Adam m, v stored in FP32                              │
│  updated FP32 weights → cast back to BF16              │
└─────────────────────────────────────────────────────────┘
```

Implemented in nanoGPT-style:

```python
import torch
import torch.nn as nn

model = GPT(config).cuda()

# Optimizer on FP32 master weights happens automatically
# when you use AMP — PyTorch handles the master copy internally
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)

# torch.compile + BF16 = maximum throughput on A100/H100
model = torch.compile(model)

ctx = torch.autocast(device_type='cuda', dtype=torch.bfloat16)

for x, y in dataloader:
    with ctx:
        logits, loss = model(x, y)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
    optimizer.zero_grad(set_to_none=True)
```

This is literally what Karpathy uses in nanoGPT — `dtype=torch.bfloat16` + A100.

---

## Inference: Quantization Beyond BF16

At inference time, you go even further:

```
Training:   BF16 weights + BF16 activations (mixed with FP32 accumulators)
Inference:  INT8 / INT4 weights + BF16 activations (GPTQ, AWQ, bitsandbytes)
```

```python
# bitsandbytes 4-bit inference
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,  # activations in BF16
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"               # NormalFloat4
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B",
    quantization_config=bnb_config,
    device_map="auto"
)
```

Weights stored in INT4 (~3.5 GB for 7B), dequantized to BF16 on-the-fly for matmuls.

---

## BF16 vs FP16: When to Use Which

| Scenario | Recommendation |
| ---------- | --------------- |
| Training on A100/H100 | **BF16** — always |
| Training on older GPUs (V100) | FP16 + GradScaler (V100 has no BF16 tensor cores) |
| Inference on consumer GPU | BF16 if supported, else FP16 |
| Apple Silicon (MPS) | BF16 supported on M2+ |
| TPUs | BF16 natively (Google designed it for TPUs) |

Check support:

```python
print(torch.cuda.is_bf16_supported())  # True on A100, H100, RTX 30xx+
```

---

## The Precision Loss in Practice

BF16 has only 7 mantissa bits → resolution of ~0.8% between adjacent representable values. Does this hurt?

Empirically: **no, for LLM weights**. Neural network weights are robust to this level of noise — it's essentially free regularization. The loss curves for BF16 vs FP32 training are indistinguishable past ~1B params.

Where it *can* hurt: operations requiring high numerical precision — softmax (exponentials of large numbers), layer norm, loss computation. These are kept in FP32 internally in the matmul accumulators even during BF16 autocast.

---

## Summary

```
BF16 = FP32's exponent + 7-bit mantissa
     = same range, less precision
     = no overflow/underflow problems that plagued FP16
     = 2x memory savings over FP32
     = 10-16x throughput on A100/H100 tensor cores
     = the standard for modern LLM training
```

If you're training on H100s (which you are), BF16 + `torch.compile` is the default stack — no GradScaler, no loss spikes from overflow, maximum FLOP utilization.
