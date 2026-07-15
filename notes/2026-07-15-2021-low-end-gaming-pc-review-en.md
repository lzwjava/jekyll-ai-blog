---
audio: false
generated: true
image: false
lang: en
layout: post
title: 2021 Low-End Gaming PC Review
translated: false
type: note
---

Question: How good is this PC configuration with i5-10400F + RX 6500 XT 4GB + 16GB RAM?

Answer:

This is a **low-end gaming / general desktop machine from around 2021**, still usable in 2026 for basic work, but not a good AI/ML machine.

Specs:

| Component   | Comment                                     |
| ----------- | ------------------------------------------- |
| CPU         | Intel Core i5-10400F (6 cores / 12 threads) |
| GPU         | AMD Radeon RX 6500 XT 4GB                   |
| RAM         | 16GB DDR4-3200                              |
| SSD         | 256GB                                       |
| Motherboard | ASUS B460M                                  |
| PSU         | "百硕 600W" (unknown quality)                 |

## CPU: i5-10400F

Intel Core i5-10400F

Still decent for daily use.

* 6C/12T
* Base 2.9GHz
* Boost 4.3GHz
* PCIe 3.0 only

Performance roughly:

* Better than old i7-7700
* Similar to Ryzen 5 3600
* Much slower than modern Ryzen 5 5600 / i5-12400F

For:

* coding ✅
* Docker/Kubernetes small workloads ✅
* web browsing ✅
* office ✅
* light compilation ✅

Fine.

---

## GPU: RX 6500 XT 4GB is the weak point

AMD Radeon RX 6500 XT

This card is unusual.

Specs:

* 4GB GDDR6
* 64-bit memory bus
* PCIe 4.0 x4 interface

The problem:

### 1. Only 4GB VRAM

For AI:

* Llama/Qwen inference ❌
* Stable Diffusion barely possible
* CUDA ecosystem unavailable

Your RTX 4070 is many generations ahead.

Comparison:

| GPU           | VRAM      | AI usefulness               |
| ------------- | --------- | --------------------------- |
| RX 6500 XT    | 4GB       | almost none                 |
| RTX 3060 12GB | 12GB      | useful                      |
| RTX 4070      | 12GB      | very useful                 |
| MI50          | 16GB HBM2 | interesting for experiments |

---

### 2. Gaming performance

Approximately:

RX 6500 XT:

* 1080p esports: OK
* AAA games: low settings

Examples:

* CS2 / Valorant: fine
* League: fine
* Cyberpunk: poor
* New AAA 2026 games: not suitable

---

## Motherboard: ASUS B460M

ASUS B460M motherboard

OK but limited.

* DDR4 only
* PCIe 3.0
* no CPU overclock
* LGA1200 socket

Upgrade path:

* i7-10700
* i9-10900

but not worth investing now.

---

## SSD: 256GB

Too small.

After:

* Windows
* IDE
* Docker images
* models

you will run out quickly.

Minimum today:

* 1TB NVMe SSD

---

## PSU: 百硕 600W

This is the biggest risk.

A cheap 600W PSU does not mean it can really provide clean power.

For this machine:

Power consumption:

```
CPU       ~65W
GPU       ~100W
system    ~50W

total     ~200W
```

A good 400W PSU is enough.

The issue is quality, not wattage.

---

# Overall score

### Normal PC

```
CPU        7/10
GPU        4/10
RAM        6/10
SSD        3/10
Upgrade    3/10

Overall    5/10
```

Good as:

✅ office PC
✅ kids computer
✅ programming learning machine
✅ light gaming

Not good as:

❌ AI training
❌ LLM inference
❌ CUDA development
❌ GPU computing

---

## Compared with your current hardware

Your machines:

### i9-13900KF + RTX 4070

This is another universe:

```
CPU:
i9-13900KF >> i5-10400F

GPU:
RTX 4070 >> RX6500XT

AI:
RTX 4070 works
RX6500XT basically doesn't
```

Your RTX 4070 machine is ~5-8x more capable depending on workload.

---

## If buying second hand

I would value this machine around:

* CPU + motherboard: ¥500-700
* RX6500XT: ¥500-700
* RAM: ¥150
* SSD: ¥50
* case/PSU: almost nothing unless PSU is good

Reasonable total:

**¥1200-1500 RMB**

Above ¥1800, I would skip.

For an AI tinkering box, I would rather buy:

* Ryzen 5 5600 + B550 + 32GB RAM
* RTX 3060 12GB

or your MI50 route:

* cheap AMD workstation platform
* 16GB HBM2 VRAM

The RX6500XT is basically the wrong GPU class for your current direction.
