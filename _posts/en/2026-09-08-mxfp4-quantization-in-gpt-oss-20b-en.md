---
audio: false
generated: true
image: false
lang: en
layout: post
title: MXFP4 Quantization in GPT-OSS-20B
translated: false
type: note
---

Question: **What does MXFP4 mean in GPT-OSS-20B?**

Answer: **MXFP4 is the native 4-bit floating-point quantization format used for GPT-OSS's MoE weights.**

Break the name down:

* **M** = Microscaling / block-scaled format
* **XF** = Microsoft's **MX** microscaling family
* **P4** = **4-bit floating-point** values

The important part is that **it is not simply “FP4 everywhere.”** MXFP4 uses:

```text
                 MXFP4 tensor
                      │
          ┌───────────┴───────────┐
          │                       │
     FP4 values              block scale
     4 bits each              shared scale
          │                       │
          └───────────┬───────────┘
                      ↓
             actual FP value
```

For GPT-OSS-20B, OpenAI quantizes the **MoE linear projection weights** to MXFP4. The other major tensors—attention, embeddings, etc.—remain **BF16**. ([GitHub][1])

### Why block scaling?

Suppose you have 32 weights:

```text
W = [0.02, -0.7, 1.2, -2.8, ...]
```

Representing each number directly with only 4 bits gives terrible dynamic range.

Instead, MXFP4 does approximately:

```text
                 shared scale
                     ↓
W[0:32] ────────> [FP4, FP4, FP4, ... FP4]
```

Each small block shares a scale factor.

Conceptually:

```python
# simplified, NOT the actual implementation

scale = max(abs(W_block)) / FP4_MAX

q = round(W_block / scale)
q = clamp(q, FP4_MIN, FP4_MAX)

# store:
#   q     -> 4-bit values
#   scale -> block scale
```

During the GEMM, the kernel effectively reconstructs:

```text
W ≈ FP4_values × block_scale
```

This is why you can get much better numerical behavior than naive 4-bit quantization.

### Why is it called 4.25 bits?

This is a particularly important detail for GPT-OSS.

OpenAI reports MXFP4 as **4.25 bits per parameter**, not exactly 4 bits, because you also have to store the block scales. ([OpenAI Deployment Safety Hub][2])

For GPT-OSS:

```text
FP4 value        = 4 bits
scale overhead   ≈ 0.25 bits / parameter
────────────────────────────────────
effective         ≈ 4.25 bits / parameter
```

So 20.9B parameters don't require:

```text
20.9B × 4 bits
```

exactly. The scale metadata adds some overhead.

That's why the published GPT-OSS-20B checkpoint is around **12.8 GiB**, rather than ~10.5 GB. ([OpenAI Deployment Safety Hub][2])

### And this is especially useful for MoE

GPT-OSS-20B actually has:

```text
total parameters:       20.91B
active parameters:       3.61B
experts:                    32
experts selected/token:     4
```

So for each token, the router activates only 4 experts, but **the expert weights still need to exist in memory**. ([OpenAI CDN][3])

MXFP4 makes those huge expert matrices much smaller.

The architecture is roughly:

```text
                    token
                      │
                      ▼
                   Router
                      │
              select 4 / 32 experts
                 ┌────┼────┐
                 ▼    ▼    ▼
               E7    E13   E27 ...
                │     │     │
                │ MXFP4     │
                ▼     ▼     ▼
                 └────┼─────┘
                      │
                      ▼
                    output
```

This is why **GPT-OSS-20B can run in ~16 GB memory**, despite having ~21B total parameters. OpenAI specifically says the MoE weights are over 90% of the parameter count and are quantized to MXFP4. ([OpenAI Deployment Safety Hub][2])

### The interesting GPU/kernel part

This connects directly to the Triton questions you've been asking.

The model doesn't necessarily do:

```text
MXFP4 → BF16
       ↓
    BF16 GEMM
```

That would throw away much of the memory-bandwidth advantage.

Instead, specialized **MXFP4 GEMM kernels** can consume the packed FP4 weights + scales directly.

OpenAI stores the tensor roughly as:

```text
tensor.blocks
    ↓
packed FP4 values
(two FP4 values / uint8)

tensor.scales
    ↓
block scaling factors
```

and the MXFP4-aware kernels operate on this representation. ([GitHub][1])

So the stack you're looking at is roughly:

```text
GPT-OSS-20B
     │
     ├── Attention ───────── BF16
     │
     ├── Embeddings ──────── BF16
     │
     └── MoE
          │
          ├── Router ─────── BF16
          │
          └── Experts
                │
                └── MXFP4
                     │
                     ├── packed FP4
                     ├── block scales
                     │
                     ▼
               MXFP4 Triton/CUDA kernel
                     │
                     ▼
                    GEMM
```

**In one sentence:** MXFP4 is a **block-scaled FP4 representation** that lets GPT-OSS store its enormous MoE expert weights at roughly **4.25 bits/parameter**, while retaining much better numerical range than naive FP4.

References:

* [OpenAI GPT-OSS model card](https://deploymentsafety.openai.com/gpt-oss/tacit-knowledge-and-troubleshooting?utm_source=chatgpt.com)
* [OpenAI GPT-OSS GitHub README](https://github.com/openai/gpt-oss/blob/main/README.md?utm_source=chatgpt.com)
* [Hugging Face MXFP4 documentation](https://huggingface.co/docs/transformers/quantization/mxfp4?utm_source=chatgpt.com)

I can also walk through the **actual 32-element MXFP4 encoding (E2M1 + E8M0 scale) and how a Triton kernel turns it into a matrix multiply**, which is the interesting low-level part.

[1]: https://github.com/openai/gpt-oss/blob/main/README.md?utm_source=chatgpt.com "gpt-oss/README.md at main · openai/gpt-oss · GitHub"
[2]: https://deploymentsafety.openai.com/gpt-oss/tacit-knowledge-and-troubleshooting?utm_source=chatgpt.com "gpt-oss-120b & gpt-oss-20b Model Card - OpenAI Deployment Safety Hub"
[3]: https://cdn.openai.com/pdf/419b6906-9da6-406c-a19d-1bb078ac7637/oai_gpt-oss_model_card.pdf?utm_source=chatgpt.com "forward pass), and gpt-oss-20b with 24 layers (20.9B total and 3.6B active parameters). Table 1 shows a full breakdown of the parameter counts."
