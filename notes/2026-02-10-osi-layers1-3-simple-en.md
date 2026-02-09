---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: OSI Layers 1–3 Explained Simply
translated: false
type: note
---

Question: In the OSI Reference Model, the physical layer, data link layer, and network layer are collectively called  
A. End-to-end layers  
B. Node-to-end layers  
C. Node-to-node layers  
D. Intermediate system layers  

Your answer: D  
Correct answer: C  

Answer:  

The correct answer is **C. Node-to-node layers**.

**Explanation:**

In the OSI Reference Model (OSI/RM), the seven layers are divided into two major groups based on their scope of communication:

- **Node-to-node layers** (also called point-to-point layers or hop-by-hop layers):  
  These layers are responsible for communication **between adjacent network devices** (one hop at a time).  
  - **Physical layer** (Layer 1)  
  - **Data Link layer** (Layer 2)  
  - **Network layer** (Layer 3)  

  → These three layers together are called **node-to-node layers** (or **point-to-point layers** / **结点到结点层** in Chinese).

- **End-to-end layers** (also called host-to-host layers):  
  These layers are responsible for communication **from the source host to the destination host**, regardless of how many intermediate devices (routers, switches) are crossed.  
  - **Transport layer** (Layer 4)  
  - **Session layer** (Layer 5)  
  - **Presentation layer** (Layer 6)  
  - **Application layer** (Layer 7)  

  → These four layers together are called **end-to-end layers** (端到端层).

**Why not D (Intermediate system layer)?**  
"Intermediate system" is a term mainly used in ISO terminology to refer to routers (devices that operate at Layer 3 — the network layer). It is **not** the standard name for the group of layers 1–3 in OSI teaching materials or textbooks.

**Summary table:**

| Group              | Layers involved                  | Scope of responsibility       | Chinese name     |
|--------------------|----------------------------------|-------------------------------|------------------|
| Node-to-node       | Physical + Data Link + Network   | Between adjacent nodes (one hop) | 结点到结点层     |
| End-to-end         | Transport + Session + Presentation + Application | From source host to destination host | 端到端层         |

So the physical layer, data link layer, and network layer are correctly called **node-to-node layers** → answer **C**.

References:  

- None (standard OSI model knowledge; widely consistent across textbooks and certification materials such as CCNA, CompTIA Network+, and Chinese computer network textbooks)