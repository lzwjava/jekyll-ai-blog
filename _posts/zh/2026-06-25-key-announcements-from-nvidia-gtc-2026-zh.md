---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA GTC 2026关键公告
translated: true
type: note
---

**问题：** NVIDIA GTC 2026 有哪些重要发布？

**答案：**

GTC 2026 于3月16日至19日在圣何塞SAP Center举行，参会者超过3万人。黄仁勋的主题演讲涵盖了五大主题：

---

## 1. Vera Rubin — 下一代GPU架构

Vera Rubin VR200 是头号硬件：50 PFLOPS FP4 算力，288 GB HBM4，22 TB/s 内存带宽——与 Blackwell B300 在相同内存占用基础上实现3.3倍算力飞跃。该系统包含130万个组件，每瓦性能比 Grace Blackwell 高出10倍。数据中心部署目标为2026年下半年。工作站版本尚未确认。

关键规格对比 Blackwell B300（15 PFLOPS FP4，8 TB/s 带宽）：

- FP4：50 PFLOPS（3.3倍）
- HBM带宽：22 TB/s（2.8倍）
- 晶体管：3360亿，3nm工艺

---

## 2. 1万亿美元订单簿

黄仁勋表示，他预计 Blackwell 和 Vera Rubin 的采购订单到2027年将达到1万亿美元——是此前5000亿美元预测的两倍。营收已飙升：2026年第一季度营收预计约为780亿美元，同比增长77%，连续11个季度增长率超过55%。

---

## 3. 智能体AI — NemoClaw + OpenClaw

黄仁勋推出了 NemoClaw，作为 OpenClaw 智能体的企业级参考堆栈：一次安装即可拉取运行时和 Nemotron 模型，构建一个可用的AI智能体。合作伙伴：Adobe、Atlassian、Salesforce、ServiceNow。这是智能体基础设施布局——实质上是 NVIDIA 将自身定位为企业默认的智能体运行时。

---

## 4. 收购 Groq + 推理策略

宣布了一笔200亿美元的 Groq 交易。Groq 3 LPU 在台上亮相；一个完整的 LPX 机架容纳256个 LPU，设计为与 Vera Rubin 机架并排放置。黄仁勋声称 Groq LPX 机架将 Rubin GPU 上的每瓦 token 产出提升35倍——将高吞吐GPU与低延迟LPU相结合。Jensen的论点：两年内推理的规模将与训练相当。

---

## 5. 物理AI / 机器人

黄仁勋宣布物理AI是“下一个大浪潮”。Boston Dynamics、Figure 和 Tesla Optimus 均基于 NVIDIA 基础设施构建。Isaac Sim 和 Omniverse 已更新，支持在仿真中进行机器人预训练。在汽车领域，Uber 将在2028年前在四大洲28个城市部署 NVIDIA Drive AV。日产、比亚迪、吉利、五十铃和现代正在基于 Drive Hyperion 构建L4级自动驾驶汽车。

---

## 6. 开源模型 — 260亿美元投资

NVIDIA 将在五年内投入260亿美元用于开放权重AI模型。首个成果：Nemotron 3 Super — 总共1200亿参数，120亿激活（MoE风格）。已在 Perplexity、Siemens、Palantir 和 Cadence 部署。

---

## 7. 数据+生态系统

NVIDIA 与 IBM 合作，在 NVIDIA GPU 上利用 cuDL 加速 watsonx.data。DuckDB、Snowflake、Databricks 和 Apache Spark 宣布与 NVIDIA RAPIDS 实现 GPU 原生集成——GPU加速现已扩展到查询/转换层，而不仅仅是训练。

---

## 这对你意味着什么（AI工程视角）

- **2026年下半年发布的 Vera Rubin VR200** → 你目前正在训练的 AMD MI300X 在2026年仍具相关价值，但推理成本/性能比将大幅向 NVIDIA 堆栈倾斜。
- **NemoClaw/OpenClaw** → NVIDIA 正在抢占智能体基础设施层；值得将其视为你正在构建的自定义智能体堆栈的竞争对手/补充方案进行关注。
- **Groq 3 LPX** → 每瓦特 token 产出对你未来的推理成本优化至关重要。
- **Nemotron 3 Super MoE** → 120B/12B 激活，开放权重——与你已在运行的 DeepSeek v4 MoE 直接竞争。值得进行基准测试。

**参考资料：**

- [NVIDIA GTC 2026 实时博客](https://blogs.nvidia.com/blog/gtc-2026-news/)
- [CNBC：黄仁勋主题演讲回顾](https://www.cnbc.com/2026/03/16/nvidia-gtc-2026-ceo-jensen-huang-keynote-blackwell-vera-rubin.html)
- [Vera Rubin vs Blackwell 深度解析 — BIZON](https://bizon-tech.com/nvidia-gtc-2026-key-announcements)
- [GTC 2026 回顾 — Idlen](https://www.idlen.io/news/gtc-2026-recap-announcements-jensen-huang-nvidia/)
