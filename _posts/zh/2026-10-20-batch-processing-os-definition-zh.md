---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 批处理操作系统定义
translated: true
type: note
---

问题："批处理操作系统"是什么意思？

答案：**批处理操作系统** 即 **Batch Processing Operating System**。

它指的是一种早期的操作系统设计，其中作业（程序/任务）被收集成一组（"批"），并在处理过程中无需用户交互地顺序执行。

主要特点：
- 作业提前提交并排队
- 操作系统自动依次运行它们（在更高级的版本中可并行运行）
- 作业运行时无实时用户交互
- 常见于早期大型机计算时代（1950–60年代）

两种主要子类型：
- **单道批处理**：一次运行一个作业；CPU在I/O期间空闲
- **多道批处理**：内存中加载多个作业；当一个作业等待I/O时，CPU切换到另一个作业——效率更高

经典例子是IBM的早期OS/360。现代等效系统包括HPC作业调度器如SLURM或PBS，以及云批处理服务如AWS Batch。

参考：
- [批处理 - 维基百科](https://en.wikipedia.org/wiki/Batch_processing)
- [操作系统历史 - 维基百科](https://en.wikipedia.org/wiki/History_of_operating_systems)