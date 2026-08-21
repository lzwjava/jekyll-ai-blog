---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 以太网扩展设备层分类
translated: true
type: note
---

问题：关于以太网扩展的问题答案是否正确——物理层扩展使用中继器和集线器，而数据链路层扩展使用网桥和交换机？

答案：是的，正确。

分类如下：

**物理层（第1层）：** 中继器和**集线器**——这些设备仅会重新生成或广播信号，不涉及任何MAC地址或帧的识别。

**数据链路层（第2层）：** 网桥和**交换机**——这些设备基于MAC地址做出转发决策，在帧级别进行操作。

因此答案 **A（集线器）** 正确。集线器与中继器一样，纯粹在物理层工作——它们放大信号并将其重新传输到所有端口，对所携带的数据没有任何智能处理。

参考资料：
- [Ethernet Hub - Wikipedia](https://en.wikipedia.org/wiki/Ethernet_hub)
- [Network Repeater - Wikipedia](https://en.wikipedia.org/wiki/Repeater)