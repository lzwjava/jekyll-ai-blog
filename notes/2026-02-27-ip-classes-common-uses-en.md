---
audio: false
generated: true
image: false
lang: en
layout: post
title: IP Classes Commonly Used Explained
translated: false
type: note
---

Question: In IP address classification, the leftmost one or more binary bits are usually used to specify the network type. The commonly used IP address classes are:

A. 3 classes  
B. 4 classes  
C. 5 classes  
D. 6 classes  

The correct answer is A, but you chose B. Please explain the error.

Answer: 

The correct answer is **A. 3 classes**.

**Detailed explanation:**

Traditional classful IPv4 addressing divides IP addresses into **five classes** (A, B, C, D, E) based on the first few bits of the address:

- **Class A**: 0xxxxxxx (first bit = 0) → 1.0.0.0 – 126.255.255.255  
- **Class B**: 10xxxxxx (first two bits = 10) → 128.0.0.0 – 191.255.255.255  
- **Class C**: 110xxxxx (first three bits = 110) → 192.0.0.0 – 223.255.255.255  
- **Class D**: 1110xxxx (first four bits = 1110) → multicast addresses  
- **Class E**: 1111xxxx (first four bits = 1111) → reserved (experimental)

However, in actual network usage and most textbooks/exams (especially in China), when people talk about **"commonly used IP address classes"**, they usually refer only to **Class A, Class B, and Class C** — because:

- Class D is used only for multicast  
- Class E is reserved and not used in normal networks  

Therefore, the **commonly used** IP address classes are **three classes** (A, B, C).

That's why the correct answer is **A. 3 classes**.

Your choice **B. 4 classes** is incorrect because although there are technically five classes in total, the question specifically asks about **"commonly used"** classes, and the standard answer in most educational contexts (especially in certification exams like HCIA, CCNA introductory materials in Chinese) is **three classes**.

References:  

- None (this is standard IPv4 classful addressing knowledge)