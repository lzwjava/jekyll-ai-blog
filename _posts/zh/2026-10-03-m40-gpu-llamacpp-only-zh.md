---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M40 GPU：仅限llama.cpp
translated: true
type: note
---

不——nanoGPT 使用的是 **PyTorch**（外加用于 DDP 的 `torchrun`、`torch.distributed`），同样是无法跨越的硬性障碍。在 CC 5.2 上甚至连 PyTorch 都安装不了。

以下是针对这个 M40 一贯的**经验法则**：

| 可以运行 | 无法运行 |
| --------- | ----------- |
| ✅ 任何使用 **llama.cpp** 的项目（推理、微调、嵌入、服务器） | ❌ 任何需要 **PyTorch / TensorFlow** 的项目 |
| ✅ **Whisper.cpp**（音频转文字） | ❌ vLLM, DeepSpeed, nanoGPT, HuggingFace `transformers` |
| ✅ 直接的 **CUDA C/C++** 程序 | ❌ 任何基于 CUDA 抽象构建的 Python ML 框架 |

根本区别在于：llama.cpp 编写了自身的原始 CUDA 内核，因此它可以针对 CC 5.2 进行编译。而其他所有框架（PyTorch、TF、JAX）早在多年前编译时就已经取消了对 Maxwell 架构的支持。
