---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATM Cell Fixed Length Explained
translated: false
type: note
---

Question: What is the fixed length of an ATM cell?

Answer: 

The correct answer is **C. 53 bytes**.

**Detailed explanation**:  
In ATM (Asynchronous Transfer Mode) networks, the basic unit of data transmission is called a **cell** (信元). This cell has a **fixed length** of **exactly 53 bytes**, which consists of:

- **Header**: 5 bytes  
- **Payload** (information field / 用户信息域): 48 bytes  

Total: 5 + 48 = **53 bytes**

This fixed and relatively small cell size was deliberately chosen in the design of ATM to:
- Minimize queuing delay (especially important for real-time voice and video traffic)
- Allow efficient statistical multiplexing
- Simplify hardware switching implementation

Common incorrect options and why they are wrong:
- **A. 8 bytes**: Far too small — not used in ATM
- **B. 16 bytes**: Sometimes confused with header size in other protocols, but incorrect for ATM cells
- **D. 64 bytes**: Close to the 53-byte size, but not accurate (some people remember it incorrectly as “about 64 bytes”)

So the only correct answer is **C. 53 bytes**.

References:  

- None (standard ATM protocol definition, widely documented in networking textbooks and ITU-T I.150 / I.361 recommendations)