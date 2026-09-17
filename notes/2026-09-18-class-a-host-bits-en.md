---
audio: false
generated: true
image: false
lang: en
layout: post
title: Class A Host Bits
translated: false
type: note
---

Question: How many bits are used for the **host number** in a Class A IPv4 address?

Answer:

A **Class A IPv4 address** uses:

```text
| 0 | Network ID (7 bits) | Host ID (24 bits) |
  1        7 bits              24 bits
```

So:

* **1 bit**: fixed `0` → identifies Class A
* **7 bits**: Network number
* **24 bits**: **Host number**
* Total: **32 bits**

Therefore:

> **Class A host number = 24 bits**

The theoretical number of hosts per Class A network is:

$$
2^{24}-2 = 16,777,214
$$

The `-2` excludes the **all-zero host address** (network address) and **all-one host address** (broadcast address).

Classic ranges:

```text
Class A: 1.0.0.0 ~ 126.255.255.255
Default mask: 255.0.0.0 = /8
Host bits: 24
```

I can also give you a compact **Class A/B/C bit-layout table** that makes these exam questions almost instant to answer.
