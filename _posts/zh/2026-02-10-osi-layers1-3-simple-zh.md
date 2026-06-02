---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: OSI 第 1–3 层简单详解
translated: true
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

The correct answer is **C. Node-to-node layers**。

**Explanation:**

在 OSI Reference Model (OSI/RM) 中，七层结构根据其通信范围被分为两大组：

- **Node-to-node layers**（也称为 point-to-point layers 或 hop-by-hop layers）：
  这些层负责**相邻网络设备之间**的通信（一次一跳）。
  - **Physical layer** (Layer 1)
  - **Data Link layer** (Layer 2)
  - **Network layer** (Layer 3)

  → 这三层统称为 **node-to-node layers**（或 **point-to-point layers** / **结点到结点层**）。

- **End-to-end layers**（也称为 host-to-host layers）：
  这些层负责**从源主机到目标主机**的通信，无论中间经过多少个设备（routers, switches）。
  - **Transport layer** (Layer 4)
  - **Session layer** (Layer 5)
  - **Presentation layer** (Layer 6)
  - **Application layer** (Layer 7)

  → 这四层统称为 **end-to-end layers**（端到端层）。

**Why not D (Intermediate system layer)?**
"Intermediate system" 是 ISO 术语中主要用于指代 routers（工作在 Layer 3 — Network layer 的设备）的词汇。在 OSI 教学材料或教科书中，它**不是** Layer 1–3 这一组层的标准名称。

**Summary table:**

| Group              | Layers involved                  | Scope of responsibility       | Chinese name     |
|--------------------|----------------------------------|-------------------------------|------------------|
| Node-to-node       | Physical + Data Link + Network   | Between adjacent nodes (one hop) | 结点到结点层     |
| End-to-end         | Transport + Session + Presentation + Application | From source host to destination host | 端到端层         |

因此，physical layer, data link layer, 和 network layer 被正确地称为 **node-to-node layers** → 选项 **C**。

References:

- None (standard OSI model knowledge; widely consistent across textbooks and certification materials such as CCNA, CompTIA Network+, and Chinese computer network textbooks)
