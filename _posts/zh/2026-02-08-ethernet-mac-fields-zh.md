---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: 以太网 MAC 地址字段大小
translated: true
type: note
---

这个问题询问的是 IEEE 802.3 MAC frame 中地址字段的大小。

## 正确答案：**C (48 bits)**

### 解析：

在 IEEE 802.3 (Ethernet) MAC frame 结构中，**destination address (DA)** 和 **source address (SA)** 均为 **48 bits** 长，相当于 **6 bytes**。

这种 48-bit 地址也称为 **MAC address** 或 **physical address**，通常以冒号或连字符分隔的十六进制表示，例如：`00:1A:2B:3C:4D:5E`。

### 为什么是 48 bits？

- **前 24 bits (3 bytes)**：Organizationally Unique Identifier (OUI) - 用于标识制造商。
- **后 24 bits (3 bytes)**：由制造商分配的设备特定标识符。

### 为什么你的答案 (B - 32 bits) 是错误的：

32 bits 仅有 4 bytes，不足以在不同制造商和网络中唯一标识设备。为了容纳现代网络中海量的设备，同时保持高效网络管理所需的层级结构，48-bit 地址空间是必不可少的。

自 Ethernet 首次标准化以来，48-bit MAC address 一直是标准，并沿用至今。