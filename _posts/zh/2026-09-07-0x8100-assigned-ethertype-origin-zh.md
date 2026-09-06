---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 0x8100：分配的以太类型来源
translated: true
type: note
---

问题：为什么802.1Q中的TPID值是`0x8100`，这个数字从何而来？

答案：

**`0x8100`** 只是一个**被分配的EtherType值**——一个由**IEEE（电气与电子工程师协会）**注册的十六进制唯一标识符，用于在以太网帧中标识特定协议。

---

**理解EtherType：**

每个以太网帧都有一个**EtherType字段**（2字节/16位），用于告知接收设备：
> “这个帧里面装的是什么类型的数据？”

| EtherType | 协议 |
|---|---|
| `0x0800` | IPv4 |
| `0x0806` | ARP |
| `0x86DD` | IPv6 |
| **`0x8100`** | **802.1Q VLAN标签帧** |
| `0x8847` | MPLS |

这些值**并非通过数学推导得出**——它们只是**被保留和注册的编号**，就像区号或国家代码一样。IEEE/IANA作为权威机构负责分配这些值，以避免冲突。

---

**那么为什么偏偏是`0x8100`？**

- 当**20世纪90年代末**开发802.1Q标准时，IEEE需要一个唯一的EtherType来标识“这个帧携带了一个VLAN标签”
- `0x8100`是IEEE**为此目的分配**的值——当时它在EtherType注册表中是一个可用的空位
- 没有更深层的数学含义——这纯粹是一个**行政分配**

---

**实际工作原理：**

```
普通以太网帧：
[ 目标MAC | 源MAC | EtherType(0x0800) | IP载荷 ]

802.1Q标签帧：
[ 目标MAC | 源MAC | 0x8100 | PCP+DEI+VID | EtherType(0x0800) | IP载荷 ]
                       ↑
              "嘿！后面跟着一个VLAN标签！"
```

当交换机看到`0x8100`时，它知道接下来的2字节是VLAN标签（PCP + DEI + VID），而不是载荷数据。标签之后，**原始的EtherType**（例如IP的`0x0800`）恢复正常。

---

**简而言之：** `0x8100`没有特殊的数学起源——它只是IEEE在创建标准时正式注册并分配给802.1Q的唯一ID，就像产品获得一个条形码一样。

参考文献：
- [EtherType - 维基百科](https://en.wikipedia.org/wiki/EtherType)
- [IEEE注册机构 - EtherType](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries)
- [IEEE 802.1Q帧格式](https://en.wikipedia.org/wiki/IEEE_802.1Q#Frame_format)