---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCP 超时与 RTT 估计算法详解
translated: true
type: note
---

这里是组织转录的续集，从上一部分结束的地方精确接续（中途句子：“On the other hand, if we wait too long, TCP...”）。文本尽可能保留 Jim Kurose 的原始口语表达和自然演讲风格，同时结构化为清晰的部分，改进流程、段落分隔，并添加轻微标点以提高可读性。这涵盖了讲座这一部分通常呈现的关键概念的其余部分（基于《Computer Networking: A Top-Down Approach》第8版的的标准覆盖范围和视频内容）。

**设置超时值（续）**

另一方面，如果我们等待太久，TCP 将花费很长时间来检测到一个 segment 实际上已经丢失。所以我们希望将 timeout interval 设置得比 round-trip time 稍长一点，但不要长太多。

问题是：我们如何实际估计 round-trip time 呢？因为 round-trip time 会随时间变化——网络中可能出现拥塞，可能采取不同的路径——所以 RTT 不是一个固定值。

**估计 Round-Trip Time**

TCP 所做的就是维护一个 RTT 的估计值——它称之为 EstimatedRTT。而且它使用一个非常简单的指数加权移动平均来更新 EstimatedRTT。公式是：

EstimatedRTT = (1 − α) × EstimatedRTT + α × SampleRTT

其中 SampleRTT 是最近测量的 round-trip time——即从发送一个 segment 到收到对应的 ACK 的时间——α 通常为 0.125。

所以大部分权重（87.5%）保留在历史值上，只有 12.5% 在新样本上。这意味着 EstimatedRTT 变化缓慢——它对 RTT 的大幅短期波动相对不敏感，这很好，因为我们不希望对单个很长的 RTT 样本过度反应。

**处理 RTT 变化——偏差**

但是即使有这种平滑，我们仍然需要考虑 RTT 可能变化很大的事实。所以 TCP 还跟踪 RTT 样本偏离 EstimatedRTT 的程度。它维护另一个平滑值，称为 DevRTT（RTT deviation），它使用类似的指数加权移动平均来更新：

DevRTT = (1 − β) × DevRTT + β × |SampleRTT − EstimatedRTT|

其中 β 通常为 0.25。

**设置 Timeout Interval**

现在，有了这两个值，TCP 将 timeout interval 设置为：

TimeoutInterval = EstimatedRTT + 4 × DevRTT

为什么是 4？这是一个工程选择。事实证明，4 × DevRTT 提供了一个相当好的平衡：它足够长，大多数 segment 会在定时器到期前被确认（从而避免大量不必要的重传），但仍然足够短，当一个 segment 真正丢失时，我们能合理快速地检测到丢失。

**一个关键问题：模糊的 Round-Trip-Time 样本**

这里有一个非常重要的细节。当我们测量 SampleRTT 时，我们只针对没有被重传的 segment 进行测量。为什么？因为如果我们重传一个 segment，然后收到一个 ACK，我们不知道那个 ACK 是针对原始传输还是重传。如果我们使用那个模糊的样本，我们的 RTT 估计可能会严重出错。

所以 TCP 只从正好发送一次的 segment（没有发生该 segment 的重传）获取 SampleRTT。这被称为 Karn’s algorithm（以其发明者 Phil Karn 命名）。

**TCP 发送方——总体概述**

现在让我们看看 TCP 发送方实际做的事情的全局图景。

发送方有三个主要事件驱动其行为：

1. 从上层应用收到数据 → TCP 创建一个 segment，将其放入发送缓冲区，启动定时器（如果定时器尚未运行），并发送该 segment。
2. 发生 timeout → 发送方重传最旧的未确认 segment，并重新启动定时器。
3. 到达 ACK → 如果它确认了新数据，发送方从发送缓冲区移除该数据。如果仍有未确认数据，则重新启动定时器（针对最旧的未确认 segment）。如果 ACK 是累积的并覆盖更多数据，则可以一次性移除多个 segment。

**TCP 接收方行为**

在接收方，有几个重要规则：

- 当有序 segment 到达时：立即将数据交付给上层应用，发送一个针对下一个期望字节的累积 ACK，但延迟 ACK 最多约 500 ms（希望另一个 segment 很快到达，ACK 可以搭便车于传出数据）。
- 当无序 segment 到达时：缓冲它（TCP 允许缓冲无序数据），并发送一个重复 ACK，指示下一个期望字节（这是给发送方的提示，表示存在间隙）。
- 如果一个 segment 填补了间隙，现在数据有序到新点：将所有缓冲的有序数据交付给上层应用，并发送一个针对新下一个期望字节的累积 ACK。

**Fast Retransmit**

等待 timeout 可能很慢——有时远比必要的时间长。所以 TCP 包含一个非常重要的优化，称为 Fast Retransmit。

规则是：如果发送方连续收到三个重复 ACK，它假设确认字节之后的 segment 已丢失，并立即重传该 segment——而不等待 timeout 到期。

这比等待完整的 timeout interval 快得多。Fast Retransmit 是 TCP 中最重要的性能改进之一。

（注：此视频为 2 部分中的第 1 部分。它通常在 Fast Retransmit 介绍和基本重传场景结束。第 2 部分继续讨论更复杂的丢失场景、selective acknowledgments (SACK)、使用 receive window 的 flow control，以及连接管理的 three-way handshake。）

参考资料：

- [YouTube Video: 3.5-1 TCP Reliability, Flow Control, and Connection Management](https://www.youtube.com/watch?v=UYJP-6mhF6E)
- [Playlist: Computer Networking: A Top-Down Approach - All Chapters](https://www.youtube.com/playlist?list=PLByK_3hwzY3Tysh-SY9MKZhMm9wIfNOas)
