---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 信号数字化的三个关键步骤
translated: true
type: note
---

问题：模拟信号数字化转换过程中包含的三个阶段是什么，它们是 sampling、quantization 和 ______？

答案：

模拟信号数字化的转换过程涉及三个基本步骤：

1. **Sampling**：这是对连续时间模拟信号在离散时间间隔处测量幅度的过程。结果是一个离散时间信号，其中幅度仍然是连续的。
2. **Quantization**：在这一步中，从采样获得的连续幅度值被映射到有限的离散电平集。这引入了称为 quantization noise 的小误差，但允许信号幅度以数字方式表示。
3. **Encoding**：这是最后一步，每个量化电平被分配一个唯一的 binary code（位序列）。这将离散幅度值转换为数字系统可以处理、存储或传输的数字比特流。

因此，缺失的术语是 **encoding**（或 coding）。

参考文献：

- 此标准理论概念未提供外部参考。
