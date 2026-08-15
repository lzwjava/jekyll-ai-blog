---
audio: false
generated: true
image: false
lang: en
layout: post
title: Huawei Ascend 950PR Overview
translated: false
type: note
---

## Question: intro to Ascend 950PR 9579

I assume you mean **Huawei Ascend 950PR** (昇腾 950PR). "9579" may be a typo or internal reference. Ascend 950PR is Huawei's next-generation AI accelerator, mainly designed for **LLM inference prefill** and **recommendation workloads**. ([Huawei][1])

![Image](https://images.openai.com/static-rsc-4/7IxRtIPq_rWrZesWOWPhZiU5N7xg9u1XkXTabRCwpJMFZzctsMUaRMJObkaijvmPxlTHk_UPPwkzLHkGm2FJPjzavprBHOMCCM9MYJdYyc92P7pGZwbioJb2KTyKY3khATvjmCCBx3WkKZKNzRKGMPuYK_3xmVeAOdOxIigzml0ja6Ssq1oKeqCE8lOEEoi2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/lLCXeST-jpDRBNRm8Owmoj8iecEpEdYP_DVS815KV14afMUU-B4AfRVux7PzIhpMTgBlAwL45ecR-iShK22qySLhDfF4eZsKV2A_cZX7QefCfPgFhuWVX-Iki79_QeKJil2978hBTvnRnR2zgGcypbk5EswofHqtNBdcOJST4epk9vMINfJEkKy0sPeuHM41?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/PiNDAPc67VuEh_qkeUkxKnzfMU7t6Y3-zgrlpp95Ib1G8MgE5Mo10DsgKznNU4d_rEHJ5JwodJ_AYxzjgfEWgfKvNRrQ0KnNGj0nj6lt2JUK63aKCjipdEQM19Nxle_iLXDqKVsQEh1We7XgI2XI3m9yzuzW24W4U4V9Rt16TjIcn5RUYyrCntmdN2R3F6Go?purpose=fullsize)

## 1. Position in Huawei Ascend roadmap

Huawei Ascend roadmap:

```
Ascend 310  (edge AI)
      |
Ascend 910 / 910B / 910C  (training + inference)
      |
Ascend 950 series  (2026)
      |
      +-- Ascend 950PR  -> Prefill + Recommendation
      |
      +-- Ascend 950DT  -> Decode + Training
      |
Ascend 960 (2027)
      |
Ascend 970 (2028)
```

The 950PR and 950DT share the same Ascend 950 die, but package different memory systems for different workloads. ([Huawei][1])

---

# 2. Why split PR and DT?

Huawei is targeting the new LLM serving architecture:

```
User prompt
     |
     v
+------------+
|  Prefill   |  <- compute heavy
+------------+
     |
     v
+------------+
|  Decode    |  <- memory bandwidth heavy
+------------+
     |
     v
Tokens
```

Example:

```
Input:
"Explain transformer architecture..."

Prefill:
process all 1000 input tokens
       |
       v
KV cache created

Decode:
generate:
"The transformer..."
"architecture..."
"is..."
```

Different bottlenecks:

| Stage    | Bottleneck                  |
| -------- | --------------------------- |
| Prefill  | Tensor compute              |
| Decode   | Memory bandwidth + KV cache |
| Training | Both                        |

So:

```
950PR
   |
   +-- Prefill
   +-- Recommendation
   +-- High throughput inference


950DT
   |
   +-- Decode
   +-- Training
```

([Huawei][1])

---

# 3. Main specifications

According to Huawei:

## Compute

Low precision AI formats:

```
FP8
MXFP8
MXFP4
HiF8
```

Peak:

```
FP8:
~1 PFLOPS

MXFP4:
~2 PFLOPS
```

([Huawei][2])

Comparison:

```
                     FP8 AI compute

NVIDIA H100       ~1 PFLOPS
NVIDIA H200       ~1 PFLOPS+
Ascend 950PR      ~1 PFLOPS
```

(The exact comparison depends heavily on workload and software stack.)

---

# 4. Memory system

950PR uses:

```
Ascend 950 die
        |
        |
     HiBL 1.0
        |
        |
      HBM
```

Huawei designed it with cheaper HBM for prefill.

Reported targets:

```
Memory:
~128GB class

Bandwidth:
~1.4-1.6 TB/s
```

([Investing.com][3])

Why less bandwidth than 950DT?

Because prefill is:

```
Large matrix multiplication

Q,K,V projection:

X @ Wq
X @ Wk
X @ Wv
```

Mostly compute-bound.

Decode is:

```
single token generation

small GEMM
+
KV cache lookup

memory bandwidth dominates
```

---

# 5. Interconnect

Large AI clusters need accelerator-to-accelerator communication.

950 series:

```
Interconnect:
2 TB/s
```

Huawei uses its own interconnect technology rather than NVIDIA NVLink. ([Huawei][1])

For comparison:

```
NVIDIA H100 NVLink:
~900 GB/s

H200:
~900 GB/s

B200:
multi-TB/s class
```

---

# 6. Software stack

Hardware is only half of AI acceleration.

NVIDIA:

```
CUDA
 |
cuBLAS
 |
TensorRT
 |
PyTorch
```

Huawei:

```
CANN
 |
Ascend operators
 |
MindSpore / PyTorch Ascend
 |
LLM frameworks
```

([Huawei][2])

The biggest challenge is not FLOPS.

It is:

```
CUDA ecosystem
        vs
CANN ecosystem
```

For example:

A CUDA kernel:

```python
torch.matmul(q, k.transpose(-1,-2))
```

on NVIDIA:

```
PyTorch
 |
CUDA kernel
 |
Tensor Core
```

On Ascend:

```
PyTorch
 |
torch_npu
 |
CANN
 |
Ascend Cube Engine
```

Software maturity matters enormously.

---

# 7. Expected use cases

## LLM serving

Example:

```
Qwen
DeepSeek
Llama
```

Deployment:

```
User requests
       |
       |
Load balancer
       |
       |
Ascend 950PR cluster
       |
       |
Prefill
       |
       |
950DT cluster
       |
       |
Decode
```

---

## Recommendation systems

Companies like:

* ecommerce
* short video
* ads

need:

```
embedding
+
ranking model
+
large-scale inference
```

950PR targets this.

---

# 8. How it compares to NVIDIA?

A simplified view:

|          | Ascend 950PR               | NVIDIA H100/H200     |
| -------- | -------------------------- | -------------------- |
| Vendor   | Huawei                     | NVIDIA               |
| Target   | Inference                  | Training + inference |
| Strength | Cost/performance inference | Ecosystem            |
| Software | CANN                       | CUDA                 |
| Memory   | HiBL HBM                   | HBM3/HBM3e           |
| Cluster  | SuperPod                   | NVLink/NVSwitch      |

---

# 9. Strategic importance

Ascend 950PR is less about beating NVIDIA RTX/H100 directly.

It is about:

```
China AI infrastructure independence

CPU:
Kunpeng

Accelerator:
Ascend

Framework:
MindSpore

Cloud:
Huawei Cloud
```

Huawei is building a full-stack alternative AI ecosystem. ([Huawei][2])

---

## For an LLM engineer perspective

The interesting part is not the chip itself.

The important question is:

```
Can Ascend run:

DeepSeek-V3
Qwen3
Llama 4
Mixture-of-Experts models

efficiently?

```

The winning platform will likely be:

```
hardware
+
compiler
+
distributed runtime
+
model optimization
```

not only TOPS/FLOPS.

References:

* Huawei Ascend roadmap and specifications ([Huawei][1])
* Huawei official Ascend 950 architecture overview ([Huawei][2])
* Reuters overview of Huawei AI chip roadmap ([reuters.com][4])

[1]: https://www.huawei.com/en/news/2025/9/hc-xu-keynote-speech?utm_source=chatgpt.com "Groundbreaking SuperPoD Interconnect: Leading a New Paradigm for AI Infrastructure - Huawei"
[2]: https://www.huawei.com/cn/news/2025/9/hc-xu-keynote-speech?utm_source=chatgpt.com "以开创的超节点互联技术，引领AI基础设施新范式"
[3]: https://www.investing.com/news/stock-market-news/factboxkey-products-in-huaweis-ai-chips-and-computing-power-roadmap-4244325?utm_source=chatgpt.com "Factbox-Key products in Huawei’s AI chips and computing power roadmap By Reuters"
[4]: https://www.reuters.com/world/china/key-products-huaweis-ai-chips-computing-power-roadmap-2025-09-18/?utm_source=chatgpt.com "Key products in Huawei's AI chips and computing power roadmap"
