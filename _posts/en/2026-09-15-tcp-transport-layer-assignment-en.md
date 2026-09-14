---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Transport Layer Assignment
translated: false
type: note
---

Question: Which layer does the TCP protocol belong to — Network layer or Transport layer?

Answer: TCP (Transmission Control Protocol) belongs to the **Transport Layer** (Layer 4) of the OSI model.

Here's a quick breakdown to clarify the distinction:

| Layer | OSI Model | Protocols |
|-------|-----------|-----------|
| Layer 3 | Network Layer | IP, ICMP, ARP |
| Layer 4 | Transport Layer | **TCP**, UDP |

**Why Transport Layer?**

- TCP is responsible for **end-to-end communication** between processes on different hosts, not routing between networks.
- It provides **reliability** (acknowledgments, retransmission), **flow control**, **congestion control**, and **ordered delivery** — all Transport Layer concerns.
- The **Network Layer** (Layer 3) handles logical addressing and packet routing (that's IP's job). TCP rides *on top of* IP.

A common mnemonic for the two working together: **IP** gets packets to the right *machine*, **TCP** gets data to the right *process* on that machine reliably.

References:

- [TCP - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Glossary/TCP)
- [OSI Model - Cloudflare](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)
