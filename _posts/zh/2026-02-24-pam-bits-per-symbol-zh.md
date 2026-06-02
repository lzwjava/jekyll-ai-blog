---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PAM 每符号比特数计算
translated: true
type: note
---

问题：在使用 8 个 phases 和每个 phase 2 个 amplitude values 的 Phase-Amplitude Modulation (PAM) 系统中，一个 single signal symbol 可以表示多少 binary bits？

答案：

### 分析与计算

要确定单个信号符号（baud）可以表示的 binary bits 数，我们需要计算该调制方案中可用的总 distinct states 数。

1.  **识别参数：**
    *   相位数 ($N_{phase}$) = 8
    *   每个相位的幅度值数 ($N_{amp}$) = 2

2.  **计算总 distinct states 数 ($M$）：**
    总 unique combinations 数是相位数和幅度数的乘积。
    $$M = N_{phase} \times N_{amp}$$
    $$M = 8 \times 2 = 16$$
    共有 16 个 distinct signal states。

3.  **计算每个 symbol 的 bits 数 ($n$）：**
    一个 symbol 表示的 bits 数是总 states 数的 base-2 对数。
    $$n = \log_2(M)$$
    $$n = \log_2(16)$$
    由于 $2^4 = 16$：
    $$n = 4$$

### 结论

每个 signal symbol 可以表示 **4** 个 binary bits。

因此，正确选项是 **C**。
