---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transport Layer Duplex Modes Explained
translated: false
type: note
---

Question: Why does the Transport Layer generally use full-duplex service, but can occasionally use half-duplex service?

Answer:

**Transport Layer Communication Modes**

The correct answer is **B** — generally full-duplex, with half-duplex in certain cases.

---

**What These Modes Mean**

```
Full-Duplex:   A ←————————→ B   (simultaneous, both directions)
Half-Duplex:   A ←——————— B     (one direction at a time)
               A ———————→ B
Simplex:       A ———————→ B     (one direction only, forever)
```

---

**Why Full-Duplex is the General Case**

Most transport layer protocols are designed for **simultaneous bidirectional** data flow:

| Scenario | Example | Why Full-Duplex? |
|----------|---------|-----------------|
| Web browsing | TCP (HTTP/HTTPS) | Client sends requests while receiving data |
| File transfer | TCP (FTP) | ACKs flow back while data flows forward |
| Video call | TCP/UDP | Audio/video stream both ways simultaneously |
| Email | TCP (SMTP) | Server sends status codes while client sends mail |

TCP is the classic example — it maintains **separate send/receive buffers** and **independent sequence numbers** for each direction, making it inherently full-duplex.

---

**Why Half-Duplex is Sometimes Used**

Certain application scenarios don't need simultaneous bidirectional flow:

```
Example 1: Simple request-response
  Client:  "Give me file X"  →→→→→→→→→  Server
  Client:  ←←←←←←←←←  "Here is file X"  Server
  (never truly simultaneous — no need for full-duplex overhead)

Example 2: Early/simple protocols
  Walkie-talkie style apps, some legacy industrial protocols
```

Also, the **underlying network** sometimes constrains the transport layer — if a physical link is half-duplex, the transport layer must adapt.

---

**Why NOT "Only Full-Duplex" (ruling out A)**

> Saying *only* full-duplex is too absolute. Standards and real-world implementations allow flexibility for efficiency or hardware constraints.

**Why NOT "Only Half-Duplex" (ruling out C)**

> The overwhelming majority of modern transport-layer usage (TCP especially) is full-duplex. Half-duplex is the exception, not the rule.

---

**Memory Trick:**

> *"Transport Layer is like a highway: normally* ***two lanes go both ways simultaneously*** *(full-duplex), but on a narrow bridge, cars take turns* ***(half-duplex)***."*

References:
- [RFC 793 – Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc793)
- [Computer Networks – Tanenbaum, Chapter 6: Transport Layer](https://www.pearson.com/en-us/subject-catalog/p/computer-networks/P200000003217)