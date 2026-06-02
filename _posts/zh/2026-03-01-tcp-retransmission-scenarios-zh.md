---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCP 重传场景详解
translated: true
type: note
---

以下是 Jim Kurose 讲座组织化转录的下一个延续部分。与之前一样，尽量忠实保留原始口语表达（包括自然措辞、强调重复和讲座式表达），同时结构化为清晰的部分，使用段落分隔和轻微标点以提高连贯性。本节紧接 Fast Retransmit 介绍之后，进入 retransmission 示例和场景，这些构成了 Part 1 下半部分的主体。

**Retransmission 场景 — 展示 TCP 的实际运作**

现在让我们看一些具体场景，来观察当事情出错时——segment 丢失、ACK 丢失或 timeout 过早发生——TCP sender 和 receiver 如何共同行为。

**场景 1：简单 Timeout 和 Retransmission**

假设 sender 发送 segment 1（sequence number 1000，500 bytes 数据）。timer 开始计时。
该 segment 丢失——从未到达 receiver。
timeout 间隔到期后，sender retransmit segment 1（相同 sequence number 1000）。
这次 segment 到达，receiver 发送回 ACK，表示“next expected byte 是 1500”（cumulative ACK）。
sender 收到该 ACK，从 send buffer 中移除数据，一切正常继续。

这是我们已经了解的基本 Go-Back-N 风格 recovery。

**场景 2：ACK 丢失**

Sender 发送 segment 1（seq=1000，500 bytes）。
Receiver 收到，发送 ACK 1500。
但该 ACK 在返回途中丢失。
Sender 的 timer 最终到期 → sender retransmit segment 1。
Receiver 收到 duplicate segment 1。因为它已经将 bytes 1000–1499 交付给 application，并期待 1500，它简单丢弃数据（但仍发送另一个 cumulative ACK 1500）。
Sender 收到（第二个）ACK 1500 并继续前进。

关键点：duplicate segment 通过 cumulative ACK 和 sequence number 被安全处理。

**场景 3：Premature Timeout（不必要的 Retransmission）**

Sender 发送 segment 1（seq=1000，500 bytes）和 segment 2（seq=1500，500 bytes）在同一 flight 中（pipelined）。
两者都到达 receiver。
Receiver 发送 cumulative ACK 2000（确认两者）。
但假设该 ACK 延迟（由于 congestion 或 queuing）。
Sender 的 segment 1 timer 在延迟 ACK 到达前到期 → sender retransmit segment 1。
不久后延迟 ACK 2000 到达。
Sender 看到 ACK 2000 覆盖了 retransmit 的 segment 1（及更多），因此从 buffer 中移除两者并继续。

这是不必要 retransmission 的示例——浪费，但正确。TCP 宁愿 retransmit 而非冒险数据未交付。

**场景 4：多个 Segment 丢失 — Cumulative ACK 后续帮助**

Sender 发送 segments 1、2、3、4（每个 500 bytes，seq 1000、1500、2000、2500）。
Segment 2 丢失；1、3 和 4 到达。
Receiver 将 segment 1 in-order 交付给 application，buffer 3 和 4，发送 duplicate ACK 1500（next expected = 1500）。
当 segment 3 再次到达（duplicate）时，仍 duplicate ACK 1500。
Segment 4 同理。
Sender 最终在 segment 2 上 timeout，retransmit 它。
Receiver 收到 segment 2，现在 buffer 中有 2、3、4 → 将它们全部交付给 application，发送新的 cumulative ACK 3000。

这展示了 cumulative ACK 如何让 receiver 在缺失 segment 到达后“赶上”。

**Fast Retransmit 的实际运作**

现在让我们看看为什么 Fast Retransmit 如此宝贵。

相同设置：发送 segments 1、2、3、4。Segment 2 丢失。
Receiver 收到 1 → ACK 1500
收到 3 → duplicate ACK 1500
收到 4 → duplicate ACK 1500（第三个 duplicate）
Sender 看到三个 1500 的 duplicate ACK → 立即 retransmit segment 2（seq=1500），无需等待 timeout。
Receiver 收到 segment 2，将 2、3、4 交付给 application，发送 ACK 3000。
Sender 收到 ACK 3000 并继续。

Fast Retransmit 通常比完整 timeout 早得多地检测丢失——往往显著缩短 recovery 时间。

**为什么是三个 Duplicate ACK？**

为什么是三个，而不是两个或四个？
如果只有一个 duplicate ACK，可能由正常 reordering 引起（segment 暂时 out-of-order 到达）。
两个 duplicate 仍可能由轻微 reordering 引起。
三个 duplicate 是 segment 缺失的强信号——Internet 中三个或更多 segment 的 reordering 非常罕见。
因此三个是个好的工程折衷：快速检测而无太多 false positive。

（注：这结束了 Part 1 讲座中通常涵盖的主要 retransmission 场景和 Fast Retransmit 讨论。视频通常在此结束，或在 flow control 和 connection management 的快速预览后结束，这些在 Part 2 或下一个讲座段落中更深入覆盖。）

References:

- [YouTube Video: 3.5-1 TCP Reliability, Flow Control, and Connection Management](https://www.youtube.com/watch?v=UYJP-6mhF6E)
- [Playlist: Computer Networking: A Top-Down Approach - All Chapters](https://www.youtube.com/playlist?list=PLByK_3hwzY3Tysh-SY9MKZhMm9wIfNOas)
