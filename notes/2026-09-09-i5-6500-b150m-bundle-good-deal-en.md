---
audio: false
generated: true
image: false
lang: en
layout: post
title: i5-6500 B150M Bundle Good Deal
translated: false
type: note
---

Question: Is the **i5-6500 + MSI B150M motherboard bundle for ¥200** a good deal?

Answer: **Yes — ¥200 is a pretty good price**, especially if you're building a cheap GPU test bench.

| Part         | Details            |         Value |
| ------------ | ------------------ | ------------: |
| CPU          | Intel Core i5-6500 |      ~¥70–100 |
| Motherboard  | MSI B150M          |     ~¥100–150 |
| Total        | CPU + board        | **~¥170–250** |
| Asking price |                    |      **¥200** |

### Why I like this combo

**i5-6500**

* 4 cores / 4 threads
* 3.2 GHz base, up to 3.6 GHz Turbo
* 65 W TDP
* LGA1151
* DDR4 support
* Has Intel iGPU → useful for diagnosing GPUs

**B150M**

* LGA1151 → exactly matches the i5-6500
* Usually DDR4
* PCIe x16 slot for your GPU testing
* Cheap and relatively simple platform
* No overclocking, but that's irrelevant for a test bench

For your **GPU repair/testing setup**, this is actually more attractive than spending money on a modern platform. You mainly need:

```text
PSU
 │
 ├── B150M
 │    └── i5-6500
 │
 ├── DDR4
 │
 └── PCIe x16
       │
       └── GPU under test
```

The i5-6500's integrated graphics is particularly useful: **remove the discrete GPU and you can still get video output**, which makes troubleshooting much easier.

### One thing I'd check before paying

The listing says:

> 功能正常，无拆无修

That's good, but I'd ask the seller to demonstrate:

```text
1. BIOS successfully boots
2. CPU-Z shows i5-6500
3. All RAM slots work
4. PCIe x16 slot works
5. SATA works
6. USB works
7. No bent LGA1151 pins
```

**Most important: inspect the CPU socket pins.** A damaged LGA1151 socket can turn a ¥200 bargain into a headache.

If you can send me the **actual Xianyu listing photos**, I can inspect the B150M model, socket, PCIe slot, VRM area, and visible damage.

I can also compare this ¥200 B150M+i5-6500 against the **B85/X99 machines you've been considering specifically as a GPU repair test bench**.
