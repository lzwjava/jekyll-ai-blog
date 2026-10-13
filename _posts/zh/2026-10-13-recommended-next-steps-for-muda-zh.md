---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 建议的下一步措施（Muda）
translated: true
type: note
---

好问题。考虑到 `muda 0.2.0` 现在的状态，我会这样思考。

## 现状

`muda` 是一个可用的 CUDA 兼容运行时，但栈底仍然是 NVIDIA 的 **OpenCL ICD**。所以诚实的现状是：*“CUDA API，没有 libcuda——但底层仍是 NVIDIA 用户空间。”* 从这里开始有两条截然不同的方向，它们不应混为一谈。

## 分岔路口

**路线 A——纯粹派：掌控执行路径。**
用直接与驱动/硬件通信的原生后端替换 OpenCL 后端。这是“使用 muda 驱动”的“真正”答案，但属于研究级别：

- 绑定 `nouveau` 而非 `nvidia`，使用 `drm_nouveau` GEM + 计算通道，构建 pushbuffer。
- 你还需要 SASS：要么手写 Maxwell 指令，要么复用 Mesa 的 `nv50_ir`/OpenCL 二进制容器。
- **风险：** 解绑 `nvidia` 会破坏你正在工作的 ComfyUI/llama.cpp 环境，直到重启。我只会在备用机器上或使用经过测试的恢复脚本来做这件事。
- 现实地看：需要数周时间，而且可能永远无法达到功能对等。

**路线 B——务实派：让 muda 真正有用。**
保留 OpenCL 后端，但构建人们在 M40 上真正想要的东西：BLAS、真实工作负载、即插即用的 CUDA shim，以及 Python。快速、低风险、可立即演示。

## 我接下来实际会做什么（路线 B，推荐）

**里程碑 1——让它有用（价值最高，约 1 次会话）**

- `mudaBLAS`：调优的 `SGEMM`/`SGEMV`（tile + 寄存器分块，`float4` 向量化）。
- 基准测试套件 vs. 朴素实现，跟踪 GB/s 和 GFLOP/s。
- 一个真实演示：在 M40 上使用 muda + mudaBLAS 端到端训练一个小型 MLP（或 mini-GPT）。

**里程碑 2——让它成为即插即用（约 1 次会话）**

- 在 muda 之上实现 CUDA **运行时** API 名称作为 shim（`cudaMalloc`、`cudaMemcpy`、`cudaLaunchKernel`、`cudaDeviceSynchronize`...），这样现有的单文件 `.cu` 示例可以**不加修改**地针对 `muda.h` 编译。
- 通过 `ctypes` 提供 Python 绑定 + 近似零拷贝的 numpy 互操作。

**里程碑 3——原生实验（可选，独立分支）**

- 从一个*安全*的实验开始：`driver_opencl_exec` 混合模式，其中 OpenCL 仅用作**编译器**（`clGetProgramInfo(CL_PROGRAM_BINARIES)` → SASS），而 muda 通过 `nouveau` 拥有分配和提交。这通过保留 OpenCL 用于代码生成来降低路线 A 的风险。
- 将其放在一个分支上，并带有 `unbind/rebind` 辅助脚本和经过测试的恢复路径。

## 快速决策指南

| 如果你的目标是…… | 那么这样做 |
| --- | --- |
| “证明它在 M40 上能做实际工作” | 里程碑 1 |
| “从 Python / 现有 CUDA 代码中使用它” | 里程碑 2 |
| “真正不依赖 NVIDIA 用户空间” | 路线 A / 里程碑 3（研究） |
| “最安全的增量打磨” | 更多 API 测试 + 用于 CI 的 `driver_cpu` |

## 我的建议

从**里程碑 1** 开始——它将 muda 从“一个聪明的 API 包装器”变成“一个我真正会运行的东西”。然后里程碑 2 让它变得可采纳。将路线 A 保留为一个独立的、明确风险的研究分支。

要我着手开始里程碑 1（`mudaBLAS` + 调优的 SGEMM + 小型 MLP 演示和基准测试）吗？
