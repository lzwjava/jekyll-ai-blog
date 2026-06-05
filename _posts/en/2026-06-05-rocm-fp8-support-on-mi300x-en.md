---
audio: false
generated: true
image: false
lang: en
layout: post
title: ROCm FP8 Support on MI300X
translated: false
type: note
---

Now I have the full picture. Here's the answer:

---

ROCm's FP8 support is actually quite mature on MI300X (CDNA3) — it's one of AMD's strongest selling points for that hardware. Here's the code-backed breakdown:

**Hardware: MI300X is a FP8 beast**

From the ROCm docs (mi300.md), MI300X Matrix Cores deliver:

- Matrix FP8: 2614.9 TFLOPS (vs 163.4 TFLOPS FP32 = 16x gain)
- Matrix FP16/BF16: 1307.4 TFLOPS
- Matrix INT8: 2614.9 TFLOPS

Your MI300X on AMD Dev Cloud hits 2.6 PFLOPS on FP8 — that's H100-class.

**Two FP8 formats (different from NVIDIA)**

This is the critical detail most people miss. ROCm supports TWO FP8 variants:

1. FNUZ (used on CDNA3/MI300X):
   - `__hip_fp8_e4m3_fnuz` — expanded range, no infinity, no signed zero, NaN = negative zero
   - `__hip_fp8_e5m2_fnuz`

2. OCP (Open Compute Project, used on CDNA4/MI350X and RDNA4):
   - `__hip_fp8_e4m3` — follows OCP spec
   - `__hip_fp8_e5m2`

These are NOT the same as NVIDIA's FP8 format. The FNUZ variant has expanded range but different NaN/zero semantics. Models quantized for NVIDIA FP8 may need re-quantization.

**ROCm library FP8 support (from precision-support.yaml)**

```
hipBLASLt:     E4M3 ✅  E5M2 ✅   (your GEMM workhorse)
Composable Kernel: E4M3 ✅  E5M2 ✅   (fused kernels)
MIGraphX:      E4M3 ✅  E5M2 ✅   (graph compiler)
Tensile:       E4M3 ✅  E5M2 ✅   (BLAS backend)
hipSPARSELt:   E4M3 ✅  E5M2 ✅   (sparse)
RCCL:          E4M3 ✅  E5M2 ✅   (multi-GPU comms)
rocWMMA:       E4M3 input only  E5M2 input only
MIOpen:        E4M3 ⚠️  E5M2 ⚠️   (partial — conv ops)
```

MIOpen (the cuDNN equivalent) is still partial — meaning FP8 conv operations aren't fully optimized yet. For transformer workloads this doesn't matter since you mostly use GEMM (hipBLASLt), not convolutions.

**PyTorch on ROCm: FP8 is listed as supported**

From pytorch-compatibility.rst, PyTorch on ROCm lists:
- `torch.float8_e4m3fn` — supported
- `torch.float8_e5m2` — supported

And the CHANGELOG confirms: "Added float8 support for the DeepSpeed extension, allowing for decreased memory footprint and increased throughput in training and inference workloads."

FP8 GEMM operations were migrated from rocBLAS to hipBLASLt for better performance.

**The practical path for your MI300X**

```python
# 1. vLLM inference — FP8 out of the box
# The ROCm docs show vLLM with AITER FP8 batched matmul:
VLLM_ROCM_USE_AITER=1
VLLM_ROCM_USE_AITER_FP8BMM=1  # Fused FP8 per-token quant + batched GEMM

# 2. AMD Quark for quantization
pip install quark
from quark.torch.quantization import (
    Config, QuantizationConfig, FP8E4M3PerTensorSpec
)
# Supports FP8 attention, INT4-FP8 two-level scheme (4x compression)

# 3. PyTorch training with torchao
from torchao.float8 import convert_to_float8_training
model = convert_to_float8_training(model)
```

**Key difference from NVIDIA**

On NVIDIA (H100): `torch.float8_e4m3fn` → E4M3 with standard NaN/Inf semantics
On AMD (MI300X): The FNUZ variant is used internally, but PyTorch abstracts this away. The OCP variant is used on CDNA4+ (MI350X).

The practical implication: if you're deploying FP8 models from HuggingFace that were quantized for NVIDIA, you may see slightly different numerical behavior on MI300X due to FNUZ vs standard FP8. AMD's Quark tool handles re-quantization.

**Bottom line for your AMD Dev Cloud MI300X**

ROCm FP8 is production-ready for inference (vLLM, Quark), actively improving for training (torchao/DeepSpeed), and backed by 2.6 PFLOPS of FP8 hardware. The main gap vs NVIDIA is MIOpen (partial) and the FNUZ format difference. For LLM inference specifically — it's solid.

References:

- ROCm precision support reference: /Users/lzwjava/projects/ROCm/docs/reference/precision-support.rst
- MI300X architecture: /Users/lzwjava/projects/ROCm/docs/conceptual/gpu-arch/mi300.md
- PyTorch compatibility: /Users/lzwjava/projects/ROCm/docs/compatibility/ml-compatibility/pytorch-compatibility.rst
- Model quantization (Quark): /Users/lzwjava/projects/ROCm/docs/how-to/rocm-for-ai/inference-optimization/model-quantization.rst
- vLLM optimization: /Users/lzwjava/projects/ROCm/docs/how-to/rocm-for-ai/inference-optimization/vllm-optimization.rst
- CHANGELOG: /Users/lzwjava/projects/ROCm/CHANGELOG.md
