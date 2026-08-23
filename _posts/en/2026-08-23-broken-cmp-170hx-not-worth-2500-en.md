---
audio: false
generated: true
image: false
lang: en
layout: post
title: Broken CMP 170HX Not Worth 2500
translated: false
type: note
---

Question: **Is a broken CMP 170HX 8GB (VBIOS damaged, driver cannot install) worth buying for 2500 CNY?**

Answer:

Short answer: **No, I would not buy it at 2500 CNY unless you can test recovery yourself.**
At 2500 CNY (~$350 USD), it is only attractive if the seller allows return or you have SPI programmer + experience.

The CMP 170HX market is strange because the card is basically a cut-down GA100/A100-class accelerator. It has 4480 CUDA cores and HBM2e; community work unlocked some hidden capability through software, making working cards valuable. ([GitHub][1])

But this specific card:

> "能认卡，驱动打不上，刷了vbios"

is a **high-risk state**.

## Price analysis

Working CMP 170HX 8GB examples have sold anywhere from roughly:

* ~$200-500 historically for mining cards ([eBay][2])
* higher after unlock hype; some listings/sales are much higher ([eBay][3])

2500 CNY (~$350) for a **working** card could be reasonable.

But a "bad VBIOS" card should have a big discount.

My pricing:

| Condition                            | Reasonable price |
| ------------------------------------ | ---------------: |
| Fully working + driver + CUDA test   |    2500-4000 CNY |
| Driver fails but nvflash can recover |    1200-1800 CNY |
| Unknown VBIOS, no testing            |     500-1000 CNY |
| Dead/no PCIe                         |       parts only |

For this one, I would offer around **1000-1500 CNY max**.

---

## Why risky?

A VBIOS mistake can mean:

### Best case

GPU is fine:

```
PCIe detected
      |
      v
wrong ROM
      |
      v
flash correct ROM
      |
      v
works
```

Cost: almost zero.

### Worst case

```
wrong ROM
      |
      v
corrupted SPI flash
      |
      v
nvflash cannot access
      |
      v
remove cooler
      |
      v
CH341A programmer
      |
      v
manual SPI recovery
```

Time cost: several hours.

---

## Before buying, ask seller for:

1. GPU detection:

```bash
lspci -nn | grep NVIDIA
```

Need:

```
10de:20c2
```

for 8GB CMP 170HX. ([GitHub][1])

2. `nvidia-smi` output:

Bad:

```
No devices were found
```

or:

```
GPU has fallen off the bus
```

3. nvflash test:

```bash
nvflash --list
```

If nvflash sees the card → much better.

4. Exact VBIOS version:

```bash
nvflash --version
```

---

Given your background (you run Linux/CUDA and have flashed GPUs before), **this is a repair gamble, not a GPU purchase**.

My personal threshold:

* **≤1000 CNY:** buy as a project
* **1500 CNY:** maybe
* **2500 CNY:** buy only if seller proves nvflash recovery possible
* **3000+ CNY:** buy working card instead

At 2500 CNY, you are paying almost working-card money while accepting repair risk. I would pass or negotiate hard.

[1]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/hardware/overview.md?utm_source=chatgpt.com "cmp170hx/docs/hardware/overview.md at main · Consensus-Protocol/cmp170hx · GitHub"
[2]: https://www.ebay.com/itm/278187573402?utm_source=chatgpt.com "NVIDIA CMP 170HX 8GB MINING GPU TESTED WORKING 100% | eBay"
[3]: https://www.ebay.com/itm/307075365403?utm_source=chatgpt.com "NVIDIA CMP 170HX 8GB Mining Card GPU 164mh/S Exclusive PCI-Express 4.0 X4 | eBay"
