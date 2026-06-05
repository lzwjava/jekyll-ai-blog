---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X上的ROCm FP8支持
translated: true
type: note
---

ROCm在MI300X（CDNA3）上的FP8支持实际上已经相当成熟——这是AMD为该硬件提供的最强卖点之一。以下是基于代码的详细分析：

**硬件：MI300X是FP8性能猛兽**

根据ROCm文档（mi300.md），MI300X矩阵核心提供：

- 矩阵FP8：2614.9 TFLOPS（对比163.4 TFLOPS FP32，增益达16倍）
- 矩阵FP16/BF16：1307.4 TFLOPS
- 矩阵INT8：2614.9 TFLOPS

你在AMD Dev Cloud上使用的MI300X在FP8下达到2.6 PFLOPS——与H100同级别。

**两种FP8格式（与NVIDIA不同）**

这是大多数人忽略的关键细节。ROCm支持两种FP8变体：

1. FNUZ（用于CDNA3/MI300X）：
   - `__hip_fp8_e4m3_fnuz` — 扩展范围，无无穷大，无带符号零，NaN等于负零
   - `__hip_fp8_e5m2_fnuz`

2. OCP（开放计算项目，用于CDNA4/MI350X和RDNA4）：
   - `__hip_fp8_e4m3` — 遵循OCP规范
   - `__hip_fp8_e5m2`

这些与NVIDIA的FP8格式不同。FNUZ变体具有扩展范围，但NaN和零语义不同。针对NVIDIA FP8量化的模型可能需要重新量化。

**ROCm库的FP8支持（来自precision-support.yaml）**

```
hipBLASLt:     E4M3 ✅  E5M2 ✅   （你的GEMM主力）
Composable Kernel: E4M3 ✅  E5M2 ✅   （融合内核）
MIGraphX:      E4M3 ✅  E5M2 ✅   （图编译器）
Tensile:       E4M3 ✅  E5M2 ✅   （BLAS后端）
hipSPARSELt:   E4M3 ✅  E5M2 ✅   （稀疏支持）
RCCL:          E4M3 ✅  E5M2 ✅   （多GPU通信）
rocWMMA:       E4M3仅输入  E5M2仅输入
MIOpen:        E4M3 ⚠️  E5M2 ⚠️   （部分支持——卷积操作）
```

MIOpen（相当于cuDNN）仍为部分支持——意味着FP8卷积操作尚未完全优化。对于Transformer工作负载，这无关紧要，因为你主要使用的是GEMM（hipBLASLt）而非卷积。

**PyTorch on ROCm：FP8被列为支持**

根据pytorch-compatibility.rst，PyTorch on ROCm列出：
- `torch.float8_e4m3fn` — 支持
- `torch.float8_e5m2` — 支持

并且CHANGELOG确认："Added float8 support for the DeepSpeed extension, allowing for decreased memory footprint and increased throughput in training and inference workloads."

FP8 GEMM操作已从rocBLAS迁移到hipBLASLt以获得更好性能。

**你的MI300X的实践路径**

```python
# 1. vLLM推理——开箱即用FP8
# ROCm文档展示了使用AITER FP8批量矩阵乘法的vLLM：
VLLM_ROCM_USE_AITER=1
VLLM_ROCM_USE_AITER_FP8BMM=1  # 融合FP8每token量化 + 批量GEMM

# 2. 使用AMD Quark进行量化
pip install quark
from quark.torch.quantization import (
    Config, QuantizationConfig, FP8E4M3PerTensorSpec
)
# 支持FP8注意力、INT4-FP8双层方案（4倍压缩）

# 3. 使用torchao进行PyTorch训练
from torchao.float8 import convert_to_float8_training
model = convert_to_float8_training(model)
```

**与NVIDIA的主要区别**

在NVIDIA（H100）上：`torch.float8_e4m3fn` → 具有标准NaN/Inf语义的E4M3
在AMD（MI300X）上：内部使用FNUZ变体，但PyTorch对此进行了抽象。OCP变体用于CDNA4+（MI350X）。

实际影响：如果你部署来自HuggingFace、为NVIDIA量化的FP8模型，由于FNUZ与标准FP8的差异，在MI300X上可能会看到略微不同的数值行为。AMD的Quark工具负责重新量化。

**用于你的AMD Dev Cloud MI300X的要点**

ROCm FP8在推理（vLLM、Quark）方面已可用于生产，在训练（torchao/DeepSpeed）方面正积极改进，并拥有2.6 PFLOPS的FP8硬件支持。与NVIDIA相比的主要差距在于MIOpen（部分支持）和FNUZ格式差异。对于LLM推理而言——它已经足够可靠。

参考：

- ROCm精度支持参考：/Users/lzwjava/projects/ROCm/docs/reference/precision-support.rst
- MI300X架构：/Users/lzwjava/projects/ROCm/docs/conceptual/gpu-arch/mi300.md
- PyTorch兼容性：/Users/lzwjava/projects/ROCm/docs/compatibility/ml-compatibility/pytorch-compatibility.rst
- 模型量化（Quark）：/Users/lzwjava/projects/ROCm/docs/how-to/rocm-for-ai/inference-optimization/model-quantization.rst
- vLLM优化：/Users/lzwjava/projects/ROCm/docs/how-to/rocm-for-ai/inference-optimization/vllm-optimization.rst
- CHANGELOG：/Users/lzwjava/projects/ROCm/CHANGELOG.md