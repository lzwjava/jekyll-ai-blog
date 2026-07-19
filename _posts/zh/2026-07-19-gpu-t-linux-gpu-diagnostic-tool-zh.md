---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU-T：Linux GPU 诊断工具
translated: true
type: note
---

问题：你能解释一下GitHub上的GPU-T仓库是什么以及它的功能吗？

答案：**GPU-T** 是一款专为 **Linux** 设计的开源显卡诊断与信息工具。它的创作灵感主要来源于 **GPU-Z**（Windows 平台上用于验证图形硬件、监控性能指标以及查看实时传感器数据的流行工具）。

开发者启动该项目的原因是 Linux 缺乏一款能提供简洁、信息密度高的图形用户界面（GUI）的 GPU-Z 直接替代品。

### 主要功能

* **详细的硬件诊断：** 利用可更新的本地 JSON 数据库，识别确切的 GPU 制造商、型号、修订版本、芯片尺寸、晶体管数量及发布日期。
* **实时传感器监控：** 追踪核心/显存时钟速度、温度（边缘与热点）、风扇转速、功耗（板卡功率）等实时指标，并支持将数据记录到文本文件。
* **高级功能检测：** 检查 PCIe 可调整大小 BAR（ReBAR）状态、驱动/BIOS 版本、内存类型/供应商以及 API 支持情况（Vulkan、OpenCL、CUDA、光线追踪）。
* **多媒体能力：** 提供视频编解码能力验证，如 VA-API（适用于 AMD）和 NVENC/NVDEC（适用于 NVIDIA）。

### 技术细节与架构

* **框架：** 使用 **.NET** 和 **Avalonia UI** 构建，可实现响应式用户界面，原生支持深色、浅色和自动主题模式。
* **架构：** 采用干净的 Model-View-ViewModel（MVVM）架构，并设计为供应商无关（使用工厂模式），从而易于在不修改 UI 代码的情况下添加对不同供应商的支持。
* **无需 root 权限：** 直接从用户可访问的系统路径（如 `/sys/class/drm`）和标准 Linux 实用程序中读取信息，因此运行时不需要管理员或 root 权限。
* **支持的硬件：** 完整实现了对 **AMD Radeon**（2014 年及以后，使用 `amdgpu` 驱动）和 **NVIDIA GeForce**（2010 年及以后，使用专有驱动）的支持。已针对 Intel Arc 显卡做好了初步架构准备。

### 安装

GPU-T 主要作为自包含的 **AppImage** 发布（该格式捆绑了所需的 .NET 运行时，因此无需单独安装）。也可以通过 Arch Linux 的 AUR（`gpu-t`）或 `am` 包管理器（`amMan`）进行安装。

参考来源：

* [GitHub - lseurttyuu/GPU-T](https://github.com/lseurttyuu/GPU-T)
