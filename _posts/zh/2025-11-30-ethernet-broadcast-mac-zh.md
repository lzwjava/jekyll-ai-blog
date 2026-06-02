---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 以太网广播媒体访问控制地址
translated: true
type: note
---

正确答案是 **B) FFFF.FFFF.FFFF**

### 解析

在以太网中，**广播帧**会被发送到同一本地网段的所有设备（二层广播）。

- 以太网广播帧的目标MAC地址为十六进制形式的**全1地址**：**FF-FF-FF-FF-FF-FF**（常写作**FFFF.FFFF.FFFF**）。
- 这是以太网标准中定义的保留广播MAC地址。

### 其他选项错误原因

- **A) 0000.0000.0000** → 这是无效或空MAC地址（特殊情况下可能作为源地址，但从不用于广播）。
- **C) 0100.5E00.0000** → 这是IPv4组播MAC地址的基础地址（非广播地址）。
- **D) 默认网关的MAC地址** → 这将构成单播帧，而非广播帧。

**正确答案：B) FFFF.FFFF.FFFF**
