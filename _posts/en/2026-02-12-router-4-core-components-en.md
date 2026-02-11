---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Router’s Four Core Components
translated: false
type: note
---

Question: From the perspective of functional structure, a router includes input ports, output ports, routing processor, and which of the following components?

A. Routing control  
B. Interface  
C. Switching fabric  
D. A/D conversion  

Answer:  

**The correct answer is C. Switching fabric**

**Detailed Explanation:**

A modern router's **functional architecture** (also called its internal structure or building blocks) is typically composed of four main parts:

1. **Input ports** (输入端口)  
   - Physical interfaces that receive incoming packets from the network.  
   - Perform Layer 1–2 functions (physical reception, link-layer processing).  
   - Often include line cards with PHY, MAC, and initial packet lookup/processing.

2. **Output ports** (输出端口)  
   - Physical interfaces that transmit outgoing packets to the next hop.  
   - Handle queuing, scheduling, and transmission.

3. **Routing processor** (路由处理器 / 路由引擎 / control plane)  
   - Runs the routing protocols (OSPF, BGP, RIP, etc.).  
   - Maintains the routing table (RIB – Routing Information Base).  
   - Computes the forwarding table (FIB – Forwarding Information Base).  
   - Distributes forwarding decisions to the line cards / ports.

4. **Switching fabric** (交换结构 / 交换矩阵 / switching fabric / backplane / interconnect)  
   - The **internal high-speed interconnect** that moves packets from input ports to output ports.  
   - This is the **data plane forwarding engine** — the actual hardware path that packets take inside the router after the forwarding decision is made.  
   - Common types: shared memory, crossbar switch, multistage interconnection network (e.g., Clos network), etc.  
   - Without the switching fabric, packets cannot be transferred from input to output at high speed.

**Why the other options are incorrect:**

- **A. Routing control**  
  → Vague term. Routing control is part of the **routing processor** (control plane), not a separate structural component. This is not one of the standard four blocks of a router.

- **B. Interface**  
  → Interfaces are already covered by **input ports** and **output ports**. "Interface" is too general and not listed as a distinct fourth component in standard router architecture.

- **D. A/D conversion** (Analog-to-Digital conversion)  
  → This belongs to physical layer hardware (e.g., in modems or optical transceivers), **not** a functional block of a router’s packet-forwarding architecture.

**Standard textbook / exam model of router structure (very frequently tested):**

Router =  
- Input ports  
- Output ports  
- Switching fabric (交换结构)  
- Routing processor (路由处理器)

**Your answer A was incorrect because "路由控制" is not a standard separate component — it is a function performed inside the routing processor.**

Correct answer: **C. Switching fabric (交换结构)**

References:  

- None (standard router architecture from "Computer Networking: A Top-Down Approach" by Kurose & Ross, Cisco CCNA/CCNP materials, and common Chinese network engineering certification textbooks)