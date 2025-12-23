---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: International Network Latency Explained
translated: false
type: note
---

Question: Why is there a large latency gap between hops 8 and 9 in the traceroute to twitter.com, and what is between them?

Answer: 

The large latency increase from hop 8 (around 10-20 ms) to hop 9 (around 197-199 ms) occurs because this is the point where traffic exits China's domestic network and enters international routes.

- Hops 1 through 9 are on China Telecom's backbone network (CHINANET, AS4134), using IP ranges like 202.97.x.x, which are allocated to China Telecom for their national infrastructure.
- Hop 10 (81.173.23.18) is the international gateway or peering point, likely located outside China (often in Europe or a transit hub), connecting to global networks.
- Subsequent hops (11-12) are on Cloudflare's network (using anycast IPs like 162.158.x.x and 162.159.x.x), which hosts twitter.com (now x.com).

The ~180 ms jump represents the added round-trip time for crossing international links, typically undersea cables from China to the US or other regions where Twitter/X servers are located. This is normal for traffic originating in mainland China accessing foreign sites, due to geographic distance and routing through limited international gateways. Congestion or prioritization on these links can also contribute to higher latency.

No specific intermediate hops are visible "between" 8 and 9 because traceroute only shows routers that respond to ICMP; the long-distance link itself doesn't add extra responding hops.

References:  

- [https://ipinfo.io/AS4134](https://ipinfo.io/AS4134)  
- [https://bgpview.io/prefix/202.97.32.0/24](https://bgpview.io/prefix/202.97.32.0/24)  
- [https://en.wikipedia.org/wiki/Great_Firewall](https://en.wikipedia.org/wiki/Great_Firewall)