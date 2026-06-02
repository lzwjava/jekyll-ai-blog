---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: OSI Layer Data Unit Terms
translated: false
type: note
---

Question: In the OSI Reference Model (OSI/RM), what is the term for the group of bits passed between entities at different layers?

Answer:

The correct answer is **A. 数据单元** (Data Unit).

**Detailed explanation in English:**

In the OSI Reference Model, communication between layers uses specific terminology:

- **Data Unit** (数据单元): General term for the block of bits (data + possibly control information) that is passed between entities in **adjacent layers** (i.e., from layer N to layer N-1 or vice versa).
  → This is the broadest and correct term for the question.

- **Protocol Data Unit (PDU)** (协议数据单元): The specific name for the data unit when it is exchanged **horizontally** between peer entities at the **same layer** on different systems, according to the rules (protocol) of that layer.

- **Service Data Unit (SDU)** (服务数据单元): The pure user data that a layer N entity receives from the layer above (layer N+1) before it adds its own header/trailer.

Key distinction in OSI terminology:

| Direction / Relationship       | Term used                     | Meaning                                      |
|-------------------------------|-------------------------------|----------------------------------------------|
| Between **adjacent layers** (N ↔ N-1) | **Data Unit** (数据单元)      | General term for bits passed up/down the stack |
| Between **peer entities** (same layer, different systems) | **Protocol Data Unit (PDU)** | Data unit exchanged according to layer protocol |
| From upper layer to current layer | **Service Data Unit (SDU)**   | User data delivered via service interface    |

The question specifically asks about bits passed **between entities of each layer** (各层的实体之间), which refers to the **vertical** communication between adjacent layers inside one system — therefore the correct general term is **数据单元 (Data Unit)**.

Why **C. 服务原语 (Service Primitive)** is wrong:
Service primitives (request, indication, response, confirm) are the **abstract interactions** at the service boundary (between a service user and service provider), **not** the actual bit groups being transferred.

Why **D. 服务访问点 (Service Access Point - SAP)** is wrong:
SAP is the **logical interface point** between layers (address-like identifier), not the data itself.

Why **B. 接口 (Interface)** is wrong:
Interface is the boundary or set of rules, not the data block being passed.

**Summary – correct mapping:**

- Bits passed **between layers** (adjacent) → **Data Unit**
- Bits passed **between peer protocol entities** → **PDU**
- Bits passed **between service user and service provider** → **SDU** (from upper to lower) or encapsulated PDU (from lower to upper)

Therefore the correct answer for this question is **A. 数据单元**.

References:

- None needed (standard OSI reference model terminology)
