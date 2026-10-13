---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cheapest AMD GPU for ROCm
translated: false
type: note
---

## 4. The cheapest option I'd investigate

**AMD Instinct MI25 16GB** is worth considering if your priority is the lowest possible purchase price and you're willing to experiment with legacy software. But don't buy it expecting modern ROCm support.

For a more dependable setup, the MI100 is a better target. AMD's ROCm 10.1 support list includes the MI100 (`gfx908`), but not the MI25 or MI50. [AMD ROCm](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html?utm_source=chatgpt.com)

You can compare the [MI25 listings](https://www.google.com/search?q=AMD+MI25+16GB+used+GPU) and [MI100 listings](https://www.google.com/search?q=AMD+MI100+32GB+used+GPU).

**One detail matters most: what's your maximum budget per GPU — ¥200, ¥500, or ¥1,000?** I'll narrow the choices to cards that fit your budget and distinguish official ROCm support from community workarounds.
