---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 以太网物理层和数据链路层扩展
translated: true
type: note
---

问题：关于以太网扩展的问题，物理层扩展使用中继器和集线器，而数据链路层扩展使用网桥和交换机——这个答案正确吗？

答案：是的，正确。

分类如下：

**物理层（第1层）：** 中继器和 **集线器** —— 这些设备仅负责再生或广播信号，不识别MAC地址或帧。

**数据链路层（第2层）：** 网桥和 **交换机** —— 这些设备基于MAC地址做出转发决策，在帧级别上工作。

因此，答案 **A（集线器）** 是正确的。集线器与中继器一样，纯粹在物理层工作——它们将信号放大并转发到所有端口，不关心所承载的数据内容。

参考：

- [以太网集线器 - 维基百科](https://en.wikipedia.org/wiki/Ethernet_hub)
- [网络中继器 - 维基百科](https://en.wikipedia.org/wiki/Repeater)
