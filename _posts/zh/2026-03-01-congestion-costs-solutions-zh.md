---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 拥塞控制成本与解决方案
translated: true
type: note
---

**整理字幕：3.6 Principles of Congestion Control (continued)**
*(Jim Kurose 讲课，摘自 Computer Networking: A Top-Down Approach)*

……即使收到了两个副本。所以这里就是不必要的重传情况——有时称为“spurious retransmissions”或“premature timeouts”。

在这种情况下，throughput (goodput)——将有用数据传递给应用层的速率——实际上小于原始数据的到达速率，因为部分带宽被浪费在接收方丢弃的重复数据包上。

现在让我们把这些部分组合起来，看看 offered load（所有发送方原始数据的总到达速率）与 goodput（传递给接收方的有用数据的总吞吐量）之间的整体关系。

当 offered load 较小时，几乎没有数据包丢失，几乎没有重传发生，goodput 与 offered load 线性增长——斜率接近 1。随着 offered load 增加，我们开始看到偶发的缓冲区溢出，需要一些重传，goodput 仍然增加，但斜率小于 1。最终，随着 offered load 继续增加，需要越来越多的重传，其中许多携带重复数据。路由器越来越多地将传输容量用于发送和重发相同的数据包，而 goodput 实际上开始下降，即使 offered load 仍在增加。

在非常高的 offered load 下，链路容量的绝大部分用于发送先前已成功交付的数据包的重复副本。在极端情况下，goodput 可以接近零——这有时称为“congestion collapse”。

这个图是网络领域最著名的图之一：它显示了拥塞崩溃的“knee”和“cliff”。关键点是，一旦 offered load 超过网络无损承载的容量（大致是队列开始显著积压的点），goodput 就停止增加，并最终急剧下降。这是没有有效拥塞控制时拥塞的基本成本。

所以我们现在已经看到了拥塞的几个成本：

1. 大型排队延迟（即使有无限缓冲区）
2. 需要重传的数据包丢失（有限缓冲区）
3. 由于 premature timeouts 导致的重复数据包浪费带宽
4. Goodput 崩溃——在极端情况下，网络吞吐量接近零，而 offered load 很高

这些观察结果引出了拥塞控制的两种广泛方法：

**End-to-end congestion control**
网络不向发送方提供关于拥塞的明确反馈。发送方必须从自己的观察中推断拥塞——通常是 packet loss 和/或延迟增加。TCP 采用这种方法。

**Network-assisted congestion control**
网络向发送方提供关于拥塞的明确反馈。这种反馈有两种形式：

- 来自拥塞路由器向发送方的直接通知（“backwards” explicit congestion notification）
- 路由器在向前发送到接收方的数据包中标记或设置一个位，然后接收方将此信息反馈给发送方（“forward” explicit congestion notification）

Network-assisted 方法的例子包括 DECbit（20 世纪 80 年代早期）、IP 中的 Explicit Congestion Notification (ECN)，以及各种 ATM ABR 方案。

在下一个视频/部分的讲解中，我们将看到 TCP 如何将 end-to-end 方法与几个具体机制（slow start、congestion avoidance、fast retransmit、fast recovery）结合，在实践中实现拥塞控制——而无需网络层的任何帮助。

这就结束了拥塞控制的高级原理。我们已经看到了原因、成本，以及应对它的两种基本理念。

[Music]

*(3.6 节结束)*

References:

- [Original Video: 3.6 Principles of Congestion Control](https://www.youtube.com/watch?v=Fm92xvIp6JY)
