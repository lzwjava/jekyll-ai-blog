---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPv6 Address Structure Explained
translated: false
type: note
---

Question: Is an IPv6 address made up of 8 parts, each containing 4 hex digits (16 bits)?

Answer: Yes, you're correct on all counts!

An IPv6 address is **128 bits** total, structured like this:

- **8 groups** (parts/hextets)
- Each group is **16 bits** wide
- 16 bits = **4 hexadecimal digits** (since each hex digit = 4 bits)

So the math works out as:

```
128 bits ÷ 8 groups = 16 bits per group
16 bits ÷ 4 bits per hex digit = 4 hex digits per group
```

A full IPv6 address looks like:

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

Each group separated by `:` is 4 hex digits = 16 bits.

One small correction to your equation: you wrote `256/8 = 64` but the correct math for bits is `128 ÷ 8 = 16` (bits per group), not 64. Each group is **16 bits**, not 64. (64 would be if you split 512 bits into 8 parts.)

**Quick summary table:**

| Property | Value |
|---|---|
| Total bits | 128 |
| Number of groups | 8 |
| Bits per group | 16 |
| Hex digits per group | 4 |
| Separator | `:` (colon) |

References:
- [IPv6 Address Architecture – RFC 4291](https://datatracker.ietf.org/doc/html/rfc4291)
- [IPv6 – Wikipedia](https://en.wikipedia.org/wiki/IPv6#Address_representation)
