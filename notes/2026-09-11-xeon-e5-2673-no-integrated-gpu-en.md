---
audio: false
generated: true
image: false
lang: en
layout: post
title: Xeon E5-2673 No Integrated GPU
translated: false
type: note
---

**Question:** Does the Xeon E5-2673 have an integrated GPU?

**Answer:** No. **Xeon E5-2673 does not have an integrated GPU.**

For the E5-2673 family:

```text
Xeon E5-2673
├── CPU cores: yes
├── Memory controller: yes
├── PCIe controller: yes
└── iGPU: ❌ no
```

So on an **X99 motherboard + E5-2673**, the motherboard's HDMI/DVI/VGA outputs generally **won't produce video**. You need a discrete GPU.

This is actually important for your **GPU repair/test bench**: an X99 + Xeon setup needs a working GPU just to get display output, whereas an **H81/B85 + i5** platform with Intel graphics can boot and display without a discrete GPU.

I can also compare **X99 + E5-2673 vs H81 + i5-4xxx** specifically as a GPU-repair test platform.