---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA 对 Tesla P100 的支持
translated: true
type: note
---

问题：NVIDIA Tesla P100支持哪个CUDA版本？

答案：

**Tesla P100采用Pascal架构，计算能力为6.0（`sm_60`）**。（[NVIDIA Developer][1]）

重要区别在于：

| 项目                          | P100          |
| ----------------------------- | ------------- |
| 架构                          | Pascal        |
| 计算能力                      | **6.0**       |
| 首个CUDA工具包                | CUDA **8.0**  |
| 支持P100的最新工具包          | **CUDA 12.x** |
| `nvcc`目标                    | `sm_60`       |
| PTX目标                       | `compute_60`  |

NVIDIA当前的兼容性矩阵将Pascal（`6.0/6.1`）列为通过**CUDA 12.x**支持的架构。（[NVIDIA Docs][2]）

因此，例如：

```bash
nvcc -arch=sm_60 foo.cu
```

或：

```bash
nvcc -gencode arch=compute_60,code=sm_60 foo.cu
```

### 但现代ML存在一个陷阱

如果您问这个问题是因为您尝试在P100上运行**PyTorch / vLLM / FlashAttention / 现代LLM软件**，那么**CUDA 12.x支持并不意味着现代ML库支持`sm_60`**。

CUDA 12.8实际上标志着Pascal开发的终点：NVIDIA表示Pascal/Volta/Maxwell现已功能完备，**下一个主要CUDA版本将移除对这些架构的离线编译器支持**。（[NVIDIA Developer][3]）

在实践中，我建议使用：

```text
P100
  ↓
sm_60
  ↓
CUDA 11.8 / 12.x
  ↓
较旧的PyTorch/CUDA栈
```

而不是盲目安装最新的CUDA/PyTorch栈。

如果您尝试在P100上运行特定的**PyTorch版本或LLM框架**，我可以列出确切可行的`CUDA + PyTorch + 驱动程序`组合。

[1]: https://developer.nvidia.com/cuda/gpus/legacy?utm_source=chatgpt.com "Legacy CUDA GPU Compute Capability | NVIDIA Developer"
[2]: https://docs.nvidia.com/datacenter/tesla/drivers/cuda-toolkit-driver-and-architecture-matrix.html?utm_source=chatgpt.com "CUDA Toolkit, Driver, and Architecture Matrix — NVIDIA Data Center Drivers"
[3]: https://developer.nvidia.com/blog/cuda-toolkit-12-8-delivers-nvidia-blackwell-support?utm_source=chatgpt.com "CUDA Toolkit Now Available for NVIDIA Blackwell | NVIDIA Technical Blog"