---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么MAC地址是48位
translated: true
type: note
---

**问题：** 为什么 IEEE 802.3 MAC 帧结构中的源地址和目的地址都是 48 位（6 字节）？

**答案：**

在 IEEE 802.3（以太网）MAC 帧结构中，**目的地址（DA）** 和 **源地址（SA）** 均为 **48 位（6 字节）**。原因如下：

**MAC 地址标准**
IEEE 将 MAC 地址标准化为 48 位值。该标准定义于 IEEE 802 中，并普遍应用于以太网、Wi-Fi、蓝牙等。

**48 位 MAC 地址结构**

```
| OUI（24 位）  | NIC 特定（24 位） |
  组织唯一标识符      设备标识符
```

- 前 3 字节 → 由 IEEE 分配给制造商
- 后 3 字节 → 由制造商分配给每台设备

**为什么其他选项不正确？**

| 选项 | 位数 | 错误原因 |
| ------ | ------ | ---------- |
| A – 16 位 | 2 字节 | 过小；仅约 65,536 个唯一地址 |
| **C – 48 位** | **6 字节** | **正确——IEEE 802 标准** |
| B – 32 位 | 4 字节 | 这是 IPv4 地址长度，非 MAC 地址 |
| D – 96 位 | 12 字节 | 相当于两个 MAC 地址组合 |

**记忆技巧：** MAC 地址通常写作 6 组十六进制数，例如 `AA:BB:CC:DD:EE:FF` —— 6 字节 = 48 位。

参考：

- [IEEE 802.3 以太网标准](https://standards.ieee.org/ieee/802.3/7071/)
- [MAC 地址 – 维基百科](https://en.wikipedia.org/wiki/MAC_address)
