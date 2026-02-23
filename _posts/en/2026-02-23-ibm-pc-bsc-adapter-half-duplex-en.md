---
audio: false
generated: true
image: false
lang: en
layout: post
title: IBM PC BSC Adapter Half Duplex Lines
translated: false
type: note
---

Question: What type of transmission line is the IBM PC BSC communication adapter primarily designed for?

Answer: 

The **IBM PC BSC (Binary Synchronous Communication) communication adapter** is primarily designed for **half-duplex transmission lines**.

### Explanation:
- **BSC (Binary Synchronous Communication)** is a character-oriented, synchronous data link layer protocol developed by IBM.
- It was commonly used in early mainframe and PC communications.
- In **half-duplex** communication, data can be transmitted in both directions, but **not simultaneously**. This fits the operational model of BSC, where the sender and receiver take turns transmitting.
- Full-duplex allows simultaneous two-way communication, which is not typically supported by basic BSC implementations without additional hardware or protocol enhancements.
- Therefore, the IBM PC BSC adapter is optimized for **half-duplex** environments.

**Correct Answer:**  
**A. 半双工传输线路设计的 (Designed for half-duplex transmission lines)**

References: