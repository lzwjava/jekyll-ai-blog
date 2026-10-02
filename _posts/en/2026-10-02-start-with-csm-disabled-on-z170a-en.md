---
audio: false
generated: true
image: false
lang: en
layout: post
title: Start with CSM Disabled on Z170A
translated: false
type: note
---

Question: Should CSM be enabled or disabled for your **Z170A Gaming M5 + M40**?

Answer: **Start with CSM disabled.**

For your PCI resource troubleshooting, use:

```text
CSM / Legacy        = Disabled
Above 4G Decoding   = Enabled
PCI_E1              = M40
PCIe Link Speed     = Gen2
```

Why: **Above 4G Decoding + pure UEFI** gives the firmware the cleanest environment for allocating large PCIe MMIO regions.

If you still get:

```text
PCI OUT OF RESOURCES
Insufficient PCI Resources Detected
```

then do a second test with **CSM enabled**. If the result changes, we've learned that the M40's legacy/UEFI initialization is involved.

So the order I'd test is:

```text
1. CSM OFF + Above 4G ON + Gen2
2. CSM ON  + Above 4G ON + Gen2
3. CSM OFF + Above 4G ON + Gen1
```

**Don't change several variables at once** beyond these controlled combinations; otherwise it's hard to identify what fixed the resource error.
