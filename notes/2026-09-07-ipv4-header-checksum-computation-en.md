---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv4 Header Checksum Computation
translated: false
type: note
---

Question: How exactly do you split an IPv4 header into 16-bit words, sum them with one's complement addition, and compute the final checksum?

Answer:

---

## Step-by-Step Example

Let's use a **minimal 20-byte IPv4 header** (no options):

```
45 00 00 3c
1a 2b 40 00
40 06 00 00   ← checksum field = 0000 (zeroed out)
c0 a8 01 01   ← Source IP: 192.168.1.1
c0 a8 01 02   ← Dest IP:   192.168.1.2
```

---

## Step 1 — Split into 16-bit (2-byte) Words

Read the header **2 bytes at a time**, left to right:

```
Word 1:  45 00  →  0x4500
Word 2:  00 3c  →  0x003c
Word 3:  1a 2b  →  0x1a2b
Word 4:  40 00  →  0x4000
Word 5:  40 06  →  0x4006
Word 6:  00 00  →  0x0000  ← checksum (zeroed)
Word 7:  c0 a8  →  0xc0a8
Word 8:  01 01  →  0x0101
Word 9:  c0 a8  →  0xc0a8
Word 10: 01 02  →  0x0102
```

---

## Step 2 — One's Complement Addition

Normal addition, but if the result **overflows 16 bits**, wrap the carry back and add it to the low bits ("end-around carry").

```
  0x4500
+ 0x003c  = 0x453c
+ 0x1a2b  = 0x5f67
+ 0x4000  = 0x9f67
+ 0x4006  = 0xdf6d
+ 0x0000  = 0xdf6d
+ 0xc0a8  = 0xa015  ← overflow! 0x1a015 → carry=1 → 0xa015+1 = 0xa016
+ 0x0101  = 0xa117
+ 0xc0a8  = 0x61bf  ← overflow! 0x161bf → carry=1 → 0x61bf+1 = 0x61c0
+ 0x0102  = 0x62c2
```

Final sum = **`0x62c2`**

---

## Step 3 — One's Complement of the Result

Flip every bit (bitwise NOT):

```
0x62c2  =  0110 0010 1100 0010
NOT        1001 1101 0011 1101
        =  0x9d3d
```

**Checksum = `0x9d3d`** → insert into header bytes 10–11.

---

## Verification at the Receiver

Sum **all 10 words** including the real checksum `0x9d3d`:

```
0x62c2 + 0x9d3d = 0xffff
```

One's complement of `0xffff` = `0x0000` → **valid!**
*(Some implementations check: if sum == `0xffff` → valid)*

---

## The Carry Wrap Rule (Key Concept)

```
Normal addition:   0xffff + 0x0001 = 0x10000  ← 17-bit overflow
One's complement:  keep low 16 bits → 0x0000
                   add carry (1)    → 0x0001   ✓ wrap around
```

This is why it's called **end-around carry** — the overflow bit loops back.

---

References:

- [RFC 791 – IPv4 Checksum](https://datatracker.ietf.org/doc/html/rfc791#section-3.1)
- [One's Complement Checksum – Wikipedia](https://en.wikipedia.org/wiki/Internet_checksum)
- [IPv4 Checksum Calculation – GeeksforGeeks](https://www.geeksforgeeks.org/calculation-of-tcp-checksum/)
