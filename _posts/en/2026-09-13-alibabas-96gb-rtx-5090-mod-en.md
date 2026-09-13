---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alibaba’s 96GB RTX 5090 Mod
translated: false
type: note
---

**Question:** What does "魔改" mean, and how did a Chinese manufacturer on Alibaba modify an RTX 5090 to have 96GB of VRAM?

**Answer:**

**What is 魔改 (mó gǎi)?**

魔改 is a Chinese slang term combining 魔 (*mó*, "demonic / magical") + 改 (*gǎi*, "modify / change"). It literally means **"extreme/radical modification"** — a mod so intense and unconventional it seems almost supernatural or "mad-scientist" level. It's commonly used in Chinese tech communities to describe hardware that has been pushed far beyond its original specs through DIY or factory engineering. Think of it as the Chinese equivalent of "frankenstein-modding" or "extreme overclocking/modding culture."

---

**The 96GB RTX 5090 "魔改" on Alibaba**

Shenzhen Suqiao Intelligent Technology took the original 32GB RTX 5090 and upgraded it to 96GB of VRAM, selling the modified cards on Alibaba for around $3,888. Here's how it's technically done:

**1. Custom PCB (Printed Circuit Board)**

The RTX 5090 96GB likely uses a custom PCB, allowing the manufacturer to install memory chips in "clamshell mode," which doubles the total memory on the PCB by placing memory pads on both sides of the board.

**2. Replacing/Upgrading Memory Chips**

The modders replaced the original GDDR7 chips with higher-capacity modules and reconfigured the PCB using advanced BGA (Ball Grid Array) soldering techniques.

**3. Reballing the GPU Die**

The vendor could either procure the GB202 silicon individually or extract it from retail RTX 5090 cards and reball it onto the custom PCB — a method Chinese workshops already used to push the RTX 4090 to 48GB VRAM.

**4. Why it's technically plausible**

The RTX Pro 6000 Blackwell, which has 96GB of GDDR7, uses the same GB202 silicon as the RTX 5090 but with more enabled Streaming Multiprocessors (SMs). This proves a 96GB configuration is possible on the GB202 architecture.

**5. Context & caveats**

This innovation comes amid increasing U.S. restrictions on Nvidia's AI-class chips entering China, pushing many Chinese firms to explore alternative options — leading to a burgeoning mod economy around gaming GPUs. However, the Alibaba listing quotes GDDR6X memory instead of GDDR7, which is a notable warning sign, and firmware/memory-initialization issues would also need to be addressed. This isn't the first time — Chinese factories have previously produced modified cards like the RTX 3090 48GB and RTX 4090 48GB.

---

**References:**

- [Tom's Hardware – China-modified RTX 5090 96GB on Alibaba](https://www.tomshardware.com/pc-components/gpus/china-modified-nvidia-rtx-5090-with-massive-96gb-of-memory-appears-on-alibaba-for-less-than-usd4-000-3x-more-vram-at-65-percent-the-cost-of-the-original)
- [eTeknix – RTX 5090 with 96GB VRAM](https://www.eteknix.com/rtx-5090-with-96-gb-of-vram-appears-on-alibaba-for-almost-4000/)
- [igor'sLAB – RTX 5090 96GB mod: technically plausible but unconfirmed](https://www.igorslab.de/en/rtx-5090-with-96-gb-vram-appears-on-alibaba-modification-technically-plausible-but-unconfirmed/)
- [ThePCEnthusiast – RTX 5090 With 96GB VRAM on Alibaba](https://thepcenthusiast.com/rtx-5090-96gb-vram-mod-alibaba/)
