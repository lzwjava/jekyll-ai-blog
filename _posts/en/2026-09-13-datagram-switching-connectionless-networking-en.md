---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Datagram Switching: Connectionless Networking"
translated: false
type: note
---

Question: Does "datagram switching" (数据报交换) belong to the connectionless communication model?

Answer: Yes, datagram switching is a **connectionless** packet-switching technique. Here's why:

**How it works:**
- Each packet (datagram) is treated **independently**
- Every packet carries the **full destination address**
- Packets may travel via **different routes** through the network
- They may arrive **out of order** and must be reordered at the destination

**Why it's connectionless:**
- No dedicated path is established **before** data is sent
- No "handshake" or setup phase is required
- The network makes per-packet routing decisions on the fly
- There is **no state maintained** between sender and receiver at the network level

**Contrast with connection-oriented (virtual circuit switching):**

| Feature | Datagram (Connectionless) | Virtual Circuit (Connection-oriented) |
|---|---|---|
| Path setup | None | Required before transmission |
| Routing | Per packet | Per connection |
| Packet order | May vary | Preserved |
| Example | IP (Internet Protocol) | ATM, Frame Relay |

The classic example of datagram switching in practice is the **IP layer** of the Internet — packets are routed independently with no guaranteed order or delivery.

References:
- [Connectionless vs Connection-oriented – Forouzan, Data Communications and Networking](https://www.mheducation.com/highered/product/data-communications-networking-forouzan/M9780073376226.html)
- [Datagram vs Virtual Circuit – Techopedia](https://www.techopedia.com/definition/25449/datagram)
- [IP as a Connectionless Protocol – Cloudflare](https://www.cloudflare.com/learning/network-layer/internet-protocol/)
