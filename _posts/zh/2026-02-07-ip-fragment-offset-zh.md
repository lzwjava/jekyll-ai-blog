---
audio: false
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: IP 数据报中的片偏移单位
translated: true
type: note
---

**IP datagram** 结构固定部分中 **Fragment Offset** 字段的单位是 **8 bytes (B)**。

### Explanation

- **Fragment Offset** 字段表示当前分片相对于原始 IP datagram 起始位置的偏移。
- 由于 IP datagram 的分片长度必须是 8 bytes 的倍数，因此 **Fragment Offset** 以 8 bytes 为单位进行测量。
- **Fragment Offset** 的值乘以 8 即可得到以 bytes 为单位的实际偏移量。

### Analysis of Options

- **A. 1B**: 错误，单位不是 1 byte。
- **B. 8B**: 正确，单位是 8 bytes。
- **C. 16B**: 错误，单位不是 16 bytes。
- **D. 32B**: 错误，单位不是 32 bytes。

因此，**正确答案是 B**。
