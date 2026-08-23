---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMP 170HX Unlock Rental Status
translated: false
type: note
---

**Question:** Are people currently renting out the unlocked CMP 170HX (64GB) on RunPod?

**Answer:**

This is a very fresh topic — the CMP 170HX unlock only became widely known a few weeks ago. Here's the honest picture:

**What the CMP 170HX unlock actually is:**

The CMP 170HX is the flagship SKU in Nvidia's CMP series and leverages the GA100 (Ampere) silicon — the same chip as the A100. A software tool called "CMPUnlocker" has restored the previously locked-away memory, boosting its memory capacity by up to 8x — from just 8GB to a massive 64GB.

**Can you list it on RunPod? Not really, currently:**

There's no evidence anyone is successfully running unlocked 170HX cards on RunPod's Community Cloud right now. The reasons are practical:

- Getting a card to report a larger memory size is not the same as proving that memory is reliable under sustained load. Independent testers have flagged inconsistent behavior at the outer edges of unlocked capacity, and outcomes vary from card to card depending on the specific memory chips and silicon binning involved. Without ECC, memory errors that would normally be caught and corrected on a real A100 can instead silently corrupt data.

- The PCIe Gen 2 x4 limitation slows down loading of neural network weights, but the actual computations are fast once loaded. This bandwidth bottleneck is a real problem for renters doing serious workloads.

- Stability at 64GB is not guaranteed — the original research paper only got 40GB to work reliably under stress. Some users report 64GB working, others report instability. The card also has no FP8/FP4 support, so it's not as fast as a 5090 despite the VRAM.

- RunPod's Community Cloud vets hosts — a hacked mining card with an unofficial firmware exploit is unlikely to pass their onboarding checks.

**Where people ARE experimenting with it:**

Secondhand listings for the 170HX have picked up, with some sellers marketing unlocked cards as inexpensive options for local AI inference, pointing to the card's roughly 1.5 TB/s memory bandwidth as a genuine draw for memory-bound workloads. The use case right now is mostly **personal/local inference**, not cloud rental.

**Vast.ai** would be the more realistic platform for something like this since it's a truly open marketplace where individual hosts set their own listings — but even then, renters may reject it due to the instability risks.

**Bottom line:** The unlock is real and exciting, but it's too new, too unstable, and too unvetted for platform rental at this point. Give it a few months to see if the community stabilizes the 64GB unlock reliably before thinking about cloud hosting it.

**References:**

- [Tom's Hardware — CMP 170HX VRAM Unlock](https://www.tomshardware.com/pc-components/gpus/nvidia-crypto-mining-gpus-hacked-to-restore-locked-away-vram-in-order-to-feed-ai-boom-software-mod-unlocks-64gb-of-vram-on-usd250-cmp-170hx)
- [WCCFTech — CMP 170HX Price Explosion](https://wccftech.com/nvidia-cmp-170hx-8-10-gb-prices-explode-over-1000-usd-as-tool-unlocks-hidden-64-80gb-vram/)
- [PBX Science — Unlocking the CMP 170HX](https://pbxscience.com/unlocking-the-cmp-170hx-how-far-the-community-has-actually-gotten-toward-an-a100-on-the-cheap/)
- [Bytwork — CMP 170HX Unlock Guide](https://bytwork.com/en/articles/cmp-170hx-unlock)
