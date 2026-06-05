---
audio: false
generated: true
image: false
lang: en
layout: post
title: BF16 and FP8 Implementation Resources
translated: false
type: note
---

Question: What open-source repos should I learn from to understand BF16 and FP8 formats deeply?

Answer:

Here's a progression from implementation to internals:

## Tier 1: Start Here (Implementable at nanoGPT Scale)

**1. nanoGPT with BF16**
```python
# Just add this to nanoGPT/train.py
device_type = 'cuda' if 'cuda' in device else 'cpu'
ptdtype = torch.bfloat16 if device_type == 'cuda' else torch.float32

with torch.autocast(device_type=device_type, dtype=ptdtype):
    logits = model(X)
    loss = F.cross_entropy(logits.view(-1, vocab_size), Y.view(-1))
```

Start by running nanoGPT with BF16 enabled. This teaches you:
- How dtypes propagate through the forward/backward pass
- When PyTorch falls back to FP32 (matmul, reductions)
- The memory/speed tradeoff

**2. [torch/ao (torchao)](https://github.com/pytorch/ao)**
The most practical repo for FP8. Clean, readable implementations:
```
- torchao/quantization/float8.py → FP8 quantization logic
- torchao/float8/ → training utilities
```
Read the `float8_tensor.py` for how they implement scale factors and quantization. This is production code at Meta scale.

**3. [NVIDIA/Apex](https://github.com/NVIDIA/apex)**
Older but still gold for understanding mixed precision:
```
- apex/amp/ → Automatic Mixed Precision implementation
- apex/optimizers/ → FusedAdam with loss scaling
```
The loss scaling strategy (dynamic loss scaling) is how you prevent gradient underflow in FP8/BF16.

## Tier 2: Deep Dive (Understand the Math)

**4. [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) + your own BF16 instrumentation**
Modify nanoGPT to log:
```python
# Add to training loop
print(f"Loss: {loss.item()}, dtype: {loss.dtype}")
print(f"Grad norm: {torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)}")
print(f"Weight range: {model.transformer.h[0].attn.c_proj.weight.abs().min():.4f} - {model.transformer.h[0].attn.c_proj.weight.abs().max():.4f}")
```

This shows you **why** BF16 matters — you'll see gradient distributions, scale factors, and overflow patterns.

**5. [pytorch/pytorch](https://github.com/pytorch/pytorch) - the source itself**
```
torch/csrc/cuda/jit_cuda_kernel_launcher.cpp  → BF16 kernel dispatch
aten/src/ATen/native/cuda/blas.cpp            → MatMul with mixed precision
```

Read how `linear()` handles `dtype` conversion internally. When does PyTorch compute in FP32 vs BF16? The answer is in the kernels.

## Tier 3: Inference Optimization (Practical Return)

**6. [vLLM](https://github.com/vLLM-project/vLLM)**
```
vllm/model_executor/ops/fp8.py → FP8 MatMul kernels
vllm/quantization/fp8.py       → Quantization scheduling
```

This shows how to actually **use** FP8 for inference speed. The token-by-token quantization strategy they use is elegant.

**7. [llama.cpp](https://github.com/ggerganov/llama.cpp)**
```
ggml.c → GGUF quantization formats
```

Not about FP8 specifically, but teaches you **quantization principles** that apply to FP8. Build a simple quantizer in C.

## Tier 4: Bleeding Edge (If You Want to Understand Megatron-style Training)

**8. [NVIDIA/Megatron-LM](https://github.com/NVIDIA/Megatron-LM)**
```
megatron/core/tensor_parallel/ → Distributed training with mixed precision
megatron/core/utils.py         → Gradient scaling, loss scaling strategies
```

This is how production LLMs do BF16/FP8 at scale. Complex, but the gradient accumulation + loss scaling patterns are reusable.

## My Recommendation for You

**Start here:**
1. Run nanoGPT with BF16 enabled (1 hour)
2. Add instrumentation to log weight/grad ranges (2 hours)
3. Read `torchao/float8/float8_tensor.py` to understand quantization (2 hours)
4. Try `torch.float8_e4m3fn` in nanoGPT training on RTX 4070 (fail, debug, learn — 4 hours)

**Then level up:**
5. Understand loss scaling in Apex: why do we scale loss before backward? What happens without it?
6. Read the NVIDIA blog on FP8 training (linked below)
7. Implement a minimal FP8 quantizer from scratch: input → scale → quantize → dequantize → output

**If you go deeper:**
8. Study vLLM's FP8 inference (most useful for production)
9. Read the FP8 RFC in PyTorch issues — Karpathy-level thinking about tradeoffs

## What NOT to Read (Yet)

- Academic papers on FP8 (pointless without code)
- Medium articles (usually wrong)
- Full Megatron-LM until you've implemented BF16 in nanoGPT first

---

**Best learning path for you:** nanoGPT → torchao → vLLM. Each teaches a different layer: training fundamentals → practical dtype handling → inference optimization.

References:

- [torchao: PyTorch native quantization](https://github.com/pytorch/ao)
- [NVIDIA Apex: Mixed Precision Training](https://github.com/NVIDIA/apex)
- [vLLM FP8 Quantization](https://docs.vllm.ai/en/latest/quantization/fp8.html)
- [NVIDIA FP8 Training Blog](https://developer.nvidia.com/blog/fp8-training-comes-to-pytorch-with-torchao/)
