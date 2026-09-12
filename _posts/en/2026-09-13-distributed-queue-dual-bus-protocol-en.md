---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distributed Queue Dual Bus Protocol
translated: false
type: note
---

**Question:** What is the Distributed Queuing Access Protocol (分布式排队访问协议) in DQDB?

**Answer:**

DQDB — **Distributed Queue Dual Bus** — is the IEEE 802.6 standard for Metropolitan Area Networks (MAN). Its core innovation is the **Distributed Queuing Access Protocol**, which coordinates how all nodes share the two buses without a central controller. Here's how it works:

---

### 1. Physical Architecture

DQDB uses two unidirectional buses that carry data in opposite directions, with bandwidth allocated via time slots, supporting data, video, and voice. A "Head of Bus" (HOB) at each end generates time-division multiplexed slots, each marked as either busy or empty.

---

### 2. The Distributed Queue Mechanism

The key insight: **nodes form a virtual global queue without any central arbiter**. Each node uses two counters:

**REQUEST Counter (RC)**
Each station monitors busy bits and request bits on both buses — incrementing a counter for each received request bit and decrementing it for each received empty slot.

**COUNTDOWN Counter (CD)**
When a station wishes to transmit on Bus A, the current count in the Bus A request counter is transferred to a Bus A countdown counter (resetting the request counter), and a reservation request is inserted into the first available slot on Bus B. The countdown counter is decremented for each empty slot passing the station on Bus A. When it reaches zero, the station seizes the next empty time slot on Bus A for its data segment.

All stations simultaneously carry on this counting process for each direction of transmission — which is precisely why the system is called the "distributed queue dual bus."

---

### 3. Priority Levels

Each node maintains three (or four) sets of REQUEST and COUNTDOWN counters for different priority levels. Higher-priority request bits influence how the counters behave, enabling priority-based transmission ordering.

---

### 4. The Fairness Problem & Bandwidth Balancing

Under heavy load, DQDB distributes traffic among nodes in a highly asymmetrical manner — the station which first starts transmission obtains the largest share of available bandwidth, and service quality depends on propagation delay between stations.

To compensate for this unfairness, the IEEE 802.6 standard recommends a Bandwidth Balancing (BWB) mechanism.

---

### Summary Table

| Component | Role |
|---|---|
| Bus A / Bus B | Two opposite-direction data channels |
| Head of Bus (HOB) | Generates empty time slots |
| REQUEST Counter | Tracks how many nodes are ahead in queue |
| COUNTDOWN Counter | Counts down until the node's turn to transmit |
| REQUEST bit (on opposite bus) | Used to signal intention to transmit |
| Bandwidth Balancing | Corrects unfairness under heavy load |

---

**References:**
- [Distributed-queue dual-bus — Wikipedia](https://en.wikipedia.org/wiki/Distributed-queue_dual-bus)
- [IEEE 802.6 (DQDB) — GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/ieee-802-6-dqdb/)
- [Distributed Queue Dual Bus (DQDB) — Academia.edu](https://www.academia.edu/72986514/Distributed_Queue_Dual_Bus_DQDB_)
- [DQDB Networks with and without Bandwidth Balancing — ResearchGate](https://www.researchgate.net/publication/3158058_DQDB_Networks_with_and_without_Bandwidth_Balancing)
