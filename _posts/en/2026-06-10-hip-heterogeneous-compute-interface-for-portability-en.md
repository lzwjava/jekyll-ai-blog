---
audio: false
generated: true
image: false
lang: en
layout: post
title: "HIP: Heterogeneous-compute Interface for Portability"
translated: false
type: note
---

Question: What does HIP stand for and mean?

Answer: **HIP** stands for **Heterogeneous-compute Interface for Portability**.

It is an open-source C++ runtime environment and programming model developed by AMD. It allows developers to write portable code that can run on both AMD and NVIDIA GPUs from a single source codebase.

---

### Key Concepts of HIP

#### 1. Code Portability

Before HIP, code written for NVIDIA GPUs used **CUDA**, which cannot run natively on AMD hardware. HIP solves this by providing a syntax that is highly similar to CUDA. This allows developers to maintain a single C++ codebase that compiles and runs on both platforms:

* When compiled on an NVIDIA platform, HIP maps directly to CUDA with zero performance overhead.
* When compiled on an AMD platform, it uses AMD's ROCm compiler (like `hipcc`) to run on AMD hardware.

#### 2. The Ecosystem Role

HIP acts as a translation and abstraction layer. AMD provides a tool called **HIPIFY** which automatically converts existing CUDA code into HIP C++ code. Once converted, the code can target either hardware family.

| Feature | NVIDIA Ecosystem | AMD Ecosystem |
| --- | --- | --- |
| **Language / Interface** | CUDA | **HIP** |
| **Compiler** | `nvcc` | `hipcc` (uses LLVM/Clang) |
| **Hardware Target** | GeForce / Tesla / Hopper / Blackwell | Radeon / Instinct (e.g., MI300X) |

#### 3. Why it matters in the log you shared

In your previous log, you saw commands like `/opt/rocm-7.2.0/bin/hipcc` and source files ending in `.hip`. This means the **FlashAttention** code (which was originally written for NVIDIA CUDA) has been adapted using HIP so it can compile and execute efficiently on AMD Instinct GPUs.
