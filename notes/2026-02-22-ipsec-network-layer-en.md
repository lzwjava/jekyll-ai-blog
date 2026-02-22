---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPsec at the Network Layer
translated: false
type: note
---

Question: At which layer does the IPsec secure communication mechanism operate?

Answer: 

IPsec (Internet Protocol Security) operates at the **Network Layer** (Layer 3) of the OSI model.

Key characteristics of IPsec at this layer include:
*   **Transparency:** Because it works at the network layer, IPsec is transparent to upper-layer protocols (like TCP and UDP) and applications. Applications do not need to be modified to use IPsec.
*   **Scope:** It secures all traffic passing between two endpoints (hosts or gateways) regardless of the specific application generating the traffic.
*   **Functionality:** It provides services such as data confidentiality (encryption), data integrity, data origin authentication, and anti-replay protection for IP packets.
*   **Modes:** It operates in two modes:
    *   **Transport Mode:** Encrypts only the payload of the IP packet (used mostly for host-to-host communication).
    *   **Tunnel Mode:** Encrypts the entire original IP packet, including the header, and encapsulates it in a new IP packet (used mostly for gateway-to-gateway or site-to-site VPNs).

This distinguishes it from security protocols like TLS/SSL, which operate at the Transport Layer (Layer 4) or Session/Presentation layers, and require application-level integration or specific proxy configurations.

References:

- [RFC 4301: Security Architecture for the Internet Protocol](https://datatracker.ietf.org/doc/html/rfc4301)