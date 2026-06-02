---
audio: false
generated: true
image: false
lang: en
layout: post
title: Autonomous Systems Explained Simply
translated: false
type: note
---

**Question:** What is an Autonomous System (AS) in networking?

**Answer:**

## Definition

An Autonomous System (AS) is a collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators on behalf of a single administrative entity or domain, that presents a common and clearly defined routing policy to the Internet.

Think of it simply: the Internet is a network of networks, and autonomous systems are the big networks that make up the Internet. Every computer or device that connects to the Internet is connected to an AS.

---

## How It Works — Analogy

Imagine an AS as being like a town's post office. Mail goes from post office to post office until it reaches the right town, and that town's post office will then deliver the mail within that town. Similarly, data packets cross the Internet by hopping from AS to AS until they reach the AS that contains their destination IP address.

---

## Autonomous System Number (ASN)

Each AS is assigned a unique identifier called an Autonomous System Number (ASN). Network operators need ASNs to control routing within their networks and to exchange routing information with other ISPs.

There are two ASN formats:

- A **2-byte ASN** is a 16-bit number providing 65,536 ASNs. A **4-byte ASN** is a 32-bit number providing over 4 billion ASNs.
- As of 2025, there are roughly **120,000 allocated ASNs** worldwide.

---

## Types of Autonomous Systems

There are three different kinds of Autonomous Systems:

- **Multi-homed AS**: Connects to two or more ASes, maintaining Internet connectivity even if one connection fails.
- **Stub AS**: Connects to only one other AS, though it may have its own private connections not visible to the rest of the Internet.
- **Transit AS**: Acts as a link between two or more other ASes, allowing data to pass through it even from unassociated networks.

---

## Role of BGP

Networks within an AS communicate routing information using interior gateway protocols (IGPs). In contrast, communications between autonomous systems rely on a single exterior gateway protocol — **Border Gateway Protocol (BGP)** — which makes it possible to share routing information and efficiently route data packets between autonomous systems.

---

## Internal vs. External View

What sets the AS apart from other network groups is that it must appear to external autonomous systems as having a single, coherent routing plan, no matter how communications are carried out within the AS.

---

## Real-World Examples

ISPs are perhaps the most common example of entities that operate autonomous systems. Each ISP typically has its own ASN. Another example includes cloud service providers like Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP).

---

## Why ASes Matter

AS promotes stability in global routing, network fault isolation, and simplified administration for large networks, which ultimately contributes to better network performance and a consistent user experience.

---

**References:**

- [Cloudflare — What is an Autonomous System?](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/)
- [Wikipedia — Autonomous System (Internet)](https://en.wikipedia.org/wiki/Autonomous_system_(Internet))
- [TechTarget — What are Autonomous Systems?](https://www.techtarget.com/searchnetworking/definition/autonomous-system)
- [ARIN — Autonomous System Numbers](https://www.arin.net/resources/guide/asn/)
- [ControlD — What is an Autonomous System?](https://controld.com/blog/what-is-an-autonomous-system/)
