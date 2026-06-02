---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: RIP Protocol Metaphor for Company Culture
translated: false
type: note
---

Question: Does the Routing Information Protocol (RIP) work in such a way that bad news travels fast and good news travels slow, as Ben Horowitz put it?

Answer:

Yes, Ben Horowitz famously used the Routing Information Protocol (RIP) as a metaphor in his book *The Hard Thing About Hard Things* to describe a healthy company culture: **bad news travels fast; good news travels slow**.

### Ben Horowitz's Metaphor

Horowitz recommends building a company culture where problems (bad news) are shared quickly and openly so they can be addressed immediately, while successes (good news) spread more gradually. He explicitly compares this ideal to the "old RIP routing protocol," emphasizing that in a good organization, critical issues surface rapidly without fear of punishment.

### How RIP Actually Works

RIP is a classic **distance-vector routing protocol** (using the Bellman-Ford algorithm). Key behaviors relevant to the "news" propagation:

- **Triggered updates (flash updates)**: When a router detects a change in its routing table—especially a route becoming worse (higher metric) or unreachable (e.g., a link failure)—it immediately sends an update to neighbors, without waiting for the regular 30-second timer. This propagates **bad news** (route failures or degradations) quickly across the network.

- **Good news (better routes)**: Improvements, such as a new lower-cost route, are typically advertised only during periodic updates every 30 seconds. There is no immediate triggered update for improvements in most implementations. Thus, **good news travels slow**.

This asymmetry helps accelerate convergence on failures (bad news) while routine better paths propagate normally.

However, RIP is well-known for **slow overall convergence**, especially in cases of route failures leading to the "count-to-infinity" problem, where invalid routes persist until the metric reaches infinity (16 in RIP). Despite this major drawback, the triggered update mechanism for worsening routes supports the idea that bad news can spread faster than good news in certain scenarios.

Horowitz's analogy uses this protocol characteristic to illustrate the value of rapid bad-news sharing in organizations.

References:

- [Goodreads - Ben Horowitz Quotes](https://www.goodreads.com/author/quotes/7155094.Ben_Horowitz?page=3)
- [AnandTech Forums - Discussion on RIP behavior](https://forums.anandtech.com/threads/count-to-infinity.2460100/)
- [Noction Blog - BGP path hunting (comparing to RIP)](https://www.noction.com/blog/bgp-path-hunting)
- [Wikipedia - Routing Information Protocol](https://en.wikipedia.org/wiki/Routing_Information_Protocol)
