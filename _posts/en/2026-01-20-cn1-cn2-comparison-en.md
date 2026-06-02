---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Comparing CN1 and CN2 Network Tiers
translated: false
type: note
---

**Question:** Compare CN1 and CN2 networks in China's internet to the global internet.

**Answer:**

In the context of China's internet infrastructure, particularly China Telecom (the dominant provider for many international connections), **CN1** and **CN2** refer to different backbone networks used for routing traffic to/from mainland China.

- **CN1** (also called ChinaNet or 163 backbone, AS4134): This is China Telecom's original and largest public internet backbone network. It handles the majority (around 85-90%) of China's internet traffic, including most residential and general broadband users. Routes often start with IP segments like 202.97.x.x. It is the cheapest and most widely available option but suffers from heavy congestion, especially during peak hours (e.g., evenings in China), leading to higher latency, packet loss, and instability for international traffic.

- **CN2** (China Telecom Next Generation Carrier Network, AS4809): This is the premium, next-generation MPLS-based backbone launched around 2005-2006 to address the limitations of CN1/ChinaNet. It is designed for higher quality, lower latency, better redundancy, and enterprise-grade performance. Routes typically start with 59.43.x.x. CN2 carries only a smaller portion of total traffic (around 10-15%), so it remains less congested. It is subdivided into:
  - **CN2 GT** (Global Transit): A cost-effective premium option with dedicated international exit paths but often shares domestic segments with ChinaNet (163). It offers better performance than CN1 but can still experience domestic congestion on return paths.
  - **CN2 GIA** (Global Internet Access): The highest-tier option with fully dedicated paths (both outbound and return), minimal hops, guaranteed low latency, almost no congestion, and the best stability. It is the most expensive, capacity-limited, and sensitive to attacks (e.g., DDoS often leads to null-routing).

**Comparison to global internet (typical Tier-1/Tier-2 routing outside China):**

| Aspect              | CN1 (ChinaNet / 163)                  | CN2 GT                               | CN2 GIA                              | Typical Global Internet (e.g., US/EU Tier-1 routes) |
|---------------------|---------------------------------------|--------------------------------------|--------------------------------------|-----------------------------------------------------|
| **Primary Use**     | Mass consumer traffic, general access | Mid-tier premium, cost-effective enterprise | High-end enterprise, latency-critical apps | General global peering/transit                      |
| **Latency to China**| High (often 200-400+ ms from US/EU, peaks higher) | Medium (better than CN1, ~150-300 ms) | Low (often 100-200 ms or less from nearby regions) | Varies widely by distance/peering (50-300+ ms)     |
| **Congestion**      | Very high, especially peak hours      | Moderate (lighter load than CN1)     | Very low (utilization kept <50%)     | Generally low on well-peered routes                 |
| **Stability/Packet Loss** | Poor during peaks (5-10%+ loss common) | Good internationally, variable domestically | Excellent (near-zero loss in normal conditions) | Good to excellent on premium paths                  |
| **Cost**            | Low/cheapest                              | Medium                               | Very high (e.g., $100+/Mbps in some cases) | Varies, often lower than CN2 GIA                    |
| **Capacity/Share**  | Massive (85-90% of China Telecom traffic) | Smaller                              | Very limited                         | Massive globally                                    |
| **Best For**        | Budget access, non-critical apps      | Balanced performance/cost            | Gaming, VoIP, finance, real-time apps | General worldwide traffic                           |

**Key Takeaways:**

- CN1 provides broad, inexpensive access but performs significantly worse than typical global internet routes for cross-border traffic due to congestion.
- CN2 (especially GIA) often outperforms standard global routes when connecting to/from China, offering lower latency and higher reliability than many non-premium international paths — this is why premium VPS/CDN providers heavily market "CN2 GIA to China."
- Global internet routing is more decentralized and peering-rich, but accessing China specifically remains challenging without premium routes like CN2 due to China's unique exit points and policies.
- In 2025-2026, CN2 GIA/equivalent (including newer variants like CTGNet) remains the "gold standard" for low-latency China access, while CN1 remains the default for everyday use.

**References:**

- [https://www.dataplugs.com/en/direct-connection-to-china-cn2-gia-vs-cn2-gt-vs-as4134](https://www.dataplugs.com/en/direct-connection-to-china-cn2-gia-vs-cn2-gt-vs-as4134)
- [https://bandwagonhost.com/cn2gia-vps.php](https://bandwagonhost.com/cn2gia-vps.php)
- [https://www.jtti.cc/supports/655.html](https://www.jtti.cc/supports/655.html)
- [https://zhuanlan.zhihu.com/p/1898372841344304871](https://zhuanlan.zhihu.com/p/1898372841344304871)
- [https://github.com/china-net/Internationally-connected](https://github.com/china-net/Internationally-connected)
