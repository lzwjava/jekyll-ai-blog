---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA驱动向后兼容性
translated: true
type: note
---

正确。NVIDIA 驱动程序是向后兼容的。驱动 580.x 支持 CUDA 12.0 至 13.0。

当你安装 `torch==2.5.1+cu124` 时，pip 包中会捆绑其自身的 CUDA 12.4 运行时库。驱动程序只需要*足够新*以支持该 CUDA 版本即可——580.x 完全满足要求。无需安装驱动，也无需更改系统 CUDA。

因此，是的，这台机器可以同时运行：
- 系统 CUDA 13.0（任何原生使用它的程序）
- 虚拟环境中的 CUDA 12.4 wheel 包（通过 pip 安装的 torch/triton）

它们不会冲突——虚拟环境中的 CUDA 运行时是自包含的，通过内核模块与同一个驱动程序通信。