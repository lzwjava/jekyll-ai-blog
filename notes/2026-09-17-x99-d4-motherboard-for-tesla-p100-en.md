---
audio: false
generated: true
image: false
lang: en
layout: post
title: X99-D4 Motherboard for Tesla P100
translated: false
type: note
---

Question: What does this **Kenao X99-D4 motherboard bulk listing** mean, and can it take an **NVIDIA Tesla P100**?

Answer:

The listing says:

> **“Kenao X99-D4 motherboard, 200 units, DDR4 ATX-sized board, I/O shield included, tested OK. If you understand it and need it, buy directly. Bulk purchases welcome.”**

So it's basically a **used/refurbished bulk lot of 200 X99-D4 motherboards**, with DDR4 support, rear I/O shield, and supposedly tested working.

### P100 compatibility

**Yes, technically an NVIDIA Tesla P100 can be used with this platform.**

There is particularly good evidence for the X99-D4 family: a documented build uses **Kenao X99-D4 + Xeon E5-2683 v4 + DDR4 + an NVIDIA P104-100**, including PCIe GPU passthrough under Proxmox. ([Tencent Cloud][1])

For a **Tesla P100 PCIe**, the important pieces are:

```text
Kenao X99-D4
    │
    ├── Xeon E5 v3/v4
    │       └── PCIe 3.0 lanes
    │
    ├── DDR4 ECC/RECC
    │
    └── PCIe x16 slot
             │
             └── NVIDIA Tesla P100 PCIe
```

The X99 platform is actually a reasonable cheap host for old Tesla cards because the Xeon E5 v3/v4 CPUs provide lots of PCIe lanes.

### But check these 4 things before buying 200 boards

**1. Exact P100 version**

This matters a lot:

* **P100 PCIe 16GB** → easiest
* **P100 PCIe 12GB** → also fine
* **P100 SXM2** → **NOT directly usable** in a normal X99 PCIe slot

You want the **PCIe version**, not SXM2.

**2. PSU**

The P100 PCIe can consume roughly **250 W**, so don't pair it with some tiny desktop PSU.

For one P100:

```text
E5-26xx v4       ~120 W
P100             ~250 W
motherboard/RAM  ~50-80 W
--------------------------------
realistic PSU    500-650 W+
```

I'd use a decent **650 W+ PSU per GPU** rather than trying to run it on a cheap 400 W unit.

**3. PCIe power connector**

Check the exact P100 board you're buying and its power connector/cable requirements. Don't assume the motherboard supplies GPU power; the GPU normally gets auxiliary power from the PSU.

**4. Multiple P100s**

This is where X99-D4 becomes less attractive.

For **1 P100**, very reasonable.

For **2 P100s**, potentially reasonable depending on the exact X99-D4 PCIe slot layout and CPU.

For **4+ P100s**, I'd look for a proper workstation/server board with explicit multi-GPU slot layout and sufficient PCIe lanes/spacing.

The X99 ecosystem does have examples of multi-GPU workstation configurations, but PCIe lane topology becomes important. ([Pion1eer][2])

### My take for an AI box

If your plan is something like:

```text
X99-D4
E5-2683 v4 / E5-2690 v4
64–128 GB DDR4 ECC
1× P100 16GB
Ubuntu
CUDA
```

**Yes, this is a viable dirt-cheap P100 inference/training machine.**

And the fact that this particular listing has **200 boards** means the seller is probably targeting exactly this kind of homelab / refurb / bulk-build market.

One thing I'd verify with the seller before buying the lot is **a photo of the actual PCIe slots + the exact board revision**, because "X99-D4" is not enough to guarantee the same slot configuration across every Kenao revision.

I can also help you work out a **200-board + P100 cluster BOM**, including CPU/RAM/PSU/networking and estimated power per GPU.

[1]: https://cloud.tencent.com.cn/developer/article/2414840?utm_source=chatgpt.com "玩转 AIGC：打造本地大模型地基，PVE 配置显卡直通-腾讯云开发者社区-腾讯云"
[2]: https://www.ruanx.net/rd452x/?utm_source=chatgpt.com "洋垃圾 RD452X 装机记录"
