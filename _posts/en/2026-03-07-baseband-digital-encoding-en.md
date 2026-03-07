---
audio: false
generated: true
image: false
lang: en
layout: post
title: Baseband Digital Data Encoding
translated: false
type: note
---

**Question:** What type of encoding transforms raw binary data into a digital pulse sequence to achieve baseband transmission?

**Answer:**

The answer is **数字数据编码 (Digital Data Encoding)**.

---

## Explanation

### Core Concept

**Baseband transmission (基带传输)** refers to transmitting digital signals directly over a channel in their original pulse waveform form, without carrier modulation. Baseband transmission sends digital signals in their original waveform (in pulse form) directly over the channel, requiring the channel to have a relatively wide passband. It does not require modulation/demodulation, making it cost-effective and suitable for shorter-range data transmission.

### What is Digital Data Encoding?

**Digital Data Encoding (数字数据编码)** is the process of converting raw binary data (原始的二进制数据) into a specific digital pulse sequence (数字脉冲序列) suitable for transmission over a baseband channel. Digital baseband signals represent digital information using electrical pulses. The form in which digital information is represented by electrical pulses is called a **line code (码型)**. Different code patterns have different spectral structures; to obtain good transmission characteristics in a channel, the baseband signal's code type must be carefully selected so that digital information is transformed into a spectral structure suited to the given channel's transmission characteristics.

### Why Encoding is Necessary

Raw binary data (0s and 1s) cannot always be transmitted directly because:
- The raw signal may contain DC components that are unsuitable for transmission.
- Clock synchronization cannot be guaranteed without proper encoding.
- Noise immunity may be poor.

### Common Digital Data Encoding Methods for Baseband Transmission

Common encoding methods used in baseband transmission include three main approaches: **Non-Return-to-Zero (NRZ)**, **Manchester Encoding**, and **Differential Manchester Encoding**. The latter two contain no DC component and include clock pulses for self-synchronization, making them widely used.

Here is a summary of the main types:

| Encoding Type | Chinese Name | Key Feature |
|---|---|---|
| NRZ (Non-Return-to-Zero) | 不归零码 | Simple, but no self-clocking |
| Manchester Encoding | 曼彻斯特编码 | Mid-bit transition; self-clocking; used in Ethernet |
| Differential Manchester | 差分曼彻斯特编码 | Transition at bit boundary indicates 0; used in Token Ring LANs |
| AMI (Alternate Mark Inversion) | 交替极性反转码 | No DC component; alternating +/− for 1s |
| HDB3 | 高密度双极性3码 | Improved AMI; limits consecutive zeros to 3 |

Manchester encoding is a self-clocking encoding method that uses voltage transitions to represent 0 or 1. A transition from high to low represents "0," and from low to high represents "1." Manchester code occupies twice the bandwidth of NRZ encoding, with an efficiency of 50%.

### Summary

The method of **transforming raw binary data into a digital pulse sequence for baseband transmission** is called **数字数据编码 (Digital Data Encoding)**. This encoding step is essential before any baseband transmission can occur, ensuring the signal is compatible with the physical channel's characteristics and enabling proper clock recovery and error detection at the receiver.

---

**References:**

- [数字基带传输系统 - 知乎](https://zhuanlan.zhihu.com/p/493951684)
- [计算机网络基础 — 数字基带传输常见码型 - CSDN](https://blog.csdn.net/acslsr/article/details/109318214)
- [基带传输、频带传输、宽带传输的概念及应用 - 博客园](https://www.cnblogs.com/youngforever/articles/3273375.html)
- [数字基带信号编码 - CSDN](https://blog.csdn.net/XiaoxiLi_YMYG/article/details/77839698)
- [数字信号的基带传输 - QQ阅读](https://m.fwdbook.qq.com/read/1000677112/12)