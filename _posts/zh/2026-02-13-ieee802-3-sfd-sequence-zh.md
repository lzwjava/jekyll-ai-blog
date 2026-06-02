---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: IEEE 802.3 SFD 序列详解
translated: true
type: note
---

问题：在 IEEE 802.3 标准中，MAC frame 中的 Start Frame Delimiter (SFD) 字段序列是什么？

A. 10101011 (left=LSB, right=MSB)
B. 11010101 (left=LSB, right=MSB)
C. 01111110 (left=LSB, right=MSB)
D. 01111111 (left=LSB, right=MSB)

答案：

正确答案是 **A. 10101011**（从左到右读取，即从 LSB 到 MSB）。

**详细解释：**

在 IEEE 802.3 (Ethernet) 中，frame 结构包括：

- **Preamble**: 7 bytes 的 10101010 … 10101010
- **Start Frame Delimiter (SFD)**: 1 byte = **10101011**

这构成了完整的 8-byte 同步序列：
10101010 10101010 10101010 10101010 10101010 10101010 10101010 **10101011**

将最后一个 byte 从 10101010 更改为 10101011 的目的是提供一个清晰、明确的指示，表明 frame data 即将开始（打破了重复的 1010 模式）。

关键点：
- IEEE 802.3 使用 **10101011** 作为 SFD。
- 这与 Ethernet V2 (DIX Ethernet) 不同，后者虽然也使用 10101011，但拥有 8-byte 全为 10101010 的 preamble。
- IEEE 802.3 选择 10101011 也是为了提高与 IEEE 802.4 (Token Bus) 和 IEEE 802.5 (Token Ring) frame 格式的兼容性/可区分性。

你选择的是 B (11010101)，这是错误的。
11010101 在 IEEE 802.3 Ethernet 中不被用作 SFD。

正确答案：**A**

参考资料：

- IEEE 802.3 standard (Clause 4 - MAC frame format)
- [https://standards.ieee.org/ieee/802.3/2022/](https://standards.ieee.org/ieee/802.3/) (官方 IEEE 802.3 标准文档)
