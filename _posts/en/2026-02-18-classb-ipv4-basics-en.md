---
audio: false
generated: true
image: false
lang: en
layout: post
title: Class B IPv4 Address Basics
translated: false
type: note
---

In the context of **IPv4 addressing**, addresses are divided into different classes (A, B, C, D, E) based on the value of the first few bits in the first octet (the first 8 bits of the IP address).

### B Class IP Addresses:
- **B class IP addresses** are designed for medium-sized networks.
- The **first octet** of a B class IP address always starts with the binary pattern **`10`**.
- This means the first two bits of the first octet are fixed as **`10`** in binary.

#### Breakdown:
- **First octet range (in decimal):** 128 to 191
- **Binary representation of the first octet:** Always starts with **`10`** followed by 6 more bits (e.g., `10xxxxxx`).

#### Example:
- **128.0.0.0** to **191.255.255.255** are B class addresses.
- The first two bits of **128** in binary are **`10`**.

### Why is this important?
- The first two bits **`10`** identify the address as a **B class** address, which determines the default subnet mask and the number of hosts and networks available.

**So, the correct answer is `10`.**