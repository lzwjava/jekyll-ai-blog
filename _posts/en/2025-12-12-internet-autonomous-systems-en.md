---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Internet Autonomous Systems Explained
translated: false
type: note
---

Question: What are autonomous systems (AS) on the Internet?

Answer:

Autonomous Systems (AS) are the fundamental building blocks of the Internet, consisting of large networks or groups of networks under the control of a single administrative entity (such as an ISP, university, corporation, or government agency). Each AS manages a collection of IP routing prefixes and operates with a unified, clearly defined routing policy that determines how it exchanges traffic with other ASes.

Key aspects include:

- **Autonomous System Number (ASN)**: Every public AS is identified by a unique ASN, assigned by Regional Internet Registries (RIRs) under the oversight of IANA. Originally 16-bit (up to 65,535), they expanded to 32-bit in 2007 to accommodate growth, now exceeding 100,000 allocated ASNs.

- **Role in Routing**: ASes use the Border Gateway Protocol (BGP) to announce their IP address spaces and exchange routing information with neighboring ASes. Data packets travel across the Internet by hopping between ASes until reaching the destination AS, which then delivers internally.

- **Types of ASes**:
  - **Stub/Single-homed**: Connected to only one other AS (often end-user networks).
  - **Multihomed**: Connected to multiple ASes for redundancy, but not transiting traffic.
  - **Transit**: Carries traffic between other ASes (common for ISPs).

This decentralized structure allows the global Internet to function as a "network of networks," enabling efficient, policy-based routing without a single central authority.

References:

- [What is an autonomous system? | Cloudflare](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/)
- [Autonomous system (Internet) - Wikipedia](https://en.wikipedia.org/wiki/Autonomous_system_%28Internet%29)
- [Autonomous System Numbers - ARIN](https://www.arin.net/resources/guide/asn/)
- [What are autonomous systems and how do they work? | TechTarget](https://www.techtarget.com/searchnetworking/definition/autonomous-system)
