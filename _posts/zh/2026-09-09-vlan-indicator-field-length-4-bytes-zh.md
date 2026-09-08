---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VLAN指示字段长度：4字节
translated: true
type: note
---

问题：在VLAN帧（802.1Q）中，VLAN指示字段的长度是多少？

答案：

在IEEE 802.1Q VLAN标记以太网帧中，VLAN标签总长度为**4字节（32位）**，插入在源MAC地址和EtherType/长度字段之间。其结构分解如下：

| 字段 | 大小 | 描述 |
| --- | --- | --- |
| **TPID**（标签协议标识符） | 16位 | 固定为`0x8100`，表示VLAN帧 |
| **TCI**（标签控制信息） | 16位 | 包含PCP（3位）+ DEI（1位）+ **VLAN ID（12位）** |

**VLAN ID（VID）** 本身为**12位**，可支持**4,096个可能的VLAN**（0–4095），但实际使用中0和4095被保留。

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        TPID = 0x8100          |PCP|D|        VLAN ID          |
|           (16位)              |(3位)|I|       (12位)           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                        ← 共4字节 →
```

参考资料：

- [IEEE 802.1Q - 维基百科](https://en.wikipedia.org/wiki/IEEE_802.1Q)
- [IEEE 802.1Q 标准](https://standards.ieee.org/ieee/802.1Q/10673/)
