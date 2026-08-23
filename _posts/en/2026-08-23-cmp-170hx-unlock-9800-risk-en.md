---
audio: false
generated: true
image: false
lang: en
layout: post
title: "CMP 170HX Unlock: ¥9,800 Risk?"
translated: false
type: note
---

**Question:** Is buying an NVIDIA CMP 170HX (8GB variant, with 64GB unlock via cmpunlocker) for ¥9,800 CNY on Xianyu a good deal?

---

**Answer:**

This is a hot topic right now. Here's the full picture:

**What the cmpunlocker does**

The tool restores full SM compute throughput and unlocked HBM2e memory geometry that are restricted in firmware/OTP configuration. Specifically for the 8GB card, the 8GB 170HX can be unlocked to 64GB.

**The price surge context**

Cards that recently sold for roughly $100–$200 are now appearing for more than $1,000 globally after the tool went viral. ¥9,800 CNY ≈ ~$1,350 USD, which puts it **at the high end** of current market prices but not outrageous given the hype.

**Critical caveats — this is the important part**

The 8GB models reportedly reach 64GB, while others are stable only at lower capacities. Memory stability and bandwidth can also differ depending on the quality of the HBM dies. Reports suggest that 8GB cards using Hynix memory may be more stable when expanded toward 64GB.

Not everyone is going to see the fully unlocked memory stack because the CMP 170HX is based on a lower bin of the original A100 Ampere GPU, and most of these HBM2e stacks are disabled due to the use of defective or subpar memory dies.

In plain terms: **64GB is not guaranteed.** Many cards stabilize at 32GB or less.

**Hardware background**

NVIDIA used GA100 dies that were rejected during production of the A100. Instead of scrapping the rejects, they disabled some CUDA and Tensor cores and cut the memory to 8 or 10GB. So you're buying a defective chip that *might* expose its full potential.

**Requirements to run the unlock**

You need Linux (x86-64), root access, nvidia-open 610.43.0x already installed, kernel headers matching the running kernel, Secure Boot disabled, and Python 3. No Windows support.

**Verdict**

| Factor | Assessment |
| --- | --- |
| Price (¥9,800) | Slightly high for the risk involved |
| 64GB unlock guarantee | ❌ Not guaranteed — chip lottery |
| Compute performance | ✅ GA100 architecture, excellent bandwidth |
| Linux-only | ⚠️ No Windows support |
| Use case | AI inference, LLM running, not gaming |

**Recommended only if:** you're willing to gamble on the memory unlock working fully, you run Linux, and you need a cheap way to experiment with large AI models. If you need a guaranteed 64GB, this is not it. If you get lucky with a good die, it's fantastic value. Negotiate the price down to ¥7,000–8,000 to offset the risk.

---

**References:**

- [cmpunlocker GitHub](https://github.com/amoghmunikote/cmpunlocker)
- [CMP 170HX prices surge past $1,000 after unlock tool](https://www.digitalcitizen.life/nvidia-cmp-170hx-prices-surge-past-1000-after-tool-unlocks-up-to-80-gb-of-vram/)
- [WCCFTech: Prices explode from $100 to $1,000+](https://wccftech.com/nvidia-cmp-170hx-8-10-gb-prices-explode-over-1000-usd-as-tool-unlocks-hidden-64-80gb-vram/)
- [Bytwork: A100-level benchmarks & background](https://bytwork.com/en/hw/videocards/cmp-170hx)
