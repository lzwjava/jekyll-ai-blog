---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: iPerf3网络带宽测试工具
translated: true
type: note
---

### 什么是 iPerf3？

iPerf3 是一款开源的命令行工具，专为测量网络带宽和性能而设计。它通常用于通过在两个端点（一个作为服务器，另一个作为客户端）之间模拟流量来测试 IP 网络可实现的最大吞吐量。这有助于诊断局域网或广域网中的延迟、数据包丢失和瓶颈等问题。

#### 主要特性：
- **支持的协议**：TCP、UDP 和 SCTP，适用于灵活的测试场景。
- **可定制性**：允许调整缓冲区大小、测试时长和双向流量等参数。
- **输出结果**：提供带宽、抖动和数据报丢失的详细统计数据。

#### 基本使用示例：
测试两台机器之间的带宽：
1. 在服务器上：`iperf3 -s`（启动服务器）。
2. 在客户端：`iperf3 -c <服务器_IP>`（连接并默认运行 10 秒测试）。

它轻量级、跨平台（适用于 Linux、Windows、macOS），被网络管理员、开发人员和 IT 专业人士广泛用于故障排除。

#### 历史背景：
iPerf3 是对原始 iPerf 工具的完全重写，由 ESnet（能源科学网络）于 2009 年启动，并于 2014 年首次发布。此次重新设计旨在实现更小、更易维护的代码库，同时提高准确性。

更多详细信息，请查看官方网站或 GitHub 仓库。

### 参考资料
- [iPerf - TCP、UDP 和 SCTP 网络带宽测量工具](https://iperf.fr/)
- [iperf3：TCP、UDP 和 SCTP 网络带宽测量工具](https://github.com/esnet/iperf)
- [Iperf - 维基百科](https://en.wikipedia.org/wiki/Iperf)
