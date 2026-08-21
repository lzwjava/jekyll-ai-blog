---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络吞吐量的定义
translated: true
type: note
---

**问题：** 单位时间内通过网络（或通道/接口）的数据量术语是什么？

**答案：** 答案是 **吞吐量 (Throughput)**。

吞吐量是指在给定时间内通过网络、通道或接口成功传输的实际数据量。它是网络性能的关键指标，通常以 **bps（比特每秒）**、**Mbps** 或 **Gbps** 为单位进行衡量。

主要区别：

- **带宽 (Bandwidth)** — 链路的*理论最大*容量
- **吞吐量 (Throughput)** — *实际测量*的数据传输速率（始终 ≤ 带宽）
- **延迟 (Latency)** — 数据从源到目的地传输的延迟/时间

吞吐量可能受到网络拥塞、丢包、协议开销、硬件限制和干扰等因素的影响。

参考来源：

- [吞吐量 - 维基百科](https://en.wikipedia.org/wiki/Throughput)
- [带宽 vs 吞吐量 - Cloudflare](https://www.cloudflare.com/learning/network-layer/what-is-throughput/)
