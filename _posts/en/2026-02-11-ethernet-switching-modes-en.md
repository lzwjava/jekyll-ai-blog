---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ethernet Switching Modes Explained
translated: false
type: note
---

Question: What are the main switching modes of Ethernet switches, primarily including direct switching and which of the following?

A. Indirect switching  
B. Detection control switching  
C. Fragment switching  
D. Store-and-forward switching  

Answer:  

**The correct answer is D. Store-and-forward switching**

**Explanation:**

Ethernet switches mainly use the following data switching (forwarding) methods:

1. **Cut-through switching** (直接交换 / 直通交换)  
   - The switch starts forwarding the frame as soon as it reads the destination MAC address (usually after receiving the first 6–14 bytes).  
   - Fastest forwarding speed, lowest latency.  
   - Disadvantage: May forward error frames (no full CRC check).

2. **Store-and-forward switching** (存储转发交换)  
   - The switch receives the **entire frame**, performs a full CRC check, discards bad frames, then forwards valid frames.  
   - Highest reliability, can filter error frames.  
   - Disadvantage: Higher latency (must wait for the whole frame).

3. **Fragment-free switching** (改进直接交换 / 无碎片交换)  
   - A compromise method: The switch waits to receive the first **64 bytes** (to avoid collision fragments), then starts forwarding.  
   - Balances speed and error filtering (filters most collision fragments but not all errors).

**Correct classification in the question:**

The two **main** and most commonly mentioned switching modes of Ethernet switches are:

- **Direct switching** (cut-through)  
- **Store-and-forward switching**

Therefore, the answer should be **D. Store-and-forward switching**.

**Why your answer C is incorrect:**

- “分段交换” (fragment switching) is **not** one of the standard mainstream switching modes of Ethernet switches.  
- The term “分段交换” is sometimes misused or appears in poorly translated questions, but it does **not** correspond to any standard Ethernet switch forwarding method. The closest related concept is “fragment-free”, but even that is usually called “改进直接交换” or “无碎片交换”, **not** “分段交换”.

**Summary of standard Ethernet switch switching modes (most textbooks & certification exams):**

- 直接交换（Cut-through）  
- 存储转发交换（Store-and-forward）  
- 改进直接交换 / 无碎片交换（Fragment-free）

The question asks for the mode that pairs with “直接交换”, which is **存储转发交换** → **D**.

References:  

- None (standard Ethernet switching knowledge from IEEE 802.3, Cisco CCNA material, and common Chinese network engineering textbooks)