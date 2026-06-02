---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络有效吞吐量简单解释
translated: true
type: note
---

**问题：** 网络中的 **"goodput"** 是什么意思？

**答案：**

**Goodput** 是指在网络连接中每单位时间内成功交付到应用层（或最终用户）的**实际有用数据**。

它仅测量以下**application payload data**：

- 正确接收的
- 正确顺序的
- 无错误的
- 无重复的
- 在移除所有 protocol overhead 和无用/重传数据之后

### Goodput 与相关术语的对比

- **Throughput**
  → 每秒成功传输通过链路的总比特数（包括协议头部、重传等）

- **Goodput**
  → 接收端实际使用的**有用 application data**（排除头部、控制包、重传数据、重复包等）

- **Bandwidth**
  → 链路的理论最大容量

### 典型关系（按降序排列）

Bandwidth ≥ Throughput ≥ Goodput

### 实际示例

| 场景                                   | Throughput | Goodput   | 差异解释                                      |
|----------------------------------------|------------|-----------|-----------------------------------------------|
| 无丢包的干净 HTTP/2 下载                | ~980 Mbps  | ~940 Mbps | 主要是 HTTP/2 + TLS 头部                      |
| 5% 丢包的 TCP 连接                     | 600 Mbps   | 380 Mbps  | 许多重传消耗带宽                              |
| 大量 FEC 的视频流                      | 25 Mbps    | 18 Mbps   | Forward Error Correction 包不携带有效载荷     |
| 高开销的 VPN 隧道                      | 850 Mbps   | 620 Mbps  | IPsec/ESP + 内层 IP + TCP/UDP 头部            |
| 非常丢包的 Wi-Fi 上的文件传输           | 40 Mbps    | 8 Mbps    | 极高的重传率                                  |

### 总结 – 最常见的记忆方式

**Goodput = Throughput – 无用流量**
（无用 = 协议头部 + 重传 + 控制包 + 重复 + 填充 + 未帮助的 FEC 开销）

在性能敏感的应用（文件传输、视频流、游戏、实时协议）中，工程师更关心 **goodput** 而非原始 throughput。

**参考文献：**

- 此概念解释无需参考
