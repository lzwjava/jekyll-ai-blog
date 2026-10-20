---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCP拥塞控制简介
translated: true
type: note
---

问题：请介绍TCP拥塞控制算法？

答案：

## 概述

TCP拥塞控制是TCP发送端调节数据注入网络速率、防止拥塞崩溃的机制。核心思想：发送端维持一个**拥塞窗口（cwnd）**，限制当前在途未确认的字节数。

```
Flight size = min(cwnd, receiver's advertised window)
```

---

## 核心概念

### AIMD — 基本原则
所有经典算法遵循**加性增、乘性减（Additive Increase, Multiplicative Decrease）**：
- **增**：正常操作时缓慢增长cwnd（加性）
- **减**：收到拥塞信号时急剧减小cwnd（乘性）

### 拥塞信号

| 信号 | 含义 |
|------|------|
| 三次重复ACK | 数据包丢失，但网络仍在传递ACK |
| 超时（RTO） | 严重拥塞或路由故障 |

---

## 阶段机制

### 1. Slow Start（慢启动）
- 初始时cwnd = 1 MSS（现代协议栈中约为10 MSS）
- **每个RTT将cwnd翻倍**（指数增长）
- 当cwnd达到`ssthresh`（慢启动阈值）时停止

```
Each ACK → cwnd += 1 MSS
```

### 2. Congestion Avoidance（拥塞避免）
- cwnd**线性增长**（每个RTT增加1个MSS）
- 探测可用带宽而不造成泛洪

```
Each ACK → cwnd += MSS × (MSS / cwnd)
```

### 3. Fast Retransmit（快速重传）
- 收到**3个重复ACK**时：立即重传丢失的段——无需等待RTO

### 4. Fast Recovery（快速恢复）
- 快速重传后：保持在"减小但未崩溃"的状态
- 避免非严重丢包时回到慢启动

---

## 关键算法时间线

### TCP Tahoe (1988)
最早的版本。发生**任何**丢包事件（超时或3次重复ACK）时：
```
ssthresh = cwnd / 2
cwnd = 1 MSS        ← always resets to Slow Start
```

### TCP Reno (1990)
区分丢包类型。收到**3次重复ACK**时：
```
ssthresh = cwnd / 2
cwnd = ssthresh     ← Fast Recovery instead of Slow Start
```
**超时时** → 与Tahoe相同（重置为1 MSS）。

### TCP NewReno (RFC 6582)
修复了Reno在一个窗口内丢多个数据包时的弱点：
- 保持在Fast Recovery阶段，直到所有丢失的段都被恢复（追踪"部分ACK"）

### TCP SACK（选择性确认）
本身并非一种算法，而是一项关键扩展——接收方精确报告哪些字节已到达，使发送方只重传缺失部分。

### TCP CUBIC (RFC 9438) — Linux 2.6.19以来的默认算法
使用自上次拥塞事件以来的时间的**三次函数**作为窗口增长依据，与RTT无关：
```
W(t) = C(t − K)³ + Wmax
```
- 远离上次最大值时快速增长，接近时谨慎增长
- 对长肥网络（高带宽×时延）友好
- Linux、macOS、Android的默认算法

### BBR (Bottleneck Bandwidth and RTT) — Google, 2016
完全不同：**基于模型，而非基于丢包**。
- 持续估计**瓶颈带宽（BtlBw）**和**最小RTT**
- 以最佳操作点为目标：填满管道但不膨胀缓冲区
- 忽略丢包作为主要信号（在有损WiFi中丢包≠拥塞）
- 被Google、YouTube、QUIC使用；BBRv3是当前版本

```
pacing_rate = BtlBw × pacing_gain
cwnd        = BtlBw × RTprop × cwnd_gain
```

---

## 对比一览

| 算法 | 丢包信号 | 增长方式 | RTT公平性 | 备注 |
|------|----------|----------|-----------|------|
| Tahoe | 超时+重复ACK | 任何丢包后慢启动 | 是 | 历史基准 |
| Reno | 区分事件 | 重复ACK时快速恢复 | 是 | 简单，被广泛研究 |
| NewReno | 与Reno相同 | 更好的多丢包恢复 | 是 | RFC 6582 |
| CUBIC | 重复ACK/超时 | 时间三次方 | 更好 | Linux默认 |
| BBR | 带宽+RTT模型 | 基于速率控制 | 部分 | YouTube/GCP规模 |

---

## 状态图（Reno/CUBIC）

```
             ┌─────────────────────────────────────────┐
             │              SLOW START                  │
             │  cwnd doubles each RTT                   │
             └──────────────┬──────────────────────────┘
                            │ cwnd ≥ ssthresh
                            ▼
             ┌─────────────────────────────────────────┐
             │          CONGESTION AVOIDANCE            │
             │  cwnd += 1 MSS per RTT                   │
             └──────────┬──────────────┬───────────────┘
                        │ 3 dup-ACKs   │ Timeout
                        ▼              ▼
             ┌──────────────┐   ssthresh = cwnd/2
             │ FAST RECOVERY│   cwnd = 1 MSS
             │ ssthresh=cwnd/2   → back to SLOW START
             │ cwnd=ssthresh│
             └──────────────┘
```

---

## 未来方向（现代发展）

- **QUIC**（HTTP/3）——在应用层实现自己的拥塞控制，默认使用CUBIC或BBR
- **Copa / PCC Vivace**——面向时延敏感型工作负载的时延梯度算法
- **Swift**——Google数据中心变体，针对微秒级RTT优化
- **基于机器学习的拥塞控制**——Aurora、Orca使用强化学习在线调整拥塞控制

参考资料：
- [RFC 5681 – TCP Congestion Control](https://datatracker.ietf.org/doc/html/rfc5681)
- [RFC 9438 – CUBIC for Fast Long-Distance Networks](https://datatracker.ietf.org/doc/html/rfc9438)
- [RFC 6582 – The NewReno Modification to TCP's Fast Recovery](https://datatracker.ietf.org/doc/html/rfc6582)
- [BBR: Congestion-Based Congestion Control (ACM Queue, 2016)](https://queue.acm.org/detail.cfm?id=3022184)
- [Computer Networks: A Systems Approach – Peterson & Davie, Chapter 6](https://book.systemsapproach.org/congestion/tcpcc.html)