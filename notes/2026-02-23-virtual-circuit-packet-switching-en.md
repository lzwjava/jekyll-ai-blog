---
audio: false
generated: true
image: false
lang: en
layout: post
title: Virtual Circuit Packet Switching Explained
translated: false
type: note
---

Question: Packet switching can be divided into two types: datagram packet switching and ______ packet switching.

Answer:

Packet switching is a method of grouping data into packets that are transmitted over a digital network. It is primarily categorized into two distinct approaches based on how the connection is managed:

1.  **Datagram Packet Switching**: In this approach, each packet is treated independently as a separate entity. Each packet contains full destination information and may take different routes to reach the destination. Consequently, packets may arrive out of order, and it is the responsibility of the receiving end to reassemble them. This method is connectionless.
2.  **Virtual Circuit Packet Switching**: In this approach, a logical path (called a virtual circuit) is established between the source and destination before any data is transferred. All packets for a specific session follow this same predefined path. While no physical dedicated line is created (unlike circuit switching), the sequence of packets is preserved, and they arrive in order. This method is connection-oriented.

Therefore, the missing term is **virtual circuit**.

References:

- [Virtual Circuit vs. Datagram - GeeksforGeeks](https://www.geeksforgeeks.org/virtual-circuit-vs-datagram/)
- [Packet Switching - Wikipedia](https://en.wikipedia.org/wiki/Packet_switching)
