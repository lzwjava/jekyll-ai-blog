---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: AMD引领开源GPU支持发展
translated: true
type: note
---

### AMD 与 NVIDIA：开源承诺对比

是的，普遍认为 AMD 比 NVIDIA 更拥抱开源，尤其在 GPU 驱动程序、软件堆栈和生态系统支持方面。这源于 AMD 长期致力于完全开源解决方案，特别是在 Linux 领域——其驱动程序成熟稳定、直接集成于内核且由社区驱动。NVIDIA 近年来虽在开放化方面取得进展，但仍严重依赖专有组件来实现完整性能和功能。下面我将从关键领域进行剖析。

#### GPU 驱动程序
- **AMD**：AMDGPU 驱动程序完全开源，自 2016 年起成为 Radeon GPU 的默认驱动。它直接集成在 Linux 内核中（截至 2025 年中已超 590 万行代码），为图形渲染、计算和 Vulkan 提供开箱即用的支持，无需专有组件。这为 Linux 用户和开发者带来了无缝体验。
- **NVIDIA**：NVIDIA 传统驱动程序是闭源的，需要手动安装才能获得最佳性能。虽然自 2022 年起他们开源了内核模块（通过 `nvidia-open` 项目），但用户空间组件仍保持闭源。其新近推出的 Rust 架构 NOVA 驱动及 Nouveau 改进仍处于实验阶段，功能完整性尚有欠缺（例如截至 2025 年末，开源版本仍不支持完整的 DLSS 和高级光线追踪）。

**优势方**：在 Linux 等开放环境中，AMD 在可靠性和集成度方面胜出。

#### 计算与人工智能软件堆栈
- **AMD**：ROCm（Radeon 开放计算平台）完全开源，支持 PyTorch、TensorFlow 等机器学习框架在 AMD GPU 上运行。该平台设计具备跨硬件与操作系统的可移植性，不过在生态成熟度上曾长期落后于竞争对手。
- **NVIDIA**：CUDA 是 GPU 加速计算的金标准，但属于 NVIDIA 专属的闭源技术。虽然存在 OpenCL 等替代方案，但优化程度较低。NVIDIA 已开源部分组件（如 cuDNN 子集），但核心堆栈仍保持封闭，限制了跨平台互操作性。

**优势方**：AMD 在开放性上领先，但 NVIDIA 在完善度与功能丰富度上占据统治地位——这往往以供应商锁定为代价。

#### 生态系统与社区建设
- AMD 积极为 Mesa（图形驱动集合）等开源项目做贡献，并原生提供更完善的 Wayland 支持。这种开放策略促进了社区贡献，有效减轻了开源发行版用户的维护负担。
- NVIDIA 的进展包括开放 vGPU 补丁和 2025 年 Nouveau 驱动可靠性的提升，但固件闭源、Vulkan 支持不完善等问题依然存在。根据社区反馈，其开放程度更接近“开放粉饰”而非真正承诺。

总而言之，如果“更开源”意味着代码可自由获取、可修改且无专有依赖，那么 AMD 明显领先——尤其在 Linux 游戏开发、AI 推理等领域表现突出。NVIDIA 在原始性能和独家功能方面表现卓越，但在技术透明度方面稍逊一筹。最终选择取决于您的优先级：要开放自由（AMD）还是生态优势（NVIDIA）。

#### 参考资料
- [AMD 与 NVIDIA GPU：Linux 系统如何选择？（Reddit 2023 年讨论）](https://www.reddit.com/r/linux_gaming/comments/18nv50w/amd_vs_nvidia_gpu_which_is_better_on_linux_updated/)
- [Linux 系统显卡抉择：NVIDIA 还是 AMD？（Linuxiac 2025 年分析）](https://linuxiac.com/nvidia-vs-amd-gpus-on-linux/)
- [开源版 NVIDIA Linux 驱动可靠性将大幅提升（Phoronix 2025 年报道）](https://www.phoronix.com/news/Nouveau-More-Reliable-Fix)
- [AMD 内核显卡驱动在 Linux 6.16 中突破 590 万行代码（Phoronix 2025 年数据）](https://www.phoronix.com/news/Linux-6.16-AMDGPU-Driver-Size)
- [NVIDIA 发布最新开源 vGPU 支持驱动补丁（Phoronix 2025 年动态）](https://www.phoronix.com/news/NVIDIA-vGPU-RFC-v2)
