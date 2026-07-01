---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络性能与定性指标
translated: true
type: note
---

**问题：** 为什么有必要建立一套计算机网络性能指标？计算机网络常用的 **非定量** 性能指标有哪些？

**答案：**

## 第一部分 — 为什么建立一套计算机网络性能指标？

Network performance metrics 是观察和确定网络行为的定性和定量方式。它们提供了对网络基础设施和服务运行状况的更深刻理解，实时洞察潜在问题、中断和错误，并允许 IT 团队相应地部署和优先分配资源。

简而言之，建立一套全面的性能指标有三个核心目的：

1. **评估网络运行质量** — 指标允许工程师和管理人员判断网络运行良好还是糟糕，并比较随时间变化的性能。
2. **促进研究和设计** — 标准化指标为研究人员、设计师和运营商在研究、构建和改进网络时提供了一种通用语言。
3. **满足用户和业务需求** — Network performance metrics 使我们能够理解终端用户需求，并帮助创建适应当前和未来业务需求的网络。

如果没有定义的一套指标，就没有客观依据来比较网络、诊断故障或保证服务水平。

---

## 第二部分 — 常用的非定量（定性）性能指标

非定量指标是网络的描述性、策略导向或架构质量，无法轻易归结为单个数字。标准集合包括以下六个指标：

---

### 1. Quality of Service (QoS) — 服务质量

Quality of Service (QoS) 是对服务整体性能的描述或测量 — 特别是网络用户体验到的性能。它是为主张为不同应用、用户或数据流提供不同优先级，或为数据流保证一定性能水平的能力。

QoS 被视为 **非定量** 指标，因为它是一个涵盖许多子指标（latency、jitter、packet loss 等）的总体概念，并最终反映出对于给定用例（例如 VoIP、视频会议、gaming）服务是否“足够好”的主观判断。

---

### 2. Reliability (可靠性)

Mean Time Between Failures (MTBF) 是网络故障之间的平均时间，表示可靠性。然而，作为性能 **指标**，Reliability 是一种定性属性 — 它描述了网络在正常和异常条件下是否能被信任正确和一致地传输数据。它包括 fault tolerance、redundancy 和 error recovery 等概念，这些无法用单个数字捕捉。

---

### 3. Scalability (可扩展性)

Scalability 指的是网络在添加更多用户、设备或流量时增长和适应的能力，而不会显著降低性能。随着架构变得更加复杂，理解和规划网络的底层组成是一种基本的良好实践，涵盖传统基础设施（hubs、switches、routers）以及无线网络、WANs、LANs、virtual LANs 和 cloud applications。Scalability 是定性的，因为它描述了一种设计理念和架构灵活性，而不是可测量的值。

---

### 4. Security (安全性)

安全指标包括 intrusion detection rate（检测未经授权访问的有效性）、vulnerability assessments（评估网络可能被威胁利用的弱点）和 security incident response time。作为非定量指标，**Security** 整体上指的是网络保护数据机密性、完整性和可用性的能力 — 这是一个涵盖 policies、protocols、encryption 和 access control 的广泛属性。

---

### 5. Standardization (标准化)

Standardization 指的是网络是否符合国际公认的 protocols 和 specifications（例如 TCP/IP、IEEE 802.x、ISO/OSI）。标准化的网络确保不同 vendors、systems 和国家之间的 interoperability。这完全是一个定性/架构指标 — 没有单个数字代表网络“标准化程度”。

---

### 6. Cost (成本)

Cost 指的是设计、构建、运行和维护网络所需的总经济支出。虽然单个成本数字是数字，但 **Cost 作为性能指标** 是非定量的，因为它反映了设计权衡和 policy decision（例如，平衡性能与预算），而不是网络行为的直接测量。

---

## 总结表格

| 非定量指标 | 核心含义 |
| --- | --- |
| **QoS** (服务质量) | 整体用户感知的服务体验 |
| **Reliability** | 正确和一致运行的能力 |
| **Scalability** | 无性能损失增长和适应的能力 |
| **Security** | 保护数据和网络免受威胁 |
| **Standardization** | 符合开放、可互操作 protocols |
| **Cost** | 构建和维护网络的经济可行性 |

这些六个指标补充定量指标（例如 bandwidth、latency 和 packet loss），提供网络如何服务用户并满足工程目标的完整图景。

**参考文献：**

- [https://obkio.com/blog/how-to-measure-network-performance-metrics/](https://obkio.com/blog/how-to-measure-network-performance-metrics/)
- [https://en.wikipedia.org/wiki/Quality_of_service](https://en.wikipedia.org/wiki/Quality_of_service)
- [https://www.solarwinds.com/resources/it-glossary/network-metrics](https://www.solarwinds.com/resources/it-glossary/network-metrics)
- [https://www.viavisolutions.com/en-us/enterprise/resources/learning-center/what-are-network-performance-metrics](https://www.viavisolutions.com/en-us/enterprise/resources/learning-center/what-are-network-performance-metrics)
- [https://www.cbtnuggets.com/blog/technology/networking/what-are-network-metrics](https://www.cbtnuggets.com/blog/technology/networking/what-are-network-metrics)
