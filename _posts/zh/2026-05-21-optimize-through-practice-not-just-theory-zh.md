---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过实践优化，而非仅理论
translated: true
type: note
---

问题：学习优化的关键是否在于专注于实际任务，并尝试用AI改进它们，而不仅仅是阅读——例如，优化AMD ROCm内核？

回答：

是的，这种方法非常有效。优化，尤其是在计算或AI领域，本质上离不开**实际应用**。阅读和理论能提供基础理解，但真正的掌握来自于在真实问题上进行实验，因为其中的权衡、约束和性能指标都是具体的。

以 **AMD ROCm内核优化** 为例：

* 你有一个**真实的工作负载**（内核），可以通过执行时间、内存使用量和吞吐量来衡量。
* AI辅助方法，例如使用机器学习来建议分块、展开或内存访问模式，能够提供**数据驱动的洞察**，这是单纯通过阅读难以获得的。
* 迭代测试让你能够**立即看到更改的效果**，从而加深对底层硬件的理解和直觉。

这一原则广泛适用：无论是优化代码、供应链、神经网络，还是业务流程，**动手实验**加上度量衡，都能比纯理论带来更深的理解。

参考：

* [ROCm优化指南](https://rocmdocs.amd.com/en/latest/ROCm_Optimization_Guide/ROCm_Optimization_Guide.html)
* [实践性能优化](https://developer.amd.com/resources/rocm-tools/)
* [AI辅助代码优化概念](https://arxiv.org/abs/2005.06723)
