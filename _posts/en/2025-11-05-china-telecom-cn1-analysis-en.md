---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: China Telecom CN1 Network Analysis
translated: false
type: note
---

Based on the traceroute you shared from a Meiyijia convenience store WiFi in Guangzhou, this appears to be using China Telecom's standard ChinaNet backbone (often referred to as CN1), not the premium CN2 network. Here's a quick breakdown of why:

### Key Indicators from the Traceroute

- **Hops 5–10 (China Telecom backbone)**: IPs like 14.147.135.198, 183.56.34.41, 202.97.93.89–202.97.116.210, and 203.215.237.42 are all part of AS4134 (ChinaNet), China Telecom's main domestic/international backbone. These are common on standard broadband lines.
  - 202.97.x.x range is specifically ChinaNet (not CN2).
  - 203.215.237.42 is located in Xiamen, Fujian (still within China), owned by CHINANET Fujian Province Network (AS4134).
- **No CN2 signatures**: CN2 (AS4809) typically shows IPs in ranges like 59.43.0.0/16 or 121.59.0.0/16 during the backbone phase. Your trace doesn't hit any of those.
- **Exit path**: Traffic exits China via a standard ChinaNet handoff to Microsoft (Azure) in Tokyo (hop 11: 104.44.235.92), then routes south to Singapore (hops 14–15). This is a common, non-optimized path for basic China Telecom connections—detouring through Japan adds ~300ms latency, which aligns with CN1 congestion. CN2 often uses direct Hong Kong or shorter Asia-Pacific exits for lower latency (~150–200ms to GitHub from Guangzhou).
- **Context**: Meiyijia stores in Guangzhou usually run on China Telecom's consumer/commercial broadband, which defaults to ChinaNet (CN1) unless explicitly upgraded to CN2 GIA (a paid enterprise add-on).

### CN1 vs. CN2 Quick Comparison

| Aspect          | CN1 (ChinaNet)                          | CN2 (Premium)                          |
|-----------------|-----------------------------------------|----------------------------------------|
| **AS Number**   | AS4134                                 | AS4809                                |
| **Typical Latency to GitHub (from Guangzhou)** | 250–400ms (congested, indirect routes) | 100–200ms (optimized, direct exits)   |
| **IP Ranges**   | 202.97.x.x, 183.56.x.x, etc.           | 59.43.x.x, 121.59.x.x, etc.           |
| **Use Case**    | Standard home/business broadband       | VPS/cloud/enterprise (extra cost)     |
| **Path Style**  | Often detours (e.g., via Japan/Korea)  | Direct to HK/US/Asia hubs             |

If you want to confirm or test further:

- Run `traceroute github.com` during peak hours (e.g., evenings) to check for more congestion.
- Ping a CN2 test site like `www.cn2.net`—if latency is under 200ms, you might have partial CN2 access.
- Contact Meiyijia or China Telecom support for your line type (mention "CN2 GIA" if upgrading).

[China Telecom CN2 Overview](https://www.ctamericas.com/company/global-network/cn2/)
[IPinfo for 203.215.237.42](https://ipinfo.io/203.215.237.42)
[CN2 vs ChinaNet Guide](http://chihengcloud.com/en/blog/cloudservice/what-is-cn2-network-a-3-minute-guide-to-types-and-features/)
