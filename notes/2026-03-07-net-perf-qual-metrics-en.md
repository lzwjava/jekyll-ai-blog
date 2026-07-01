---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Performance and Qualitative Metrics
translated: false
type: note
---

**Question:** Why is it necessary to establish a set of computer network performance metrics? What are the commonly used **non-quantitative** performance indicators for computer networks?

**Answer:**

## Part 1 — Why Establish a Set of Computer Network Performance Metrics?

Network performance metrics are qualitative and quantitative ways to observe and determine network behavior. They provide a more profound understanding of how network infrastructure and services are operating, deliver real-time insights into potential issues, outages, and errors, and allow IT teams to deploy and prioritize resources accordingly.

In short, establishing a comprehensive set of performance metrics serves three core purposes:

1. **Evaluating network operation quality** — Metrics allow engineers and administrators to judge whether a network is running well or poorly, and to compare performance over time.
2. **Facilitating research and design** — Standardized indicators provide a common language for researchers, designers, and operators when studying, building, and improving networks.
3. **Meeting user and business demands** — Network performance metrics enable understanding of end-user demands and help create adaptive networks to meet present and future business needs.

Without a defined set of metrics, there would be no objective basis for comparing networks, diagnosing faults, or guaranteeing service levels.

---

## Part 2 — Commonly Used Non-Quantitative (Qualitative) Performance Indicators

Non-quantitative indicators are descriptive, policy-oriented, or architectural qualities of a network that cannot be easily reduced to a single number. The standard set includes the following six indicators:

---

### 1. Quality of Service (QoS) — 服务质量

Quality of Service (QoS) is the description or measurement of the overall performance of a service — particularly the performance as experienced by users of the network. It is the ability to provide different priorities to different applications, users, or data flows, or to guarantee a certain level of performance to a data flow.

QoS is considered **non-quantitative** as an indicator because it is an overarching concept that encompasses many sub-metrics (latency, jitter, packet loss, etc.) and ultimately reflects a subjective judgement about whether service is "good enough" for a given use case (e.g., VoIP, video conferencing, gaming).

---

### 2. Reliability (可靠性)

Mean Time Between Failures (MTBF) is the average time between network failures, indicating reliability. However, as a performance **indicator**, reliability is a qualitative property — it describes whether a network can be trusted to deliver data correctly and consistently under normal and abnormal conditions. It includes concepts such as fault tolerance, redundancy, and error recovery, which cannot be captured by a single number.

---

### 3. Scalability (可扩展性)

Scalability refers to the ability of a network to grow and adapt — adding more users, devices, or traffic — without significant degradation of performance. As architecture becomes more complex, understanding and planning the underlying composition of the network is an essential best practice, covering traditional infrastructure (hubs, switches, routers) as well as wireless networks, WANs, LANs, virtual LANs, and cloud applications. Scalability is qualitative because it describes a design philosophy and architectural flexibility rather than a measurable value.

---

### 4. Security (安全性)

Security metrics include the intrusion detection rate (the effectiveness of detecting unauthorized access), vulnerability assessments (evaluation of the network's weaknesses that could be exploited by threats), and security incident response time. As a non-quantitative indicator, **security** refers holistically to the network's ability to protect data confidentiality, integrity, and availability — a broad property that encompasses policies, protocols, encryption, and access control.

---

### 5. Standardization (标准化)

Standardization refers to whether the network conforms to internationally recognized protocols and specifications (e.g., TCP/IP, IEEE 802.x, ISO/OSI). A standardized network ensures interoperability between different vendors, systems, and countries. This is entirely a qualitative/architectural indicator — there is no single number that represents "how standardized" a network is.

---

### 6. Cost (成本)

Cost refers to the total economic expenditure required to design, build, operate, and maintain the network. While individual cost figures are numbers, **cost as a performance indicator** is non-quantitative in the sense that it reflects a design trade-off and policy decision (e.g., balancing performance versus budget), rather than a direct measurement of network behavior.

---

## Summary Table

| Non-Quantitative Indicator | Core Meaning |
| --- | --- |
| **QoS** (Service Quality) | Overall user-perceived service experience |
| **Reliability** | Ability to operate correctly and consistently |
| **Scalability** | Ability to grow and adapt without performance loss |
| **Security** | Protection of data and network from threats |
| **Standardization** | Conformance to open, interoperable protocols |
| **Cost** | Economic feasibility of building and maintaining the network |

These six indicators complement quantitative metrics (such as bandwidth, latency, and packet loss) to give a complete picture of how well a network serves its users and meets engineering goals.

**References:**

- [https://obkio.com/blog/how-to-measure-network-performance-metrics/](https://obkio.com/blog/how-to-measure-network-performance-metrics/)
- [https://en.wikipedia.org/wiki/Quality_of_service](https://en.wikipedia.org/wiki/Quality_of_service)
- [https://www.solarwinds.com/resources/it-glossary/network-metrics](https://www.solarwinds.com/resources/it-glossary/network-metrics)
- [https://www.viavisolutions.com/en-us/enterprise/resources/learning-center/what-are-network-performance-metrics](https://www.viavisolutions.com/en-us/enterprise/resources/learning-center/what-are-network-performance-metrics)
- [https://www.cbtnuggets.com/blog/technology/networking/what-are-network-metrics](https://www.cbtnuggets.com/blog/technology/networking/what-are-network-metrics)
