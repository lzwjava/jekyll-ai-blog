---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX Spark 运行 Windows，而非 Linux
translated: true
type: note
---

**问题：RTX Spark 能在 Linux 上运行吗？**

**答案：**

不——**RTX Spark 是 Windows-on-Arm 平台**，而非 Linux。这正是它的核心定位。不要将其与运行 Linux 的 DGX Spark 混淆。

二者的区别：

- **RTX Spark**（消费级笔记本电脑/迷你台式机，N1X 芯片）→ **Windows on Arm**。该平台由 NVIDIA 和微软联合发布，Windows 针对统一内存、异构架构上的工作负载调度、电源/热管理以及 Windows 11 Prism 模拟器（用于在 Arm 上运行 32 位和 64 位 x86 应用）提供了优化。RTX Spark PC 属于 Copilot+ PC 类别。当时的宣传语是：“有了 RTX Spark 和 Microsoft Windows，你只需提出要求——PC 就会完成工作。”

- **DGX Spark**（桌面研究主机，GB10）→ **Linux**。它预装了基于 Ubuntu 的 NVIDIA DGX OS，并附带完整的 NVIDIA AI 软件栈——CUDA、cuDNN、TensorRT、RAPIDS。

因此，两者基于相同的 GB10/Grace-Blackwell 芯片家族，但面向不同操作系统：DGX Spark 是 Ubuntu/CUDA 开发机器，而 RTX Spark 是 Windows-on-Arm 消费设备。

特别需要注意的一点：由于 RTX Spark 是 Arm + Windows 优先，你习惯的终端优先 Linux/CUDA 工作流无法直接迁移。能否在 RTX Spark 硬件上安装 Linux 发行版，取决于 NVIDIA/OEM 是否为 Blackwell GPU 模块提供 Arm Linux 驱动——而在发布时，这一点并未得到承诺；其软件工作明确集中在 Windows on Arm 上。如果你的目标是本地 CUDA 调试，DGX Spark（或运行 DGX OS 的 GB10 合作主机）才是合适的 SKU，而非 RTX Spark。

**参考链接：**

- [Nvidia RTX Spark - 维基百科](https://en.wikipedia.org/wiki/Nvidia_RTX_Spark)
- [NVIDIA 与微软重塑 Windows PC（RTX Spark）](https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark)
- [NVIDIA DGX Spark 初探 - Signal65](https://signal65.com/research/nvidia-dgx-spark-first-look-a-personal-ai-supercomputer-on-your-desk/)
