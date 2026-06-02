---
audio: false
generated: true
image: false
lang: en
layout: post
title: Policy Drives Inter-AS Routing
translated: false
type: note
---

Question: The scale of the Internet is so large that routing between autonomous systems is very difficult, so inter-AS routing prioritizes ().

Answer:

**策略** (policy) / **策略优先** / **政策优先**

**Explanation:**

Internet is composed of thousands of independent **Autonomous Systems (AS)**, each belonging to different organizations (ISPs, universities, large companies, content providers, etc.), and each having its own commercial interests, security requirements, cost considerations, and business relationships (customer, peer, provider).

Because of these differences, **path selection between ASes cannot simply use the shortest path or best performance metrics** (like in intra-domain routing protocols such as OSPF/IS-IS). Instead, the most important factor is usually **routing policy** (or routing strategy / policy-based routing).

**BGP (Border Gateway Protocol)** — the de facto standard for inter-domain routing — is fundamentally a **policy-based** routing protocol. Its main job is not to find the technically "best" path, but to allow each AS to implement its own **preferred policies**, such as:

- Prefer customer routes over peer routes over provider routes
- Avoid transiting traffic for free (peering disputes)
- Prefer cheaper links
- Prefer paths that avoid certain countries/regions for security or legal reasons
- Enforce traffic engineering goals
- Blackhole or filter specific prefixes for security

Therefore, the correct answer is **策略** (policy) or **政策** (policy), and the most common phrasing in Chinese textbooks and exams is:

**自治系统之间的路由选择是策略优先**
or
**策略优先** / **政策优先**

**References:**

- None (standard computer networking knowledge, BGP core concept)
