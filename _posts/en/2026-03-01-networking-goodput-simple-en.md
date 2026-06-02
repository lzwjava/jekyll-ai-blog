---
audio: false
generated: true
image: false
lang: en
layout: post
title: Networking Goodput Explained Simply
translated: false
type: note
---

**Question:** What does "goodput" mean in networking?

**Answer:**

**Goodput** refers to the **actual useful data** successfully delivered to the application layer (or end user) per unit of time in a network connection.

It measures only the **application payload data** that is:
- Correctly received
- In the right order
- Without errors
- Without duplicates
- After removing all protocol overhead and useless/retransmitted data

### Goodput vs. related terms

- **Throughput**
  → Total number of bits successfully transmitted over the link per second (includes protocol headers, retransmissions, etc.)

- **Goodput**
  → Only the **useful application data** that the receiver actually uses (excludes headers, control packets, retransmitted data, duplicate packets, etc.)

- **Bandwidth**
  → Theoretical maximum capacity of the link

### Typical relationship (in decreasing order)

Bandwidth ≥ Throughput ≥ Goodput

### Practical examples

| Scenario                              | Throughput | Goodput     | Difference explanation                              |
|---------------------------------------|------------|-------------|------------------------------------------------------|
| Clean HTTP/2 download, no loss        | ~980 Mbps  | ~940 Mbps   | Mainly HTTP/2 + TLS headers                          |
| TCP connection with 5% packet loss    | 600 Mbps   | 380 Mbps    | Many retransmissions consume bandwidth               |
| Video streaming with lots of FEC      | 25 Mbps    | 18 Mbps     | Forward Error Correction packets don't carry payload |
| VPN tunnel (high overhead)            | 850 Mbps   | 620 Mbps    | IPsec/ESP + inner IP + TCP/UDP headers               |
| File transfer over very lossy Wi-Fi   | 40 Mbps    | 8 Mbps      | Extremely high retransmission rate                   |

### Summary – most common way people remember it

**Goodput = Throughput – useless traffic**
(useless = protocol headers + retransmissions + control packets + duplicates + padding + FEC overhead that didn't help)

In performance-sensitive applications (file transfer, video streaming, gaming, real-time protocols), engineers care much more about **goodput** than raw throughput.

**References:**

- None required for this conceptual explanation
