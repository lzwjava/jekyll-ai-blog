---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LFortran：交互式Fortran编译器
translated: true
type: note
---

**问题：** 什么是 LFortran？

**答案：**

LFortran 是一个现代、开源（BSD 许可）、基于 LLVM 的交互式 Fortran 编译器。它支持两种模式：交互式/REPL 执行（类似于 Python 或 Julia）以及面向现代架构（包括多核 CPU 和 GPU）的提前编译。

**架构上为何重要：**

其技术栈为：Fortran 源码 → LFortran 前端（C++）→ **ASR**（抽象语义表示，他们自定义的中间表示）→ LLVM IR → 原生二进制或 WASM。ASR 层很有意思——它是一种带有类型、语义丰富的中间表示，位于解析树和 LLVM IR 之间，使得分析和优化过程更加容易。

**关键事实：**

- 约 67% C++、22% Fortran、5% Python 编写
- 支持 Jupyter 内核（Fortran 互动笔记本）
- 可编译为 WASM（`build_to_wasm.sh`）
- 仓库中包含 `CLAUDE.md` 和 `AGENTS.md` 文件——表明他们正在积极整合 AI 编码助手
- v0.61.0 于 2026 年 3 月发布，开发活跃（超过 2.5 万次提交）
- 由 NumFOCUS 支持（与 NumPy、pandas 等同组织）

**为什么 2026 年还用 Fortran？** 科学计算与高性能计算——天气建模、等离子体物理、数值线性代数。大量遗留 Fortran 代码支撑着关键科学基础设施，而目前缺乏针对 Fortran 的现代交互式编译器。LFortran 本质上试图成为 Fortran 领域的 Julia——快速、编译，但带有 REPL。

**与你领域的关联：** 考虑到你在 MI300X 上的工作以及对 GPU 计算的兴趣，GPU 编译目标是最相关的方向。LFortran 旨在通过 LLVM 将 Fortran 直接编译到 GPU 后端，这对于将遗留 HPC 代码迁移至 AMD/NVIDIA 硬件而无需用 CUDA/HIP 重写具有重要意义。

**参考：**

- [LFortran GitHub](https://github.com/lfortran/lfortran)
- [LFortran Docs](https://docs.lfortran.org/)
- [Try Online](https://dev.lfortran.org/)
