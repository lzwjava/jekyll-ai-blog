---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络拥塞控制原理
translated: true
type: note
---

**整理后的讲稿：3.6 Principles of Congestion Control**  
*(Jim Kurose 讲课，来自 Computer Networking: A Top-Down Approach)*

[Music]

在这一节中，我们将对 congestion control 进行宏观视角——真正寻求对 congestion 的原因和成本的原理性理解。我们将识别两种基本的应对 congestion 的方法。

在下一节中，我们将考察 TCP 以及它如何实际实现这些原则，但现在我们将退后一步，采取宏观视角。所以你可以放下笔和铅笔，坐下来思考、聆听——就像俗话所说，戴上你的思考帽。我想你会真正喜欢的。而且记住，congestion control 确实是计算机网络中的前五大事项，所以请注意。

好吧，让我们从最基本的问题开始：我们所说的 congestion 是什么意思？嗯，非正式地说，congestion 是关于太多来源发送太多 packets 太快，以至于网络中某处的 congested network link 无法处理。

现在记住，links 有 transmission rate，当 packets 的 arrival rate 超过 transmission rate 时，queues 将开始积累，delays 将越来越大。而且如果 link 的 packet buffers 完全填满，到达的 packets 将被 dropped 和 lost。

重要的是要记住，congestion control 真正关乎多个 senders 总体发送太快，而 flow control——我们在上一节中研究的——真正关乎单个 sender 和单个 receiver 之间的 speed matching。

有了这个背景，让我们深入探讨 congestion 的原因和成本。我们将从一个简单的理想化场景开始——你知道，理想化场景是教授们喜欢思考的东西——然后开始添加越来越现实的假设。

所以让我们从这里显示的场景开始。我们将考察单个 router 发生 congestion 的情况。首先假设有无限的 buffering（当然这是理想化的）。router 有容量为 R bits per second 的 input 和 output links，并且有两个 flows：这里显示的 red flow 和 blue flow。

让我们仔细看看与 red flow 相关的 flow rates。在 sending side 有 λ_in——那是 application layer 向下传输到 transport layer 的数据速率。在 receiving side 有 λ_out，我们称之为 throughput——那是数据实际交付到 receiver 处 application layer 的速率。

我们将想问的问题是：当我们在 sending side 拨高 arrival rate 时，throughput 会发生什么，假设我们类似地增加 red 和 blue flows 的 arrival rate？

嗯，在 infinite buffering 的情况下，没有 packets 被 lost——每个发送的 packet 最终都会被 received。所以 receiver 处的 throughput 等于 sender 的 sending rate，如这里的 plot 所示。不过注意 x-axis 在 R/2 结束，因为如果每个 sender 发送速率超过 R/2，throughput 将简单地最大化为每个 flow 的 R/2。那是因为 router 的 input 和 output links 无法承载超过 R bits per second 的 traffic——两个 flows 各 R/2。

嗯，这看起来不错，至少从 throughput 的角度来看。但记住我们在 Chapter 1 中学到，当 link 的 arrival rate 接近 link 的 transmission rate 时，会发生 large queuing delays，如这里所示。所以我们已经看到即使在这个理想化场景中，也存在成本：delay costs。

现在让我们看看当我们放弃关于 infinite buffering 的不现实假设时会发生什么。所以让我们考虑相同的场景，除了现在 buffering 的量将是 finite 的。

回想我们在 reliable data transfer 研究中得知，senders 将在面对由于 buffer overflows 或 corruption 导致的 packet loss 时进行 retransmit。所以现在我们需要更仔细地考察 sending rate。特别是，我们将区分：

- 从 application 向下传递的 original data 的速率——我们记为 λ_in  
- transport layer 发送数据（包括 retransmissions）的总体速率——我们记为 λ_in'（lambda in prime）

packets 到达 router 的速率是 λ_in'，而不是 λ_in。确保你理解了 λ_in 和 λ_in' 之间的区别——这真的很重要。而且如这里所述，λ_in 等于 λ_out，而 λ_in' 将大于或等于 λ_in，因为它包括 retransmissions。

好吧，对于这个 finite buffers 的情况，让我们仍然从一个理想化场景开始，并想象 sender 某种神奇地知道 transmitted packet 是否有 free buffer space。所以在这种情况下，没有 packets 被 lost。source 发送一个 packet，它只是被 router buffer，最终 transmitted，并被 receiver received。在这种情况下没有 packets 被 lost，y-axis 上的 throughput λ_out 等于 λ_in。这里没有问题——嗯，除了当 λ_in 接近 R/2 时 queuing delays，就像我们的第一个场景一样。

所以接下来让我们放松 sender 某种神奇地知道何时有 free buffer space 的假设，并考虑当 packets 到达时如果没有 free buffer space 而在 router 被 lost 时会发生什么。

这里我们看到一个 packet 到达发现 buffers full——它被 lost，因此 sender 最终 retransmit 一个 packet 的 copy，在这种情况下找到 free buffer space，进入 buffer，并最终被 router transmitted 并被 destination received。

在这种情况下，当因为 known loss 而发生 retransmissions 时，显示 overall arrival rate 与 throughput 的 plot 看起来像这样。在 low arrival rate 时，buffers 几乎总是有空的，每个 originally transmitted packet 都会通过。所以在 slow arrival region，包含 retransmissions（实际上不经常发生）的 arrival rate 本质上等于 receiver throughput。overall arrival rate λ_in' 的一个单位增加等于 throughput λ_out 的一个单位增加——也就是说这里 red curve 的 slope 接近一。

更有趣的是这里的 high arrival rate region。这里到达的 packets 越来越多地包括 retransmitted packets，因此 receiver throughput 不再随着 overall arrival rate 的增加而一一增加。而且我们看到随着 x-axis 上的 overall arrival rate 接近 R/2（不能更高），receiver 的 maximum throughput 实际上小于 R/2。这里这个 gap——这一点很重要——是因为 n 个 retransmitted copies of a packet 占用 n 倍 single packet 的 transmission capacity，但最终这些 n 个 packet transmissions 只贡献一个 packet 到 throughput。

嗯，现在让我们看看如果我们放弃所有 retransmissions 实际上都是 needed 的不现实假设会发生什么。也就是说，让我们假设 sender 可能 prematurely timeout，如这里的 example 所示，并实际向 receiver 交付两个 packet copies。

在这个 example 中第一个 packet 被 delayed，因此 sender 最终 timeout 并 retransmit，这两个 packets 最终都到达 receiver。当然 receiver 即使...

*(注：提供的 transcript 摘录在此中途结束。完整视频继续讨论 congestion 的进一步成本，包括 "goodput" collapse 和额外场景。)*

References:  

- [Original Video: 3.6 Principles of Congestion Control](https://www.youtube.com/watch?v=Fm92xvIp6JY)