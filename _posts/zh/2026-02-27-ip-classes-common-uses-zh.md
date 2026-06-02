---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 常用IP分类详解
translated: true
type: note
---

问题：在 IP address 分类中，通常使用地址最左边的一个或多个二进制位来指定网络类型。常用的 IP address classes 有：

A. 3 classes
B. 4 classes
C. 5 classes
D. 6 classes

正确答案是 A，但你选择了 B。请解释错误。

答案：

正确答案是 **A. 3 classes**。

**详细解释：**

传统的 classful IPv4 addressing 将 IP addresses 分为 **five classes** (A, B, C, D, E)，基于地址的前几位：

- **Class A**：0xxxxxxx (first bit = 0) → 1.0.0.0 – 126.255.255.255
- **Class B**：10xxxxxx (first two bits = 10) → 128.0.0.0 – 191.255.255.255
- **Class C**：110xxxxx (first three bits = 110) → 192.0.0.0 – 223.255.255.255
- **Class D**：1110xxxx (first four bits = 1110) → multicast addresses
- **Class E**：1111xxxx (first four bits = 1111) → reserved (experimental)

然而，在实际网络使用和大多数教材/考试（特别是在中国）中，当人们谈到 **"commonly used IP address classes"** 时，通常仅指 **Class A、Class B 和 Class C** — 因为：

- Class D 仅用于 multicast
- Class E 是保留的，不在正常网络中使用

因此，**常用**的 IP address classes 是 **3 classes** (A, B, C)。

这就是为什么正确答案是 **A. 3 classes**。

你的选择 **B. 4 classes** 是错误的，因为虽然技术上总共有 five classes，但问题特别询问 **"commonly used"** classes，并且在大多数教育语境（特别是在像 HCIA、CCNA 入门材料的中国认证考试）中的标准答案是 **3 classes**。

参考资料：

- None (this is standard IPv4 classful addressing knowledge)
