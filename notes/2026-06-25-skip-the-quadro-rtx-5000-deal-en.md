---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skip the Quadro RTX 5000 Deal
translated: false
type: note
---

**Question:** What is this Walmart product listing?

**Answer:**

This is a **used/refurbished NVIDIA Quadro RTX 5000** (the Turing-generation workstation GPU, not a consumer GeForce card — the listing title is misleading with "GeForce") sold for **$799** by a third-party seller (SYNNEX Ltd) on Walmart.

Key specs:

- **GPU**: Quadro RTX 5000 (Turing, TU104 die) — same die as consumer RTX 2080
- **VRAM**: 16 GB GDDR6 (vs 8 GB on consumer RTX 2080)
- **Interface**: PCIe x16 3.0
- **Outputs**: 4× DisplayPort 1.4 + 1× USB-C
- **TDP**: 265W (needs PCIe power)
- **Condition**: Grade A "Like New", 30-day return, no accessories
- **Dell OEM part**: `7XK5H` — pulled from a Dell workstation

**Is it worth it for you?**

Honestly, **no** — at least not for ML training. Here's the comparison:

| Card | VRAM | Tensor TFLOPS | Generation | Price |
|------|------|--------------|------------|-------|
| Quadro RTX 5000 (this) | 16 GB GDDR6 | ~57 (FP16) | Turing (2018) | $799 used |
| RTX 4070 Ti | 12 GB GDDR6X | ~285 (FP16) | Ada (2023) | ~$650 |
| RTX 3090 | 24 GB GDDR6X | ~142 (FP16) | Ampere (2020) | ~$500 used |

The Quadro RTX 5000 is a **2018-era professional card** — the workstation branding gives it 16 GB VRAM (good), but the raw compute is ancient compared to modern consumer cards. Tensor core performance is ~4-5x worse than current Ada gen cards.

**The only real reason to buy this** would be if you specifically need 16 GB on a tight budget and can't get a used RTX 3090 (24 GB, ~$500). For your use case — model training, nanoGPT, fine-tuning — a **used RTX 3090** at ~$500 would be far superior: more VRAM, significantly faster Tensor cores, better cuDNN support maturity.

Pass on this one.
