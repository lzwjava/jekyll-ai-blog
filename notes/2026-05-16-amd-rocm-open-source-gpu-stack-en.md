---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD ROCm Open-Source GPU Stack
translated: false
type: note
---

Question: What is AMD ROCm, as introduced on its GitHub repository?

Answer:

## AMD ROCm — Introduction

### What is ROCm?

ROCm (Radeon Open Compute) is an open-source stack, composed primarily of open-source software, designed for graphics processing unit (GPU) computation. It consists of a collection of drivers, development tools, and APIs that enable GPU programming from the low-level kernel all the way to end-user applications.

ROCm is optimized for Generative AI and HPC applications, and it is designed to make migrating existing code straightforward.

---

### Core Technology: HIP

ROCm is powered by AMD's Heterogeneous-computing Interface for Portability (HIP), an open-source C++ GPU programming environment and its corresponding runtime. HIP allows ROCm developers to create portable applications on different platforms by deploying code on a range of platforms — from dedicated gaming GPUs to exascale HPC clusters.

---

### Key Use Cases

ROCm is particularly well-suited to GPU-accelerated high-performance computing (HPC), artificial intelligence (AI), scientific computing, and computer-aided design (CAD).

---

### Programming Models & Framework Support

ROCm supports multiple programming languages and programming interfaces such as HIP, OpenCL, and OpenMP. It is also an open-source software platform optimized to extract HPC and AI workload performance from AMD Instinct GPUs and AMD Radeon GPUs while maintaining compatibility with industry software frameworks.

ROCm is fully integrated into machine learning frameworks such as PyTorch and TensorFlow, and it supports all AMD Instinct™ accelerator models.

---

### Hardware Support

ROCm supports all AMD Instinct™ accelerator models, and certain ROCm features support select AMD Radeon™ graphics cards. The latest version provides full support for AMD Instinct™ MI350 Series GPUs, distributed inference with open-source framework support, enterprise-ready AI tools, and support for large-scale models with new data types FP6 and FP4.

---

### Platform Expansion (2025–2026)

ROCm 7.2 supports both Linux and Windows environments — a notable shift from its historically Linux-centric deployment. AMD also confirmed compatibility with its latest Ryzen AI 400 processors and Radeon AI PRO GPUs, and claimed a up to 5× performance uplift compared to ROCm 6.4.4 across key AI models.

---

### Real-World Scale: Supercomputers

AMD powers 156 supercomputers on the TOP500 list (as of November 2024), marking a 29% increase from the previous year. The El Capitan supercomputer — the world's fastest — achieved 1.742 exaflops on the HPL benchmark, powered by AMD Instinct MI300A APUs running ROCm 6.0.

---

### History & Milestone

As 2026 marks the 10th anniversary of the ROCm AI stack, AMD CTO Mark Papermaster noted that the stack — initially aimed at HPC applications — has since become production-ready software running in the world's largest supercomputers.

---

### Repository at a Glance

| Item | Detail |
| ------ | --------- |
| GitHub Stars | 6.2k |
| Forks | 517 |
| License | MIT |
| Latest Release | ROCm 7.2.0 (Jan 2026) |
| Language | Primarily Shell, Python, Makefile |
| Documentation | [rocm.docs.amd.com](https://rocm.docs.amd.com) |

References:

- [AMD ROCm GitHub Repository](https://github.com/ROCm/ROCm)
- [AMD ROCm Official Product Page](https://www.amd.com/en/products/software/rocm.html)
- [ROCm Official Documentation](https://rocm.docs.amd.com/)
- [ROCm 7.2 Windows & Linux Expansion — Neowin](https://www.neowin.net/news/amd-rocm-open-source-nvidia-cuda-rival-gets-massive-windows--linux-improvements/)
- [AMD ROCm Powering Supercomputers](https://rocm.blogs.amd.com/ecosystems-and-partners/rocm-revisited-power/README.html)
- [The Road to ROCm on Radeon for Windows and Linux — AMD Blog](https://www.amd.com/en/blogs/2025/the-road-to-rocm-on-radeon-for-windows-and-linux.html)
