---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek V4 Differences from nanoGPT
translated: false
type: note
---

Question: In the DeepSeek V4 official inference code, what are `scale_fmt`, `n_routed_experts`, and the `ue8m0` format — things that differ from nanoGPT?

Answer:

Good instinct to study the official inference code directly. Let me break down each one from first principles.

---

## `n_routed_experts` — MoE Routing

nanoGPT has a single dense FFN per layer:

```python
# nanoGPT FFN — every token goes through the same weights
x = self.c_fc(x)    # [B, T, 4*n_embd]
x = self.gelu(x)
x = self.c_proj(x)  # [B, T, n_embd]
```

DeepSeek V4 replaces this with a **Mixture of Experts** FFN:

```python
# MoE: N experts exist, but only top-K are activated per token
n_routed_experts = 256   # total expert count
n_activated_experts = 8  # top-K selected per token (sparse activation)
```

The router is a small linear layer that scores all 256 experts and picks 8:

```python
# Simplified MoE forward
router_logits = x @ router_weight.T        # [B*T, n_routed_experts]
topk_ids = router_logits.topk(k=8).indices # select 8 experts
output = sum(expert[i](x) for i in topk_ids)  # only 8 FFNs fire
```

**Why it matters:** 256 experts × FFN params = massive total parameter count, but only 8 activate per token → compute stays tractable. DeepSeek-V3/V4 has ~671B total params but ~37B active per forward pass. That's the MoE tradeoff.

There are also **shared experts** (always active, like a dense residual) + routed experts. DeepSeek calls this **DeepSeekMoE** architecture.

---

## `scale_fmt` — Quantization Scale Format

This is about **how you store the scaling factors** for quantized weights.

When you quantize a weight matrix (say FP16 → INT8), you need a scale per block:

```
W_quantized = round(W / scale)
W_reconstructed = W_quantized * scale
```

`scale_fmt` specifies the **dtype of that scale tensor**. In DeepSeek V4's inference code you'll see options like:

```python
scale_fmt = "e4m3"   # FP8 scale
scale_fmt = "e5m2"   # FP8 scale (different range/precision)
scale_fmt = "fp16"   # half-precision scale
```

This matters for **FP8 quantization** — DeepSeek V3/V4 trains and infers in FP8 natively (a major engineering contribution). The scale format controls the precision of the dequantization step.

---

## `ue8m0` — Unsigned Exponent-8, Mantissa-0

This is a **non-standard float format** and the most exotic of the three.

Standard float anatomy: `sign | exponent | mantissa`

| Format | Sign | Exponent | Mantissa | Range |
|--------|------|----------|----------|-------|
| FP32 | 1 | 8 | 23 | ~1e-38 to 3e38 |
| FP16 | 1 | 5 | 10 | ~6e-5 to 65504 |
| E4M3 (FP8) | 1 | 4 | 3 | ~1e-9 to 448 |
| **UE8M0** | **0** | **8** | **0** | powers of 2 only |

`ue8m0` can **only represent powers of 2**: `2^-127` through `2^128`. No fractional mantissa, no sign.

**Why use it for scales?** Quantization scales are almost always powers of 2 in practice (you round to the nearest power of 2 anyway for hardware efficiency). Storing them as `ue8m0` means:

- Dequantization becomes a **bit shift** instead of a multiply — extremely fast on hardware
- 8 bits per scale instead of 16 (FP16) → half the memory for scale tensors
- Perfect fit for block-wise FP8 quantization at scale

This is the **MXFP8 / microscaling format** that's becoming standard for frontier model inference. NVIDIA H100, AMD MI300X both support it at the hardware level.

---

## How They Connect

```
DeepSeek V4 inference pipeline:

Token → Attention (MLA, also unique) → MoE FFN
                                           ↓
                              Router scores 256 experts (n_routed_experts)
                                           ↓
                              Top-8 experts fire (sparse, cheap)
                                           ↓
                              Each expert weight is FP8 quantized
                              Scale stored as ue8m0 (power-of-2, 8-bit)
                              scale_fmt controls this dtype
```

---

## What to Look for in the Hermes Analysis

When you run it through Hermes, focus on:

1. **`MoEGate` / router module** — how aux loss (load balancing) is computed
2. **`fp8_gemm` calls** — where `scale_fmt` and `ue8m0` actually get used in matmul
3. **`shared_experts` vs `routed_experts`** — DeepSeek's hybrid dense+sparse design
4. **`ep_size` (expert parallelism)** — how experts are sharded across GPUs

The official inference code is the clearest documentation of how MXFP8 + MoE actually works in production. Better than any paper.

References:

- [DeepSeek-V4-Pro inference code](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/tree/main/inference)
- [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437)
- [MXFP8 / Microscaling Formats — OCP Spec](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf)