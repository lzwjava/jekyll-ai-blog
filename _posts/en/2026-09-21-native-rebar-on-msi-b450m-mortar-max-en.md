---
audio: false
generated: true
image: false
lang: en
layout: post
title: Native ReBAR on MSI B450M Mortar Max
translated: false
type: note
---

Question: **Is the MSI B450M MORTAR MAX a good choice if I want native ReBAR and don't want ReBarUEFI?**

Answer: **Yes — this is a reasonable board to buy, but I would verify the BIOS version before paying.**

The **MSI B450M MORTAR MAX** is an AM4/B450 board, and MSI's BIOS ecosystem supports Re-Size BAR on this generation. MSI documents Re-Size BAR as a normal BIOS feature alongside Above 4G Decoding. ([MSI][1])

The important distinction is:

```text
B450M MORTAR MAX
        │
        ├── Above 4G Decoding       ← BIOS setting
        ├── Re-Size BAR Support     ← BIOS setting
        │
        └── ReBarUEFI               ← NOT needed
```

### What I'd check before buying the used board

Ask the seller for a photo of:

```text
BIOS → Advanced → PCIe Sub-system Settings
```

You want to see:

```text
Above 4G Decoding        [Enabled/Disabled]
Re-Size BAR Support      [Enabled/Disabled/Auto]
```

MSI's current BIOS documentation shows this exact Re-Size BAR configuration path. ([MSI][1])

Also ask for the **current BIOS version**. This matters because the MORTAR MAX is an older B450 board, and BIOS revisions determine CPU/ReBAR compatibility.

The board itself has a CPU-connected **PCIe 3.0 x16** slot, so with something like a Ryzen 3000/5000 + RX 6000/RTX 30-class GPU, the hardware topology is perfectly reasonable for ReBAR. ([MSI][2])

### One correction to my previous answer

I would **not** characterize this board as merely a "ReBarUEFI community workaround" board.

The better way to think about it is:

> **B450M MORTAR MAX + appropriate stock MSI BIOS = native BIOS ReBAR, no ReBarUEFI.**

The ReBarUEFI project may still contain reports for this board because the project tracks many historical configurations, but that doesn't mean you need ReBarUEFI on a properly updated stock BIOS.

### For this particular used listing

I'd message the seller:

> “请拍一下 BIOS 里 `Above 4G Decoding` 和 `Re-Size BAR Support` 的设置页面，再拍一下 BIOS 版本号。”

If they show those two options, **I'd consider the board suitable for your goal**.

One caveat: the seller's description says nothing about the BIOS version, so **don't buy solely from this listing text**. The board itself is fine; the missing piece is confirming the BIOS.

[MSI B450M MORTAR MAX official specification](https://www.msi.com/Motherboard/B450M-MORTAR-MAX/Specification?utm_source=chatgpt.com)

[MSI Re-Size BAR BIOS documentation](https://us.msi.com/Landing/msi-click-bios-intel-amd-motherboard?utm_source=chatgpt.com)

[1]: https://us.msi.com/Landing/msi-click-bios-intel-amd-motherboard?utm_source=chatgpt.com "MSI Click BIOS - One-click optimization for Intel / AMD motherboards, effortlessly and efficiently"
[2]: https://www.msi.com/Motherboard/B450M-MORTAR-MAX/Specification?utm_source=chatgpt.com "B450 MORTAR MAX | Motherboard | MSI Global"
