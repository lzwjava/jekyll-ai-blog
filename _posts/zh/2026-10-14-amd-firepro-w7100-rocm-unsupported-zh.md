---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD FirePro W7100 ROCm 不支持
translated: true
type: note
---

**问题：** 哪些 ROCm 版本可以在 AMD FirePro W7100 上运行？

---

**答案：**

**简短回答：官方上没有任何版本支持。** W7100 实际上在所有 ROCm 版本中均不受支持。

**原因——GPU ID 问题**

W7100 使用的是 **Tonga** 芯片，在 ROCm 中被标识为 **`gfx802`**。这是一个关键区别：

| GPU | ROCm ID | ROCm 支持情况 |
|---|---|---|
| Tonga (FirePro W7100) | `gfx802` | ❌ 从未被官方支持 |
| Fiji / Polaris (RX 480, RX 580…) | `gfx803` | ✅ 直到约 ROCm 3.7 可用，之后出现问题；ROCm 4.0+ 完全移除 |

除了 Tonga（`gfx802`）之外，自 2015 年以来所有 AMD GCN GPU 都曾受到 ROCm 支持。Tonga 的支持被明确排除在外。

由于许多 ROCm 项目依赖 HCC（编译器），而 HCC 默认不针对 `gfx802` 编译，因此 Tonga 在整个技术栈中实际上始终无法正常工作。

**时间线摘要**

| ROCm 版本 | W7100 / Tonga 状态 |
|---|---|
| 1.x – 2.x | 可部分检测到，但无法用于 HIP/HCC 计算 |
| 3.x | 仍无法识别 / 已损坏 |
| 4.0+ | gfx803（Fiji）也被移除；gfx802 从来就不在其中 |
| 5.x → 当前 | 完全没有 GCN 支持 |

ROCm 5.7.1 是即使是 gfx803（Polaris）也能正常工作的最后一个版本，而 ROCm 6+ 完全移除了支持——运行时显示“Unsupported HSA device”错误。W7100 的 `gfx802` 甚至从未达到过那个水平。

**什么可以正常工作？**

- ✅ **OpenCL** — 通过 **AMDGPU-PRO 闭源驱动**（而非 ROCm）正常工作
- ROCm 通过 `clinfo` 将该卡识别为 `Tonga PRO GL [FirePro W7100]`，但 OpenCL 显示为 v1.2（可能具备 v2.1 能力）——这是通过闭源栈运行的，而非 ROCm 的开放计算栈。
- ❌ **HIP / ROCm 计算** — 任何版本下都无法在此卡上使用

**底线：** 如果你购买这张卡是为了基于 ROCm 的 AI/ML（通过 ROCm 使用 PyTorch、TensorFlow），它**将无法工作**。它更适合 OpenCL 工作负载、CAD/可视化或多显示器使用。

---

**参考链接：**
- [GitHub – Does ROCm support Tonga? #509](https://github.com/RadeonOpenCompute/ROCm/issues/509)
- [GitHub – gfx802 segfaults with ROCm 2.7 #880](https://github.com/ROCm/ROCm/issues/880)
- [Debian AI List – Dropping gfx803 support](https://lists.debian.org/debian-ai/2024/09/msg00030.html)
- [Phoronix – AMD GCN3/Fiji Support Retired from GCC](https://www.phoronix.com/news/AMD-GCN3-Fiji-GCC-Removal)