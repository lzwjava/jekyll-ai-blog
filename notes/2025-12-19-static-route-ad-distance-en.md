---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Static Route Administrative Distance Default
translated: false
type: note
---

**B) 1**

In Cisco routers (the most common context for this question in networking certifications like CCNA), the default administrative distance (AD) for a static route is **1**. AD ranks the trustworthiness of routing sources—lower values are preferred.

- Connected interfaces have AD 0 (most preferred).
- Static routes have AD 1 (preferred over dynamic protocols).
- For comparison: OSPF is 110, RIP is 120.

This is why static routes override dynamically learned routes to the same destination unless the static route's AD is manually increased (e.g., for floating static backups).

Evidence from reliable sources:

- Cisco official documentation and community confirm static routes default to AD 1.
- Standard AD tables list: Static = 1, OSPF = 110, RIP = 120.

Options C (110) and D (120) are defaults for OSPF and RIP, respectively, while A (0) is for directly connected networks.
