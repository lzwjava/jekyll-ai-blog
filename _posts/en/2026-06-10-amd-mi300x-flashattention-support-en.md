---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD MI300X FlashAttention Support
translated: false
type: note
---

Question: Can AMD MI300X use FlashAttention 1 or 2?

Answer: Yes, the AMD Instinct MI300X supports both FlashAttention-1 and FlashAttention-2 via AMD's ROCm ecosystem. However, for your FP8/BF16 training workload, you should explicitly target **FlashAttention-2**.

### Overview of Support

* **FlashAttention-2 (Recommended):** Fully supported on the MI300X using ROCm 6.0 and above. It provides optimized implementations through two backends: the default Composable Kernel (CK) backend and an alternative OpenAI Triton backend. It natively supports both `fp16` and `bf16` data types.
* **FlashAttention-1:** Historically supported on the MI200 and MI300 series via earlier ROCm ports, but it is considered legacy and lacks the performance enhancements and extended token head dimensions of the newer implementation.

---

### Implementation Details for Your Run

Since you are running training via `nanochat`, you can install and configure FlashAttention-2 via the official repository.

#### 1. Installation

You can build the ROCm-compatible version of FlashAttention-2 directly inside your environment:

```bash
pip install ninja packaging
git clone --recursive https://github.com/dao-ailab/flash-attention.git
cd flash-attention
# Building on ROCm will automatically detect your MI300X target
pip install .

```

#### 2. Switching Backends

Depending on your framework setup, you can experiment with which backend yields the highest Model FLOPs Utilization (MFU) on the MI300X by toggling the environmental flag:

* **To use the Composable Kernel backend (Default):**

```bash
export FLASH_ATTENTION_TRITON_AMD_ENABLE="FALSE"

```

* **To use the OpenAI Triton backend:**

```bash
export FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"

```

References:

* [Dao-AILab/flash-attention GitHub Repository](https://github.com/dao-ailab/flash-attention)
* [ROCm Model Acceleration Libraries Documentation](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference-optimization/model-acceleration-libraries.html)
