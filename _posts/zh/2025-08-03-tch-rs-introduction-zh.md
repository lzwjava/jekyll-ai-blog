---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch的Rust绑定
translated: true
type: note
---

### tch-rs 简介

tch-rs 是一个 Rust 包，为 PyTorch 的 C++ API 提供绑定，特别是封装了 libtorch 库。其主要目的是让 Rust 开发者能够在 Rust 应用程序中直接利用 PyTorch 强大的张量计算、自动微分和机器学习能力。通过提供与原始 C++ API 对应的精简底层封装，tch-rs 允许在其基础上创建更符合 Rust 语言习惯的抽象层，使得在 Rust 生态系统中执行模型训练、推理和张量操作等任务变得更加便捷。

#### 核心特性
- **张量运算与自动求导**：支持核心张量算术、梯度计算，以及通过 Adam 等优化器进行模型训练的反向传播。
- **神经网络 API**：包含构建和训练神经架构的工具，例如在 MNIST 数据集上的简单前馈网络示例。
- **模型加载**：支持使用 safetensors 格式导入预训练的 PyTorch 模型，该格式高效且无需 Python 依赖。
- **示例与用例**：提供实用演示，涵盖张量创建基础、梯度下降训练、自定义神经网络以及运行预训练模型（如用于图像分类的 ResNet18）。
- **跨平台支持**：可在多种系统上运行，支持 CPU 或 GPU（CUDA）加速。

该项目采用 Apache-2.0 和 MIT 许可证，积极维护，并从 ocaml-torch 等相关项目中汲取了部分代码生成思路。

#### 快速开始
使用 tch-rs 需要在系统上安装 libtorch（PyTorch 的 C++ 发行版）。通过 Cargo 将其添加到 Rust 项目中：
```
[dependencies]
tch = "0.17.2"  # 请检查最新版本
```
通过手动下载 libtorch、使用系统安装或启用如 `download-libtorch` 等功能进行自动获取来设置 libtorch。对于 GPU 支持，需指定 CUDA 版本（例如通过 `TORCH_CUDA_VERSION=cu117`）。使用诸如 `cargo run --example basics` 的命令运行示例。请注意，Windows 用户应优先使用 MSVC 工具链，并且可通过环境变量进行静态链接。

更多详细信息，请参阅代码库中提供的文档和示例。

[tch-rs GitHub 代码库](https://github.com/LaurentMazare/tch-rs)
[tch-rs 文档](https://docs.rs/tch)
