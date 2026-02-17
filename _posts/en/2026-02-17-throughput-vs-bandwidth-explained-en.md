---
audio: false
generated: true
image: false
lang: en
layout: post
title: Throughput vs Bandwidth Explained
translated: false
type: note
---

Question: What is the term for the amount of data that passes through a specific network, channel, or interface within a unit of time?

Answer: The correct term is **Throughput (吞吐量)**.

While it is often confused with **Bandwidth**, there is a subtle but important distinction between the two:

### Key Definitions

* **Throughput (吞吐量):** The *actual* amount of data that successfully travels through a system in a given period (e.g., bits per second). It reflects the real-world performance of the network.
* **Bandwidth (带宽):** The *maximum* theoretical capacity of a channel. Think of it as the width of a pipe, whereas throughput is the actual amount of water flowing through it at any given moment.

---

### Factors Affecting Throughput

Several variables can cause the actual throughput to be lower than the rated bandwidth:

1. **Network Congestion:** Too many users competing for the same resources.
2. **Hardware Limitations:** Processing power of routers, switches, or network interface cards.
3. **Transmission Errors:** Data packets that are lost or corrupted and must be re-sent.
4. **Protocol Overhead:** The "extra" data required for addressing and controlling the transmission (like headers in TCP/IP).

### Comparison Table

| Feature | Bandwidth | Throughput |
| --- | --- | --- |
| **Nature** | Theoretical Maximum | Actual Performance |
| **Analogy** | Number of lanes on a highway | Number of cars actually passing a point |
| **Unit** | bps (bits per second) | bps (bits per second) |

Would you like me to explain how to calculate the effective throughput for a specific network protocol?

References:

* [Throughput - Wikipedia]()
* [Difference between Bandwidth and Throughput]()