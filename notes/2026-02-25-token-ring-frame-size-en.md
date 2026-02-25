---
audio: false
generated: true
image: false
lang: en
layout: post
title: Token Ring Frame Size Answer
translated: false
type: note
---

Question: In IEEE 802.5 Token Ring, the MAC frame has two basic formats: the token frame and the data frame. The token frame is only how many bytes long?  
A. 2 bytes  
B. 3 bytes  
C. 4 bytes  
D. 5 bytes  

Answer:  

**The correct answer is B. 3 bytes.**

**Detailed explanation:**

In the IEEE 802.5 Token Ring standard, there are indeed two fundamental MAC frame formats:

1. **Token frame** (pure token)  
   - Consists of exactly **3 bytes**:  
     - Starting Delimiter (SD) → 1 byte  
     - Access Control (AC) → 1 byte  
     - Ending Delimiter (ED) → 1 byte  
   - Total length = **3 bytes**

2. **Data frame** (also called LLC frame or information frame when it carries data)  
   - Much longer and variable length  
   - Basic structure: SD (1) + AC (1) + FC (1) + Destination Address (6) + Source Address (6) + [Information field, variable] + FCS (4) + ED (1) + Frame Status (1)  
   - Minimum length is typically around 19–21 bytes (without data), but can be much longer.

The key difference emphasized in the standard and most textbooks is that the **token itself is only 3 bytes long**.

The Starting Delimiter (SD) and Ending Delimiter (ED) each use a special violation of normal Manchester coding (J and K symbols, which are represented as "high-high" and "low-low" level pairs) to clearly mark frame boundaries and ensure data transparency.

Therefore, the correct choice is **B. 3 bytes**.

Your previous answer (A. 2 bytes) is incorrect. No mainstream version of the IEEE 802.5 Token Ring standard defines a 2-byte token.

References:  

- IEEE 802.5-1998 standard (Token Ring access method and physical layer specifications)  
- Most classic computer networking textbooks (e.g., Tanenbaum, Kurose & Ross, Peterson & Davie) describe the Token Ring token as 3 bytes