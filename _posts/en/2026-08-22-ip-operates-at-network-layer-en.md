---
audio: false
generated: true
image: false
lang: en
layout: post
title: IP Operates at Network Layer
translated: false
type: note
---

Question: What OSI layer does the Internet Protocol (IP) operate on, given that it is a connectionless, unreliable packet transmission protocol responsible for routing and forwarding data?

Answer: IP operates at the **Network Layer** (Layer 3) of the OSI model.

Here's why:

- **Connectionless** — IP does not establish a dedicated connection before sending data. Each packet is routed independently.
- **Unreliable** — IP provides no guarantee of delivery, ordering, or error correction. That responsibility falls to higher layers (e.g., TCP at the Transport Layer).
- **Routing & Forwarding** — These are the core jobs of the Network Layer. Routers use IP addresses to determine the best path for each packet across interconnected networks.

**OSI Layer Mapping (for context):**

| Layer | Name | Examples |
|-------|------|---------|
| 7 | Application | HTTP, FTP, DNS |
| 6 | Presentation | TLS, JPEG |
| 5 | Session | NetBIOS |
| 4 | Transport | TCP, UDP |
| **3** | **Network** | **IP, ICMP, OSPF** |
| 2 | Data Link | Ethernet, Wi-Fi |
| 1 | Physical | Cables, Radio |

So the blank should be filled with: **网络（Network）层**

References:
- [OSI Model – Wikipedia](https://en.wikipedia.org/wiki/OSI_model)
- [Internet Protocol – Wikipedia](https://en.wikipedia.org/wiki/Internet_Protocol)
