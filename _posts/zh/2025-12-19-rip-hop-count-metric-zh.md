---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: RIP 使用跳数度量
translated: true
type: note
---

问题：哪种路由协议使用跳数作为其度量标准？
A) OSPF
B) RIP
C) BGP
D) EIGRP

答案：

正确答案是 **B) RIP**。

- **RIP (Routing Information Protocol)**：使用跳数（数据包必须经过的路由器数量）作为其主要也是唯一的度量标准。最大跳数为15，16则表示网络不可达。
- **OSPF (Open Shortest Path First)**：使用开销，主要基于带宽（累计接口开销），而非跳数。
- **BGP (Border Gateway Protocol)**：使用路径属性，如ASPATH长度、本地优先级等；跳数不是其度量标准。
- **EIGRP (Enhanced Interior Gateway Routing Protocol)**：使用基于带宽、延迟、负载、可靠性和MTU的复合度量标准（尽管带宽和延迟是主要因素）；它不单单依赖跳数。

RIP是经典的距离矢量协议，专为小型网络设计，侧重于简单性（跳数），而非更精确的度量标准，如带宽。
