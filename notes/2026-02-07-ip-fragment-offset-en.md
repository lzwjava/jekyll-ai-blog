---
audio: false
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: Fragment Offset Unit in IP Datagram
translated: false
type: note
---

The unit of the **Fragment Offset** field in the fixed part of an **IP datagram** structure is **8 bytes (B)**.

### Explanation:
- The **Fragment Offset** field indicates the position of the current fragment relative to the start of the original IP datagram.
- Since IP datagram fragments must be multiples of 8 bytes in length, the **Fragment Offset** is measured in units of 8 bytes.
- The value of the **Fragment Offset** is multiplied by 8 to get the actual offset in bytes.

### Analysis of Options:
- **A. 1B**: Incorrect, the unit is not 1 byte.
- **B. 8B**: Correct, the unit is 8 bytes.
- **C. 16B**: Incorrect, the unit is not 16 bytes.
- **D. 32B**: Incorrect, the unit is not 32 bytes.

Thus, the **correct answer is B**.