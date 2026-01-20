---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: CN1 与 CN2 网络层级对比
translated: true
type: note
---

**Question:** 比较中国互联网中的 CN1 和 CN2 网络与全球互联网。

**Answer:**

在中国互联网基础设施的语境下，特别是针对 China Telecom（许多国际连接的主导运营商），**CN1** 和 **CN2** 指的是用于进出中国大陆流量路由的不同骨干网。

- **CN1**（也称为 ChinaNet 或 163 骨干网，AS4134）：这是 China Telecom 最早且规模最大的公共互联网骨干网。它承载了中国绝大部分（约 85-90%）的互联网流量，包括大多数住宅和普通宽带用户。路由通常以 202.97.x.x 等 IP 段开头。它是最便宜且覆盖最广的选项，但在高峰时段（如中国晚间）拥堵严重，导致国际流量的 Latency（延迟）更高、Packet Loss（丢包）严重且稳定性较差。

- **CN2**（China Telecom Next Generation Carrier Network，AS4809）：这是为了解决 CN1/ChinaNet 的局限性，于 2005-2006 年左右推出的基于 MPLS 的下一代高端骨干网。它专为高质量、低 Latency、更好的冗余和企业级性能而设计。路由通常以 59.43.x.x 开头。CN2 仅承载较小比例的总流量（约 10-15%），因此保持了较低的拥堵程度。它细分为：
  - **CN2 GT** (Global Transit)：一种性价比高的优质选项，拥有专用的国际出口路径，但在国内段通常与 ChinaNet (163) 共享。它的性能优于 CN1，但在回程路径上仍可能遇到国内段拥堵。
  - **CN2 GIA** (Global Internet Access)：最高级别的选项，拥有完全专用的路径（去程和回程），跳数极少，保障低 Latency，几乎无拥堵，且稳定性最好。它是最昂贵、容量最受限的，且对攻击较为敏感（例如，DDoS 攻击常导致 Null-routing）。

**与全球互联网（中国境外的典型 Tier-1/Tier-2 路由）的比较：**

| 维度 | CN1 (ChinaNet / 163) | CN2 GT | CN2 GIA | 典型全球互联网 (如美国/欧洲 Tier-1 路由) |
|---------------------|---------------------------------------|--------------------------------------|--------------------------------------|-----------------------------------------------------|
| **主要用途** | 大众消耗流量，普通访问 | 中端优质，高性价比企业级 | 高端企业，延迟敏感型应用 | 通用的全球 Peering/Transit |
| **到中国的 Latency** | 高（美欧常在 200-400+ ms 且有峰值） | 中（优于 CN1，约 150-300 ms） | 低（邻近地区常在 100-200 ms 或更低） | 取决于距离/Peering (50-300+ ms 不等) |
| **拥堵情况** | 非常高，尤其是高峰时段 | 中度（负载比 CN1 轻） | 极低（利用率保持在 50% 以下） | 在 Peering 良好的路由上通常较低 |
| **稳定性/丢包** | 高峰期较差（常见 5-10%+ 丢包） | 国际段良好，国内段有波动 | 极佳（正常情况下接近零丢包） | 优质路径上表现良好至极佳 |
| **成本** | 低/最便宜 | 中 | 非常高（某些情况下超过 $100+/Mbps） | 波动较大，通常低于 CN2 GIA |
| **容量/份额** | 巨大 (85-90% 的 China Telecom 流量) | 较小 | 非常有限 | 全球范围内巨大 |
| **适用场景** | 预算型访问，非关键应用 | 性能与成本平衡 | 游戏、VoIP、金融、实时应用 | 通用的全球流量 |

**核心要点：**
- CN1 提供了广泛且廉价的接入，但受限于拥堵，在跨境流量上的表现明显差于典型的全球互联网路由。
- CN2（尤其是 GIA）在连接中国时性能往往优于标准的全球路由，提供比许多非优质国际路径更低的 Latency 和更高的可靠性——这就是为什么优质 VPS/CDN 服务商会大力推广“CN2 GIA to China”。
- 全球互联网路由更加去中心化且 Peering 丰富，但由于中国独特的出口节点和政策，如果不使用 CN2 等优质路由，访问中国仍具挑战性。
- 在 2025-2026 年，CN2 GIA 及其等效产品（包括 CTGNet 等新变体）仍然是低 Latency 访问中国的“金标”，而 CN1 仍然是日常使用的默认选择。

**参考文献：**

- [https://www.dataplugs.com/en/direct-connection-to-china-cn2-gia-vs-cn2-gt-vs-as4134](https://www.dataplugs.com/en/direct-connection-to-china-cn2-gia-vs-cn2-gt-vs-as4134)
- [https://bandwagonhost.com/cn2gia-vps.php](https://bandwagonhost.com/cn2gia-vps.php)
- [https://www.jtti.cc/supports/655.html](https://www.jtti.cc/supports/655.html)
- [https://zhuanlan.zhihu.com/p/1898372841344304871](https://zhuanlan.zhihu.com/p/1898372841344304871)
- [https://github.com/china-net/Internationally-connected](https://github.com/china-net/Internationally-connected)