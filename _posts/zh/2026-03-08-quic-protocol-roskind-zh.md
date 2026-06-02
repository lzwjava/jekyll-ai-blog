---
audio: false
generated: true
image: false
lang: zh
layout: post
title: QUIC协议创建者吉姆·罗斯金德
translated: true
type: note
---

**问题：** QUIC 协议的作者/设计者 Jim Roskind 是谁？请提供全面介绍。

**答案：**

## Jim Roskind — 全面介绍

### 概述

Jim Roskind 是一位美国软件工程师，最为人所知的是他在 2012 年担任 Google 员工期间设计了 QUIC 协议。他的职业生涯跨越数十年，涉及计算历史中最具影响力的几家公司，他的贡献从根本上塑造了现代互联网传输数据的方式。

---

### 早年生活与教育

Jim 在南布朗克斯长大。尽管成长环境艰苦，但他还是追求了精英学术训练。他在 MIT 获得电气工程 SB 学位和计算机科学 SB 学位，随后在 Hertz Foundation 的支持下获得 MIT 的 SM EECS 学位和 EECS 博士学位，研究领域为数据通信网络，由 Robert G. Gallager 指导。他的研究生论文标题为 “Edge Disjoint Spanning Trees and Failure Recovery in Data Communication Networks”。

他还是 **1978 Hertz Fellow**，这是一个享有盛誉的基于优异的 merit-based 研究生奖学金，表彰杰出的科学才能。

---

### 职业时间线

#### Bell Labs（1980 年代早期）
1983 年从 MIT 获得博士学位后，Jim Roskind 加入 Bell Labs，在那里他从事数据通信和网络项目的研究与开发，利用他在容错系统方面的专长。

#### 自由职业与开源贡献（1983–1994）
在加入 Infoseek 之前的 10 年，他是一名自由软件承包商，为太多公司工作，无法一一列举。一份编译器工作促使他编写了一个开源的 YACCable C++ 语法，并随后成为 ANSI C++ Formal Syntax Working Group 的负责人。

#### Infoseek 联合创始人（1994）
Roskind 于 1994 年与包括 Steve Kirsch 在内的其他 7 人共同创立了 Infoseek。同年晚些时候，Roskind 编写了 Python profiler，该 profiler 如今仍是 Python 标准库的一部分——这是他对开发者社区的持久贡献。

#### Netscape / AOL — 首席架构师 & Java 安全架构师（1995–2003）
Jim 在 Netscape 工作了 8 年，在那里他设计并部署了带有 Signed Java 的 Java Security 模型，还帮助设计了 SSL 2.0，并担任 Java Security Architect。他在此期间的安全工作帮助确立了互联网基础年代的早期 web 安全标准。

1996 年在 Netscape 任职期间，他成功起诉 Morgan Stanley，认为他们出售他的股票的方式导致他获得的股价低于应得价格。该案上诉至美国最高法院，最高法院拒绝审理，从而保留了个人可以起诉股票经纪人违反州法的先例。

#### Google（2008–2016）— 设计 QUIC
他在 Google 工作了八年，在那里他设计了 QUIC 协议，并领导其在 Chrome 中的实现，该协议已演变为最近获批的 IETF 标准 HTTP/3。

除了 QUIC 外，他在 Google 的更广泛工作包括：
设计并实现客户端指标系统、speculative DNS pre-resolution、speculative TCP pre-connection、HTTP 上的 Shared Dictionary Compression (SDCH)，以及一个始终开启的内部 profiler。在离开 Google 前，他还花了一年时间从事 Machine Learning 研究。

#### Amazon（2016–至今）— 副总裁兼杰出工程师
Jim Roskind 是 Amazon 的副总裁兼杰出工程师，于 2016 年加入公司。Jim 在那里的主要工作重点是提高计算效率、eCommerce 可用性和应用延迟。

---

### QUIC 协议 — 他的标志性遗产

QUIC 是一种通用传输层网络协议，最初由 Google 的 Jim Roskind 设计。它于 2012 年首次实现并部署，并于 2013 年随着实验范围扩大而公开发布。

Roskind 开创的 QUIC 关键特性：

- **UDP-based**：QUIC 使用 User Datagram Protocol (UDP) 在两个端点之间建立多个复用连接，并设计用于取代许多应用的传输层 TCP。
- **低延迟**：QUIC 是一种加密的、复用的、低延迟传输协议，从头设计以改善 HTTPS 流量的传输性能，并实现传输机制的快速部署和持续演进。
- **大规模部署**：QUIC 已由 Google 在全球数千台服务器上部署，用于向各种客户端提供流量，包括广泛使用的 web 浏览器 (Chrome) 和流行的移动视频流应用 (YouTube)。
- **HTTP/3 基础**：2017 年，Google 的 QUIC 工程师引述的数据显示，当时约 7% 的所有互联网流量已使用该协议。后来它被 IETF 标准化为 HTTP/3。

---

### 专利与标准贡献

在他的工作中，他还获得了超过 190 项美国专利。有些来源称该数字超过 300 项，反映了他在网络、安全和编译器技术方面的多产创新。他还作为 Formal Syntax Working Group 负责人贡献于 **ANSI C++ 标准**。

---

### 荣誉

Roskind 对网络安全的贡献使他在 2024 年入选 National Cyber Security Hall of Fame，以表彰他在 Netscape、Google 和 Amazon 任职期间的安全架构、网络协议（包括 QUIC 协议）以及威胁缓解策略的开创性工作。

---

### 个人与爱好

据报道，他不太明显的爱好包括家谱学、快速变牌魔术、杂耍、足球裁判以及健身。不太当前的消遣包括让 NASDAQ 经纪人更诚实、水肺潜水、跳板跳水、体操、摩托车骑行（并教学）、独轮车、开锁、飞行飞机、从完全良好的飞机上跳伞、柔道、柔术和跆拳道。

---

### 总结表格

| Period | Organization | Key Contribution |
|---|---|---|
| MIT (SB/SM/PhD) | MIT | Thesis on fault-tolerant network recovery |
| 1983–1994 | Bell Labs / Freelance | Network research, ANSI C++ grammar |
| 1994 | Infoseek (Co-founder) | Co-founded search engine; wrote Python profiler |
| 1995–2003 | Netscape / AOL | SSL 2.0, Java Security Model |
| 2008–2016 | Google | **Designed QUIC protocol**, Chrome performance |
| 2016–Present | Amazon | VP & Distinguished Engineer, e-commerce reliability |

---

**参考资料：**

- [Jim Roskind — Wikipedia](https://en.wikipedia.org/wiki/Jim_Roskind)
- [QUIC — Wikipedia](https://en.wikipedia.org/wiki/QUIC)
- [Hertz Foundation — James Roskind](https://www.hertzfoundation.org/people/james-roskind/)
- [The QUIC Transport Protocol: Design and Internet-Scale Deployment (SIGCOMM 2017)](https://research.google/pubs/the-quic-transport-protocol-design-and-internet-scale-deployment/)
- [Jim Roskind on X/Twitter](https://x.com/jimroskind)
