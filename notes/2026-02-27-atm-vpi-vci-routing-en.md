---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATM VPI/VCI for Routing Clarified
translated: false
type: note
---

Question: In the ATM cell header format, the VPI/VCI fields are used for

A. Error control
B. Flow control
C. Routing
D. Cell selection

Your answer: D
Correct answer: C

Answer:

The correct answer is **C. Routing** (路由选择).

### Detailed Explanation

In the ATM (Asynchronous Transfer Mode) cell header (5-byte header), the main fields and their primary functions are:

- **GFC** (Generic Flow Control) → Used for **flow control** (mainly at the UNI interface, 4 bits, local significance only)
- **VPI** (Virtual Path Identifier) + **VCI** (Virtual Channel Identifier) → Used for **routing** / path selection
  These two fields together identify the virtual connection (VPC or VCC) and are the most important fields for forwarding the cell through the ATM network (just like IP destination address in IP networks).
- **PT** (Payload Type) → Indicates the type of payload (user data / management data)
- **CLP** (Cell Loss Priority) → Used for **congestion control** / cell discard priority
- **HEC** (Header Error Control) → Used for **error detection** and single-bit error correction in the header

So the correct mapping is:

- Error control → **HEC**
- Flow control → **GFC**
- Routing / path selection → **VPI/VCI**
- Congestion / cell discard priority → **CLP**

Therefore, VPI/VCI fields are clearly used for **routing selection** (路由选择), not "cell selection" (信元选择).

"Cell selection" is not a standard function assigned to any field in the ATM header.

**Your mistake**: You chose D (信元选择), but the correct choice is C (路由选择).

References:

- ITU-T Recommendation I.361 - B-ISDN ATM Layer Specification
- ATM Forum specifications (historical reference)
