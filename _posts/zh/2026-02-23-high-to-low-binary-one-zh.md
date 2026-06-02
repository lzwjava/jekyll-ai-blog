---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从高到低表示二进制1
translated: true
type: note
---

问题：在 Manchester encoding 中，每个比特持续时间的中间发生电压跃变；从高电压到低电压的跃变代表什么？

答案：

在 **Manchester encoding** 中，数据被编码为每个比特周期的中间总是有一个跃变。这个跃变同时作为时钟信号和数据载波。跃变的方向决定了二进制值：

- 比特周期中间从 **high to low** 电压的跃变代表二进制 **1**。
- 比特周期中间从 **low to high** 电压的跃变代表二进制 **0**。

这种方案确保了发送方和接收方之间的同步，因为每个比特间隔都有保证的活动（跃变），防止长串相同比特导致时钟漂移。它广泛用于 Ethernet（特别是 10BASE-T）和其他通信系统中。

因此，从高到低的跃变表示值 **1**。

参考文献：

- [https://en.wikipedia.org/wiki/Manchester_code](https://en.wikipedia.org/wiki/Manchester_code)
