---
audio: false
generated: true
image: false
lang: en
layout: post
title: Top ReBarUEFI Motherboard Choices
translated: false
type: note
---

Question: Which motherboard from the **ReBarUEFI tested motherboard list** should I pick?

Answer:

Yes, the page you mean is the **"List of tested motherboards"** in the ReBarUEFI Wiki / Issue #11. It contains actual user-tested boards, GPUs, BAR sizes, and whether UEFIPatch was required. ([GitHub][1])

For your goal (cheap Xianyu board + RTX 3090/M40/P100 experiments + 4G Decoding + CSM control), I would filter that list like this:

## Best choices from the list

### 1. ASUS Z170-P ⭐⭐⭐⭐⭐

From the list:

```
ASUS Z170-P
GPU: RTX 3090
BAR: 32GB
UEFIPatch: Y
```

([GitHub][2])

Why:

* Cheap on second-hand market
* DDR4
* M.2
* ASUS BIOS is easy to navigate
* Good chance of finding "Above 4G Decoding"
* Good for your i7-6700 / Xeon E3-1280 v5 idea

This is probably the one I would buy first.

---

### 2. ASUS Z170-A ⭐⭐⭐⭐⭐

From the list:

```
ASUS Z170-A
GPU: RX 5700 XT / RTX 3080 / Arc A750
BAR: 8GB-16GB
UEFIPatch: Y
```

([GitHub][2])

Similar to Z170-P, but slightly higher-end.

Advantages:

* Better VRM
* More expansion
* More enthusiast users → easier BIOS information

---

### 3. ASUS X99-DELUXE II ⭐⭐⭐⭐⭐ (AI lab choice)

From the list:

```
ASUS X99 DELUXE II
GPU: RTX 3090
BAR: 24GB
UEFIPatch: Y
```

([GitHub][2])

For your AI GPU experiments this is actually very interesting:

```
Xeon E5 v4
+
ECC DDR4
+
RTX 3090
+
Tesla cards
```

Advantages:

* Many PCIe lanes
* Quad channel RAM
* Better multi-GPU platform

---

### 4. Huananzhi X99-QD4 ⭐⭐⭐⭐ (cheap China option)

From the list:

```
Huananzhi X99-QD4
RTX 3060
BAR:16GB
UEFIPatch:N
```

([GitHub][1])

Interesting because:

* No BIOS patch required
* Cheap
* Easy to find

But BIOS quality is not ASUS level.

---

## Boards I would avoid even if they appear

For your purpose:

* Z97 boards requiring DSDT patch
* old X79 unless very cheap
* random H61/B75 boards

They work, but you spend time fighting PCI resource issues.

---

My ranking for you:

```
AI GPU lab:
1. ASUS X99-DELUXE II
2. ASUS Z170-P
3. ASUS Z170-A

Cheap experiment:
1. ASUS Z170-P
2. Huananzhi X99-QD4
3. MSI Z170A Gaming M5
```

For your previous **PCI insufficient resources** problem with P100/M40, I would especially prefer **ASUS Z170-P / Z170-A** because the BIOS options are usually clearer:

```
Advanced
 └── PCI Subsystem Settings
      ├── Above 4G Decoding  [Enabled]
      └── Re-Size BAR Support [Enabled]

Boot
 └── CSM
      └── Launch CSM [Disabled]
```

The ReBarUEFI list confirms Z170-P, Z170-A, and X99 boards have real successful large BAR tests. ([GitHub][2])

[1]: https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com "Home · xCuri0/ReBarUEFI Wiki · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI/issues/11?utm_source=chatgpt.com "List of working motherboards · Issue #11 · xCuri0/ReBarUEFI · GitHub"
