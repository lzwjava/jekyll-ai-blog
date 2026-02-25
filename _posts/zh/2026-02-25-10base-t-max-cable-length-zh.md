---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 10BASE-T 最大电缆长度详解
translated: true
type: note
---

问题：根据 10BASE-T Ethernet 技术规范，HUB 和网络接口卡 (NIC) 之间的最大距离是多少？

A. 20m  
B. 50m  
C. 100m  
D. 200m

答案： 

**C. 100m**

**说明：**

10BASE-T 标准（定义于 IEEE 802.3i-1990）是使用非屏蔽双绞线 (UTP) 布线的 10 Mbps Ethernet 规范——通常为 Category 3 或更高等级——并在物理星型拓扑中运行，中心为 hub（或 repeater）。

10BASE-T 的关键技术参数包括：

- hub（repeater）与网络接口卡 (DTE) 之间的最大电缆长度：**100 meters**
- 使用 RJ-45 连接器
- 电缆中的四对线中使用两对（一对用于发送，一对用于接收）
- 100 米限制包括跳线，是水平布线段的总允许长度

这一 100 米最大段长是 10BASE-T 的基本规则，在原始 IEEE 802.3 标准以及所有后续参考文献中均有一致记载。

因此，正确答案是 **C. 100m**。

其他选项不正确，因为：
- 20m 和 50m 远低于标准允许值
- 200m 超出规范，会导致信号衰减过度和时序问题

参考文献：  

- IEEE 802.3-1990 标准 (10BASE-T 子句)  
- [https://standards.ieee.org/ieee/802.3/1990/](https://standards.ieee.org/ieee/802.3/1990/)