---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RMON2 高效时间过滤器
translated: true
type: note
---

这个问题涉及 RMON2（远程监控第二版）MIB 设计及如何提升网络管理效率。

正确答案是 **A - 时间过滤索引（Time filter index）**。

**解释：**

网络管理应用需定期轮询监控设备，以获取被管对象的最新状态信息。为提升效率，我们希望监控设备仅返回自上次查询后发生变化的数据。SNMPv1 和 SNMPv2 均未直接解决此问题。

然而，RMON2 的设计者在 MIB 定义中创新性地实现了这一功能——通过**时间过滤索引（time filter for indexing）**机制。

**工作原理：**

- 时间过滤索引允许管理者仅检索自指定时间后发生变化的条目
- 本质上是一种基于时间戳的过滤机制
- 当管理者使用时间过滤索引值查询时，代理仅返回该时间戳后发生变化的对象

该方法通过消除冗余数据传输，显著减少了网络流量和处理开销，使网络监控更高效。
