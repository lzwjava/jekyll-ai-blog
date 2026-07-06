---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpCore-Simplify自动化EFI构建器
translated: true
type: note
---

**问题：** 请介绍一下 OpCore-Simplify 项目（github.com/lzhoang2801/OpCore-Simplify）。

**回答：**

**OpCore-Simplify** 是一个 Python CLI 工具（约 6.4k 星标，592 分支，BSD-3-Clause 许可证），它自动化了黑苹果（Hackintosh）过程中最繁琐的部分：根据你的确切硬件构建一个 OpenCore EFI 文件夹，而不是通过遵循 Dortania 指南手动组装。

### 它解决的问题

手动构建 OpenCore EFI 意味着：导出 ACPI 表、确定你的主板需要哪些 SSDT 补丁、选择合适的 kext（Lilu、WhateverGreen、VirtualSMC、音频编解码器、网卡驱动……）、选择 SMBIOS，并手动编辑一个包含数百个键值的 `config.plist`。一个错误的 quirks 设置 = 内核崩溃。OpCore-Simplify 将其转化为一个流水线：**硬件报告输入 → 可启动的 EFI 输出**。

### 工作原理（流水线）

1. **硬件检测** — 在 Windows 上可以直接导出硬件报告；否则你可以提供来自其配套工具 Hardware-Sniffer 的 `Report.json` 和 ACPI 转储文件。
2. **兼容性检查** — `Compatibility Checker`（兼容性检查器）会告诉你哪些设备和 macOS 版本你的硬件支持。
3. **ACPI 补丁** — 集成 SSDTTime 处理常见补丁（FakeEC、FixHPET、PLUG、RTCAWAC），外加自定义补丁：修复 _PRW 休眠状态值以防止立即唤醒、禁用不支持的 PCI 设备、添加 PNLF、MCHC、USBX 等设备，以及 HEDT 特定的内核崩溃修复。
4. **Kext 和引导加载程序获取** — 在每次构建前自动检查并从 Dortania Builds 和 GitHub Releases 下载最新的 OpenCorePkg 和 kext。
5. **config.plist 生成** — 应用基于经验的默认设置：对未被识别的 AMD 显卡进行 GPU ID 伪冒、针对 Intel P/E 核心 CPU 的 CpuTopologyRebuild、ResizeAppleGpuBars 配置、针对电源管理和性能优化的 SMBIOS 选择，以及用于启动时自动连接的 itlwm WiFi 配置文件。

### 硬件覆盖范围

Intel Nehalem（第1代）至 Arrow Lake（第15代/Core Ultra 2），AMD Ryzen/Threadripper 通过 AMD Vanilla 补丁支持；GPU 涵盖 Intel iGPU（Iron Lake → Ice Lake）、AMD Navi 21/22/23 和 Vega APU，以及旧款 NVIDIA（Kepler/Pascal/Maxwell）；macOS 支持从 High Sierra 到 Tahoe 26——其中 Tahoe 支持依赖于作者自己的 OpenCore Legacy Patcher 3.0.0 分支，因为官方 Dortania 发布版无法与 Tahoe 早期补丁配合使用。

### 仓库结构

简洁易读——`OpCore-Simplify.py` 是入口点，`Scripts/` 包含逻辑（包括 `datasets/kext_data.py`，实际上是一个 curated 知识库，将硬件 ID 映射到 kext），外加 `.bat`/`.command` 启动器。96% Python 代码，没有繁重的依赖——其风格与 corpnewt 的工具（SSDTTime、UnPlugged）一脉相承，并在此基础上构建。

### 注意事项

作者明确指出，它不能保证一次就成功安装——你仍然需要 Dortania 指南的基础知识，之后还需要进行 USB 端口映射，并且要有排查问题的耐心。它能为你提供一个**非常好的起点 EFI**，而不是一个即装即用的安装方案。

值得一提的是：这里的工程设计亮点在于编码后的专家知识——多年的黑苹果社区经验法则被压缩成基于规则的 Python 代码（硬件指纹 → 补丁集）。这是一个经典的专家系统；一个有趣的思维实验是：`kext_data.py` 和 ACPI 补丁启发式规则中，有多少可以被一个直接读取 ACPI 转储的智能体所替代。

**参考资料：**

- [OpCore-Simplify — GitHub](https://github.com/lzhoang2801/OpCore-Simplify)
- [Dortania OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/)
- [Hardware-Sniffer（配套工具）](https://github.com/lzhoang2801/Hardware-Sniffer)
