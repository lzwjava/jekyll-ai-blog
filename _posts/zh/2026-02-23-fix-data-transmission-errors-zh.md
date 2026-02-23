---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 冗余修复数据传输错误
translated: true
type: note
---

问题：简要描述 error-correcting coding 的基本原理。

答案：

**error-correcting coding**（也称为 channel coding）的基本原理是通过引入受控冗余来增强在噪声信道上数据传输的可靠性。该过程涉及以下关键步骤：

1.  **Addition of Redundancy**：在发送端，根据预定义的数学规则或算法，向原始数据位添加特定的冗余位（check bits）。这些冗余位不携带新信息，而是与数据位建立特定的逻辑关系或约束。
2.  **Transmission**：原始数据位和冗余位的组合序列通过通信信道传输。
3.  **Detection and Correction**：在接收端，使用相同的预定义规则检查输入比特流。
    *   **Error Detection**：接收端验证数据位与冗余位之间的关系是否成立。如果关系被违反，则表明传输过程中发生了错误。
    *   **Error Correction**：在更高级的码（Forward Error Correction - FEC）中，违反模式的特定图案允许接收端不仅检测到错误的存在，还能自动定位和纠正它们，而无需重传。

本质上，error coding 通过发送额外位来牺牲传输效率，以换取更高的可靠性，从而使系统能够检测并通常纠正由噪声、干扰或信号衰减引起的错误。

参考文献：