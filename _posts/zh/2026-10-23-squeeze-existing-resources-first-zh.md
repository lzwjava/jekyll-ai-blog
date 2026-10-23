---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 先挖掘现有资源潜力
translated: true
type: note
---

问题：先从充分利用现有设备资源来尽可能多地学习（例如，掌握计算机基础，这本身就需要付出很大努力），然后逐步扩展到像GPU编程这样的领域，这是一个好策略吗？

答案：是的，这实际上是一个非常合理且实用的方法。以下是一些原因说明为什么它效果很好：

**为什么“首先充分利用现有资源”是合理的：**

- **深度优先于广度** —— 真正理解CPU、内存、OS和编译器如何协同工作并非易事。大多数人低估了这个领域的深度（caching、branch prediction、syscalls、threading等）。
- **强大的基础可以迁移** —— 你在CPU/通用系统上学到的一切都会直接对GPU工作有所启发。GPU编程（CUDA、ROCm）本质上就是“假如我们有10,000个较弱的CPU核心，并且必须非常谨慎地考虑内存会怎样？”—— memory hierarchy、parallelism和latency等概念是共通的。
- **成本效益** —— GPU（尤其是云GPU时间）很昂贵。先在笔记本电脑/台式机上熟练掌握意味着你能在昂贵的GPU时间上减少新手错误的花费。
- **避免过早的复杂性** —— 在理解memory models或parallelism之前就跳到GPU，会导致难以理清的困惑。

**一个适合你计划的大致过程：**

| 阶段 | 重点 | 示例工具 |
| --- | --- | --- |
| 1 | 编程基础 + 算法 | Python, C, any CPU |
| 2 | 计算机系统（OS, memory, networking） | Your existing machine |
| 3 | 性能与剖析 | `perf`, `valgrind`, flame graphs |
| 4 | CPU并行 | multithreading, SIMD |
| 5 | GPU基础 | CUDA/ROCm, Google Colab (free GPU) |
| 6 | 深度学习 / HPC | PyTorch, distributed systems |

**关键见解：** 一旦你真正深入掌握了CPU级别的parallelism，从阶段4到阶段5的跨越就会感觉小得多。很多人过早跳到GPU，结果发现它令人困惑。

所以说，是的——你的直觉是正确的。掌握你面前的这台机器并不是“退而求其次”，而是构建一个心智模型，让所有更困难的事情自然到来。
