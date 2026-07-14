---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ti in NVIDIA Graphics Cards
translated: false
type: note
---

Question: What does "Ti" mean in NVIDIA card names like RTX 5060 Ti?

Answer:

"Ti" = Titanium. It's NVIDIA's suffix for a higher-binned, more fully-enabled version of a base chip, sitting between the plain model and the next tier up.

Concretely, within one GPU die (e.g. GB206 here):

- Non-Ti (RTX 5060): fewer CUDA cores enabled, lower clocks, often less VRAM, lower TDP
- Ti (RTX 5060 Ti): more cores unlocked on the same die, higher clocks, usually more VRAM/wider bus, higher TDP

Example on this generation:

- RTX 5060 8GB: 3840 CUDA cores, 145W TDP
- RTX 5060 Ti 16GB: 4608 CUDA cores, 180W TDP, same 128-bit bus but full GDDR7 capacity

It's purely a market segmentation label — no fixed rule (doesn't always mean "same die, better bin"; sometimes it's a different die entirely, like RTX 4070 vs 4070 Ti being different GPUs). Historically it dates back to GeForce 2 Ti (2000). No architectural meaning beyond "better SKU in the stack," unlike "Super" (mid-cycle refresh) or "Founders Edition" (NVIDIA reference board).

For your case: the naming tells you nothing about bandwidth/VRAM tradeoffs for inference — always check the actual spec sheet (bus width, GB/s, VRAM) rather than trusting the tier name.
