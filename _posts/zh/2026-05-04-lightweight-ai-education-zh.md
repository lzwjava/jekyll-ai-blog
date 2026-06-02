---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 教育用轻量级人工智能库
translated: true
type: note
---

**Axono** 是一个轻量级的 AI/深度学习库（采用中文编写，针对教学/研究场景设计），具备以下特性：

- **C++ 核心**（支持 CPU 与 CUDA 后端）并通过 CMake 提供 Python 绑定
- **张量抽象**，支持 int8 至 float64 数据类型
- **运算符**：矩阵乘法（`@`）、加法（`+`）、ReLU 激活函数
- **NumPy 交互**：`to_numpy()` / `from_numpy()` 方法
- **设备支持**：CPU 与 NVIDIA CUDA GPU
- **神经网络模块系统**（`axono.nn`）包含多种层结构

可将其视为用于教学张量运算的、类似 PyTorch 的极简框架。
