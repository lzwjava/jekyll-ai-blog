---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基带数字数据编码
translated: true
type: note
---

**问题：** 将原始二进制数据转换为数字脉冲序列以实现 baseband transmission 的编码类型是什么？

**答案：**

答案是 **数字数据编码 (Digital Data Encoding)**。

---

## 解释

### 核心概念

**Baseband transmission (基带传输)** 是指以原始脉冲波形形式直接在信道上传输数字信号，而不进行载波调制。基带传输将数字信号以其原始波形（脉冲形式）直接发送到信道上，要求信道具有相对较宽的通带。它不需要调制/解调，成本低廉，适用于较短距离的数据传输。

### 什么是 Digital Data Encoding？

**Digital Data Encoding (数字数据编码)** 是将原始二进制数据（raw binary data）转换为适合在基带信道上传输的特定数字脉冲序列（digital pulse sequence）的过程。数字基带信号使用电脉冲表示数字信息。数字信息由电脉冲表示的形式称为 **line code (码型)**。不同的码型具有不同的频谱结构；为了在信道中获得良好的传输特性，必须仔细选择基带信号的码型，使数字信息转换为适合给定信道传输特性的频谱结构。

### 为什么需要编码

原始二进制数据（0 和 1）不能总是直接传输，因为：
- 原始信号可能包含不适合传输的 DC 成分。
- 没有适当编码，无法保证时钟同步。
- 抗噪能力可能较差。

### 基带传输的常见 Digital Data Encoding 方法

基带传输中常用的编码方法包括三种主要方式：**Non-Return-to-Zero (NRZ)**、**Manchester Encoding** 和 **Differential Manchester Encoding**。后两种不含 DC 成分，并包含时钟脉冲以实现自同步，因此应用广泛。

以下是主要类型的总结：

| Encoding Type | Chinese Name | Key Feature |
|---|---|---|
| NRZ (Non-Return-to-Zero) | 不归零码 | 简单，但无自时钟 |
| Manchester Encoding | 曼彻斯特编码 | 位中跳变；自时钟；用于 Ethernet |
| Differential Manchester | 差分曼彻斯特编码 | 位边界跳变表示 0；用于 Token Ring LANs |
| AMI (Alternate Mark Inversion) | 交替极性反转码 | 无 DC 成分；1 使用交替 +/- |
| HDB3 | 高密度双极性3码 | 改进的 AMI；将连续 0 限制为 3 个 |

Manchester encoding 是一种自时钟编码方法，使用电压跳变表示 0 或 1。从高到低跳变表示“0”，从低到高跳变表示“1”。Manchester code 占用 NRZ encoding 两倍的带宽，效率为 50%。

### 总结

将 **原始二进制数据转换为数字脉冲序列以实现基带传输** 的方法称为 **数字数据编码 (Digital Data Encoding)**。这一编码步骤是基带传输发生前的必需步骤，确保信号与物理信道特性兼容，并在接收端实现正确的时钟恢复和错误检测。

---

**参考文献：**

- [数字基带传输系统 - 知乎](https://zhuanlan.zhihu.com/p/493951684)
- [计算机网络基础 — 数字基带传输常见码型 - CSDN](https://blog.csdn.net/acslsr/article/details/109318214)
- [基带传输、频带传输、宽带传输的概念及应用 - 博客园](https://www.cnblogs.com/youngforever/articles/3273375.html)
- [数字基带信号编码 - CSDN](https://blog.csdn.net/XiaoxiLi_YMYG/article/details/77839698)
- [数字信号的基带传输 - QQ阅读](https://m.fwdbook.qq.com/read/1000677112/12)
