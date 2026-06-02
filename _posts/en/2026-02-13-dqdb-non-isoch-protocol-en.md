---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: DQDB Non-Isochronous Protocol Answer
translated: false
type: note
---

Question: In the DQDB dual bus subnet, which media access control protocol is specified to provide non-isochronous services?

A. Carrier Sense Multiple Access
B. Pre-arbitrated Access
C. Distributed Queue Access
D. Time Division Multiple Access

Your answer: D
Correct answer: C

Answer:

**Correct answer is C – Distributed Queue Access (分布式排队访问)**

**Explanation:**

DQDB (Distributed Queue Dual Bus) is a metropolitan area network (MAN) standard defined in IEEE 802.6. It uses two unidirectional buses (forward and reverse bus) and is designed to support both **isochronous** (time-sensitive, constant bit rate) and **non-isochronous** (asynchronous, variable bit rate) traffic.

In DQDB, there are two main media access control mechanisms:

- **QA (Queued Arbitrated) slots** → use **Distributed Queue Access** protocol
  → mainly used for **non-isochronous** (connectionless, best-effort, asynchronous) services, such as data traffic, LAN-like communication, file transfer, etc.

- **PA (Pre-Arbitrated) slots** → use pre-assigned fixed slots
  → mainly used for **isochronous** services (constant bit rate, delay-sensitive), such as voice and video.

Therefore:

- The protocol that provides **non-isochronous services** in DQDB is **Distributed Queue Access** (分布式排队访问), which corresponds to option **C**.

**Why the other options are incorrect:**

- **A. Carrier Sense Multiple Access (CSMA)**
  This is the access method used in Ethernet (IEEE 802.3), not in DQDB.

- **B. Pre-arbitrated Access**
  This exists in DQDB, but it is used for **isochronous** services, not non-isochronous.

- **D. Time Division Multiple Access (TDMA)**
  While DQDB uses slot-based access (similar in concept to TDMA), the specific mechanism name for non-isochronous traffic in DQDB is **Distributed Queue Access**, not simply called TDMA.

**Summary:**

DQDB dual-bus subnet → non-isochronous services → **Distributed Queue Access (QA protocol)** → correct answer is **C**.

References:

- IEEE 802.6 standard (DQDB) documentation
- Computer network textbooks covering MAN standards (e.g., Tanenbaum, Kurose & Ross, etc.)
