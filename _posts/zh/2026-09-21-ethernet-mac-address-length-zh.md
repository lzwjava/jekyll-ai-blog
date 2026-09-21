---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 以太网MAC地址长度
translated: true
type: note
---

问题：在以太网MAC帧中，源地址和目标地址都是48位吗？

答案：**是的——对于标准以太网，两者都是48位（6字节）的MAC地址。**

```text
Ethernet II 帧
┌──────────────┬──────────────┬────────────┬───────────────┐
│ 目标MAC      │ 源MAC        │ EtherType  │ 负载 ...      │
│ 48位         │ 48位         │ 16位       │ 46–1500字节   │
└──────────────┴──────────────┴────────────┴───────────────┘
     6字节         6字节         2字节
```

示例：

```text
dst = ff:ff:ff:ff:ff:ff    # 广播
src = 3c:22:fb:12:34:56    # 单播
```

因此，一个MAC地址是：

```text
48位 = 6字节 = 12个十六进制数字
```

一个细微之处：**48位是标准以太网MAC地址的大小，但并非每个MAC层协议/寻址方案都一定是48位。**以太网在常见情况下使用的是48位MAC地址。

参考资料：

* [IEEE 802.3 Ethernet](https://standards.ieee.org/ieee/802.3/10422/)
* [RFC 7042 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802](https://www.rfc-editor.org/rfc/rfc7042)

我还可以逐步分析一个实际的以太网帧，包括前导码、FCS、EtherType以及IP/TCP报头所在的位置。
