---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCP 可靠性、流量控制与连接基础
translated: true
type: note
---

以下是来自 Jim Kurose 的视频“3.5-1 TCP Reliability, Flow Control, and Connection Management”（Part 1）的可用转录的整理和清理版本。原始口语文本尽可能保留（包括轻微重复和自然语流），但已格式化为连贯段落，删除了原始提取中的多余间距/伪影，并添加了少量标点以提高可读性。这涵盖了可用来源中捕获的讲座部分（视频似乎更长，但这是提取的内容）。

**TCP 可靠数据传输简介**

在本节中，我们将看看 TCP 如何提供可靠的数据传输。我们将看到 TCP 使用了我们之前研究的所有机制：checksums、acknowledgments、sequence numbers、timeout 和 retransmit，以及 pipelining。我们还将看看 TCP 如何估计发送方和接收方之间的往返时间（round-trip time），以及它如何使用该时间来设置 timeout interval。我们还将检查一些 TCP 场景，观察 TCP 发送方和接收方在行动中。那么让我们开始吧。

**TCP 概述和语义**

正如我们所见，TCP 以点对点方式运行——即一个发送方和一个接收方之间。其可靠数据传输的语义是 in-order byte stream。我们应该将其与 UDP 对比，UDP 是 message-oriented。TCP 实现的是可靠的 byte stream 抽象。

TCP 也是 full duplex 的，这意味着数据负载可以双向流动。TCP segment 中作为 payload 包含的数据有一个 maximum segment size (MSS)，实际中通常是 1460 bytes，但可能有各种不同的值，我们稍后会说明。

TCP 使用 cumulative ACKs，并且是一个 Go-Back-N pipelined protocol。它也是 connection-oriented 的，这意味着在数据实际开始流动之前，发送方和接收方之间会发生 handshake。我们稍后将看看该 handshake 过程。

TCP 还实现了 flow control，这意味着发送方和接收方的速度是匹配的，从而发送方不会用数据淹没接收方。

**TCP Segment 结构**

接下来让我们看看 TCP segment 结构。我知道这可能看起来有点无聊——这里有很多字段——所以可能有点枯燥。但要记住，关键不是这些字段是什么，而是为什么要有这些字段。在所有这些情况下，我们将从之前学到的可靠数据传输原则中看到，为什么 TCP 有这些字段。

我们之前见过 source port number 和 destination port number 用于 multiplexing 和 demultiplexing。TCP header 还包含 32 位 sequence number 和 32 位 acknowledgement number，我们马上就会详细查看。

在底部我们看到 application data——那是 TCP segment 携带的 payload。TCP header 还有一个 Internet checksum，就像我们在 UDP 中看到的那样。

TCP 还有一组 options，可以包含可变数量的 options。我们不会深入这些，但这使得我们看到的 header 长度可变，从而可以在 TCP header 中携带 options。因为 header 长度可变，我们需要在 TCP header 本身有一个 length field。

reset、SYN 和 FIN 位用于 connection management——我们稍后会研究。还有一个 header 字段用于 flow control，接收方可以告诉发送方它愿意接受的字节数。

header 中有两个位用于 congestion notification，我们稍后会查看。最后，有一个字段——urgent field——中的两个位，在实践中并没有真正使用。

**Sequence Numbers 和 Acknowledgement Numbers**

让我们深入探讨一下 TCP sequence number 和 acknowledgement number 字段的含义。请记住，TCP 实现的是 byte stream 抽象，TCP segment header 中携带的 sequence number 表示该 segment payload 数据中第一个字节的 byte stream 编号。

acknowledgement field 由接收方用于告诉发送方下一个期望从发送方接收的字节的 sequence number。该数字作为该 sequence number 之前所有数据字节的 cumulative acknowledgment。

最后，学生们经常问：TCP 接收方应该如何处理 out-of-order segments？TCP 规范在这里没有要求——这取决于实现者。

**简单示例：Telnet 场景**

接下来让我们看看一个非常简单的 TCP 行动示例，观察 sequence numbers 和 acknowledgement numbers。在这个示例中，我们看一个简单的 telnet 场景，其中 host A 向 host B 发送一个字符，host B 将该单个字符回显回去。

你需要仔细查看示例中显示的 segment 上的 sequence 和 ACK numbers。这里要注明的关键是，B-to-A segment 上的 ACK number 43 比触发该 acknowledgment 的 A-to-B segment 上的 sequence number 42 多 1。类似地，最后一个 A-to-B segment 上的 ACK number 80 比触发该 acknowledgment 的 B-to-A segment 上的 sequence number 79 多 1。

**Sequence 和 ACK 用法总结**

嗯，我们看到 TCP 使用 sequence numbers 和 acknowledgments 几乎就像我们从原则性研究中预料的那样。我们看到有几个不同点：byte stream 语义，以及 sequence numbers 和 acknowledgments 对应于该 byte stream 中的偏移量。

**设置 Timeout 值**

接下来让我们看看一个我们还没有解决的问题，那就是：timeout 值应该如何设置？现在让我们看看 TCP 是如何做的。

显然，我们希望 timer 值以某种方式取决于往返时间 (RTT)。但我们如何实际设置该 timer 值？如果设置得太短，会发生 premature timeouts——这意味着我们会重传尚未丢失的 segments。另一方面，如果等待太久，TCP...

（注：可用转录在此句中途中断。完整视频继续讨论 RTT estimation、使用 EstimatedRTT 和 DevRTT 的 timeout 计算、retransmission 场景等。）

参考文献：  

- [YouTube Video: 3.5-1 TCP Reliability, Flow Control, and Connection Management](https://www.youtube.com/watch?v=UYJP-6mhF6E)
- [Playlist: Computer Networking: A Top-Down Approach - All Chapters](https://www.youtube.com/playlist?list=PLByK_3hwzY3Tysh-SY9MKZhMm9wIfNOas)