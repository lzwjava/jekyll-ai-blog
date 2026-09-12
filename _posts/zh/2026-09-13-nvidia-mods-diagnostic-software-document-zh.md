---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA MODS诊断软件文档
translated: true
type: note
---

这是一份 **NVIDIA 机密文档**，标题为：

**"MODS - 模块化诊断软件"**
用于 **367.X 诊断**（文档版本 R367_v02，共 84 页）

以下是文档内容摘要：

### 什么是 MODS？

MODS 代表 **模块化诊断软件（Modular Diagnostic Software）**——它是 NVIDIA 内部用于测试和验证 NVIDIA GPU 的诊断工具。它是一个基于 JavaScript 的测试框架，运行在 NVIDIA 硬件上。

### 文档主要内容

1. **并发测试** — 如何在一张或多张 GPU 上同时运行多个 MODS 测试，包括前台/后台线程管理。
2. **命令行参数** — 详细的 CLI 选项，如 `-bgfunc`、`-bgtest`、`-concurrent_devices`、`-threadid` 等。
3. **测试规格函数** — `-savespec` 和 `-readspec` 用于保存/加载自定义测试配置。
4. **错误代码（1–842）** — GPU 诊断的完整错误代码列表，涵盖：
   - 常规软件错误
   - NVRM（NVIDIA 资源管理器）错误
   - OpenGL 错误
   - GPU 通道/FIFO 错误
   - 音频/HDMI/显示错误
   - USB、PCIe、热管理、ECC、SLI 错误
   - Tegra 专属错误
   - 以及其他更多错误

这显然是一份 **NVIDIA 内部工程文档**，标注为 **"NVIDIA CONFIDENTIAL"**——不适用于公开发布。
