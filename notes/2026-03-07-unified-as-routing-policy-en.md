---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unified AS Routing Policy
translated: false
type: note
---

**Question:** What term fills the blank — an Autonomous System (AS) may use multiple internal routing protocols and metrics, but it presents a ________ and consistent routing policy to other ASes?

**Answer:**

The answer is **单一的 (single / unified)**.

---

### Explanation

An **Autonomous System (AS)** is defined as a collection of IP networks and routers under the control of a single administrative entity. The key principle is:

**Internally**, an AS can be very complex:

- It may run multiple Interior Gateway Protocols (IGPs) such as OSPF, EIGRP, RIP, or IS-IS.
- It can use different metrics (hop count, bandwidth, delay, cost, etc.) for internal route selection.
- It can have thousands of routers with varying configurations.

**Externally**, however, an AS must present itself as a single, unified entity:

- An autonomous system (AS) is a large network or group of networks that has a **unified routing policy**. Every computer or device that connects to the Internet is connected to an AS.

- An Autonomous System (AS) is a collection of IP networks and routers under the control of a single entity, **presenting a unified routing policy to the internet**.

- An AS is a network or a collection of connected IP routing prefixes under the control of one or multiple network operators that **present a common routing policy to the internet**.

This "single/unified" routing policy is what the AS advertises to other ASes via **BGP (Border Gateway Protocol)** — the exterior gateway protocol used between different ASes on the Internet.

### Why is this important?

| Aspect | Internal (Inside AS) | External (To other ASes) |
| --- | --- | --- |
| Routing Protocol | Multiple IGPs (OSPF, RIP, EIGRP…) | Single EGP (BGP) |
| Routing Policy | Can vary by region/department | One unified policy |
| Metrics | Different per protocol | Abstracted into BGP attributes |
| Identity | Many routers, many subnets | One ASN (e.g., AS13335) |

Policy decisions (such as preferring certain network paths, accepting or rejecting routes from specific sources) **remain internal to the AS and invisible to external systems**. This is what allows the Internet to scale — each AS handles its own internal complexity and only exposes a clean, single routing policy outward.

**Therefore, the blank should be filled with: 单一的 (single)**

---

**References:**

- [Cloudflare — What is an Autonomous System?](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/)
- [Kentik — BGP Routing Tutorial](https://www.kentik.com/kentipedia/bgp-routing/)
- [CacheFly — BGP Routing Guide](https://www.cachefly.com/news/a-guide-to-border-gateway-protocol-bgp-routing-and-its-applications/)
- [JumpCloud — What is an Autonomous System?](https://jumpcloud.com/it-index/what-is-an-autonomous-system-as)
