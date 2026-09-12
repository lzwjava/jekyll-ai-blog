---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IPv6基本报头长度40字节
translated: true
type: note
---

问题：IPv6基本首部的长度是多少？

答案：IPv6基本首部的**固定长度为40字节（320比特）**。

与IPv4可变长度的首部不同，IPv6采用固定大小的基本首部，使路由器的处理效率更高。

40字节的首部包含以下字段：

| 字段 | 大小 |
| --- | --- |
| 版本号 | 4比特 |
| 流量类别 | 8比特 |
| 流标签 | 20比特 |
| 有效载荷长度 | 16比特 |
| 下一个首部 | 8比特 |
| 跳数限制 | 8比特 |
| 源地址 | 128比特 |
| 目的地址 | 128比特 |
| **总计** | **320比特 = 40字节** |

参考资料：

- [RFC 8200 – 互联网协议第6版（IPv6）规范](https://datatracker.ietf.org/doc/html/rfc8200#section-3)
- [IPv6 – 维基百科](https://en.wikipedia.org/wiki/IPv6_packet#Fixed_header)
