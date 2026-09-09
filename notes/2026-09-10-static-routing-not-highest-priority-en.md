---
audio: false
generated: true
image: false
lang: en
layout: post
title: Static Routing Not Highest Priority
translated: false
type: note
---

**Question:** In a routing table, does static routing have the highest priority?

**Answer:**

No, static routing does **not** always have the highest priority. Route priority is determined by **Administrative Distance (AD)** — a lower AD value means higher priority.

Here is the typical AD priority order (on Cisco IOS, for example):

| Route Type | Administrative Distance |
| --- | --- |
| **Connected Interface** | **0** ← Highest Priority |
| **Static Route** | **1** |
| EIGRP Summary | 5 |
| External BGP (eBGP) | 20 |
| Internal EIGRP | 90 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| External EIGRP | 170 |
| Internal BGP (iBGP) | 200 |
| Unknown / Unreachable | 255 ← Lowest Priority |

**Key points:**

- **Connected routes (AD = 0)** have the highest priority — they are directly attached interfaces and are always preferred.
- **Static routes (AD = 1)** come second, which is very high but not the highest.
- Dynamic routing protocols (OSPF, RIP, BGP, etc.) all have higher AD values, meaning lower priority than static routes.
- If a static route and a dynamic route exist for the same destination, the **static route wins** (AD 1 vs. 110+ for OSPF, etc.).

**Summary:** Connected routes > Static routes > Dynamic routing protocols.

---

**References:**

- [Cisco - Administrative Distance](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/15986-admin-distance.html)
- [Cloudflare - What is a Routing Table?](https://www.cloudflare.com/learning/network-layer/what-is-a-routing-table/)
