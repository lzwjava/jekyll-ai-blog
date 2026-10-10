---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 1000BASE-T传输介质
translated: true
type: note
---

**问题：** 1000BASE-T 使用的传输介质是什么？

**答案：**

**1000BASE-T**（在 IEEE 802.3ab 中定义）使用 **双绞铜缆** 作为其传输介质——具体如下：

| 属性 | 详情 |
|---|---|
| **介质** | 非屏蔽双绞线（UTP）铜线 |
| **最低线缆等级** | Cat 5e（超五类）或更高（Cat 6、Cat 6a 亦可） |
| **使用线对** | 同时使用全部 **4 对**（8 根线） |
| **最大段长度** | 100 米（328 英尺） |
| **速度** | 1 Gbps（千兆以太网） |
| **信令** | 全双工，每对线采用 PAM-5 编码 |

与早期标准（例如 100BASE-TX 仅使用 2 对线）不同，1000BASE-T 利用全部 4 对线 **同时双向传输**，这就是它在普通铜缆上实现千兆速度的方式。

**参考资料：**
- [IEEE 802.3ab – 维基百科](https://en.wikipedia.org/wiki/IEEE_802.3ab)
- [1000BASE-T – 以太网联盟](https://ethernettechnology.net/gigabit-ethernet/)