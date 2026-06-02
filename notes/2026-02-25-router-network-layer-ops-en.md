---
audio: false
generated: true
image: false
lang: en
layout: post
title: Router Operates at Network Layer
translated: false
type: note
---

Question: In the OSI seven-layer reference model, routers and bridges are both network interconnection devices, but they operate at different layers. At which layer does a router operate?
A. Network Layer
B. Transport Layer
C. Session Layer
D. Application Layer

Answer:

## Answer: A — Network Layer

### Explanation

This question tests your understanding of where common network devices operate within the **OSI (Open Systems Interconnection) 7-layer model**.

---

### OSI Model Overview (Relevant Layers)

| Layer | Name | Example Devices |
|---|---|---|
| Layer 1 | Physical Layer | Hub, Repeater |
| Layer 2 | Data Link Layer | **Bridge**, Switch |
| Layer 3 | Network Layer | **Router** |
| Layer 4 | Transport Layer | Gateway (partial) |

---

### Key Comparison: Bridge vs. Router

| Feature | Bridge | Router |
|---|---|---|
| OSI Layer | **Layer 2 — Data Link Layer** | **Layer 3 — Network Layer** |
| Address Used | **MAC Address** (Physical Address) | **IP Address** (Logical Address) |
| Function | Forwards or filters **frames** within the same network | Forwards **packets** between different networks |
| Network Scope | Same LAN / network segment | Different networks / subnets |
| Intelligence | Less intelligent, simple forwarding | More intelligent, uses routing tables |

---

### Why Router Operates at the Network Layer

- The router reads the **destination IP address** in the packet header to make forwarding decisions.
- It uses **routing tables and protocols** (e.g., RIP, OSPF, BGP) to determine the best path.
- It can connect **heterogeneous networks** (different network architectures).
- Because IP addressing is a **Layer 3 (Network Layer)** function in the OSI model, routers are classified as Layer 3 devices.

---

### Why Option A is Correct

- **A (Network Layer)** ✅ — Routers operate here, using IP addresses to route packets.
- **B (Transport Layer)** ❌ — This layer handles end-to-end communication (TCP/UDP); no standard routing device works here.
- **C (Session Layer)** ❌ — Manages sessions between applications; no routing device operates here.
- **D (Application Layer)** ❌ — This is the topmost layer for user-facing protocols (HTTP, FTP, etc.).

---

### Summary

> A **bridge** works at the **Data Link Layer (Layer 2)** using **MAC addresses**, while a **router** works at the **Network Layer (Layer 3)** using **IP addresses**. This is a classic and frequently tested distinction in networking exams.
