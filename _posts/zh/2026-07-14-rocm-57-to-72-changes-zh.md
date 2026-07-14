---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ROCm 5.7到7.2版本变更
translated: true
type: note
---

问题：ROCm 从 5.7.0（最后一个“完全支持”您的 MI50/gfx906 的版本）到当前版本之间发生了什么变化？

答案：

当前稳定版是 **ROCm 7.2.4**（2026 年 5 月），7.10.0 作为活跃的技术预览流。以下是您特别关心的内容：

**1. gfx906（MI50/MI60/Radeon VII）已从“维护模式”变为主动移除**

- ROCm 5.7 → 6.0：gfx906 进入维护模式（仅修复漏洞，无新功能）——您当时停在了这个阶段。
- ROCm 7.0：AMD 完全从 ROCm Compute Profiler 中移除了 MI50/MI60 专用 YAML 数据——不仅是“停止优化”，而是直接在工具中删除了设备支持。Phoronix 关于此事的报道引发了足够多的社区反对，AMD 表示会考虑撤销这一更改，但方向已经明确：gfx906 正在从工具链中逐步淘汰，而不仅仅是降级优先处理。
- 当前的官方兼容性矩阵（7.9.0、7.10.0）仅列出 CDNA2/3/4（MI210/250/300/350）和 RDNA3/4 消费级显卡——gfx906 已完全不再出现。

**2. 仍然可用的方案（社区维护，非 AMD 官方提供）**

- MI50 在 ROCm 6.4.3 上运行良好，只需从 Arch 的 `extra` 仓库拉取一个小的 rocblas 包替换即可——在活跃的 GitHub 讨论中已确认可用。
- `vllm-gfx906`（社区分支）搭配 Ubuntu 24.04 LTS + ROCm 6.4.3 是当前推荐的 gfx906 推理服务栈。
- Arch Linux 通过 pacman 可直接为 gfx906 打包 ROCm，无需额外破解——如果您希望减少麻烦，这比 Ubuntu 的官方 ROCm 包更优。
- llama.cpp 的 ROCm 后端在 gfx906 上存在开放性回归问题（在较新模型架构如 Qwen3.5 上崩溃）——Vulkan 后端是同一硬件上的安全备选。

**3. 5.7 → 7.2 更大的结构性变化（间接影响您）**

- ROCTracer、ROCProfiler、rocprof 和 rocprofv2 已弃用——请迁移至 rocprofv3（基于 ROCprofiler-SDK）。预计生命终期（EOS）为 2026 年第二季度末。
- ROCm SMI 正在进入维护模式——AMD SMI 是后继者，将持续获得功能更新。
- ROCm 7.2 将 Windows 和 Linux 统一为单一发布流，并大力推动消费级硬件（Ryzen AI 300/400、Radeon RX 7000+）与 ComfyUI 集成——AMD 当前的投资明显集中在消费级/APU 和 MI300 级数据中心，而非您使用的旧款 CDNA1/GCN5.1 显卡。
- 每个大版本号更新（5→6→7）都会破坏向后兼容性（HIP 运行时 API 变化、rocRAND/hipRAND 重新打包、文件结构重组）——因此，为 gfx906 绑定 6.4.3 意味着您只能停留在此；没有干净的升级路径可以进入 7.x 并用于 MI50。

**对您的显卡的实际建议：** 将 ROCm 6.4.3 视为 MI50 的最终上限，在 Ubuntu 24.04 或 Arch Linux 上运行，使用 `vllm-gfx906` 进行推理服务，且不要期待任何新的 ROCm 功能（Triton 内核改进、FlashAttention 更新、更新的 PyTorch ROCm 构建）会支持 gfx906——您从此刻起将停留在社区修补的冻结栈上。

参考文献：

- [AMD 硬件理想情况下应支持约 10 年 — Phoronix（ROCm 7.0 Profiler 移除）](https://www.phoronix.com/news/AMD-ROCm-Hardware-Length)
- [ROCm 设备支持愿望清单 — gfx906 社区状态](https://github.com/ROCm/ROCm/discussions/4276)
- [ROCm 7.2.4 发布说明 — rocprofv3/AMD SMI 弃用](https://github.com/ROCm/ROCm/releases)
- [ROCm 7.10.0 兼容性矩阵](https://rocm.docs.amd.com/en/7.10.0-preview/compatibility/compatibility-matrix.html)
- [CES 2026 上的 ROCm 7.2.2 — VideoCardz](https://videocardz.com/newz/amd-highlights-rocm-7-2-2-at-ces-2026-with-ryzen-ai-400-support-and-a-single-windows-plus-linux-release)
