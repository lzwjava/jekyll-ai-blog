---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transport Layer Data Transmission Modes
translated: false
type: note
---

Question: What is the data transmission service mode of the transport layer between two transport entities?

Answer:

The correct answer is **B**.

**Explanation:**
The primary task of the transport layer is to provide reliable or unreliable data transfer services between two end systems (transport entities).
- **Full-Duplex Service**: In most standard networking scenarios (such as TCP connections), the transport layer operates in **full-duplex** mode. This means both entities can send and receive user data and control data simultaneously. This is the default and most common configuration.
- **Half-Duplex Service**: While less common in modern general-purpose protocols like TCP, there are specific contexts or specialized protocols where communication might be restricted to **half-duplex** (data flows in only one direction at a time). Therefore, stating that it is "generally full-duplex, but can be half-duplex in individual cases" accurately reflects the flexibility and typical operation of the layer.

Options A and C are incorrect because they use absolute terms ("only") which do not account for the variety of protocol implementations and specific use cases. Option D is incorrect because Option B provides a valid description.

References:
