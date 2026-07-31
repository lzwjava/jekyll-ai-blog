---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maximum Hop Limit Value 255
translated: false
type: note
---

Question: In IPv6, what is the maximum value of the "Hop Limit" field?

Answer: **C. 255**

### Explanation

* **Field Size:** The **Hop Limit** field in the IPv6 header is **8 bits** (1 byte) long.
* **Maximum Value:** An 8-bit field can represent $2^8 = 256$ total values, ranging from **0 to 255**. Therefore, the maximum numerical value that can be stored in this field is **255**.
* **Purpose:** Each router that forwards the IPv6 packet decrements the Hop Limit value by 1. If the value reaches 0, the packet is discarded, preventing it from looping indefinitely in the network.

---

> **Note on the question text:** The textbook explanation provided in your snippet mentions "长度为8B" (length is 8 Bytes). This is a typo commonly found in some exam prep materials. It should state **8 bits** (1 Byte), not 8 Bytes.
