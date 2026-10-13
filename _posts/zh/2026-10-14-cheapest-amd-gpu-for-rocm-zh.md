---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 适用于ROCm的最便宜AMD GPU
translated: true
type: note
---

## 4. 我会研究的最便宜选项

**AMD Instinct MI25 16GB** 值得考虑，如果你的首要目标是尽可能低的购买价格，并且你愿意尝试旧版软件。但不要指望它能获得现代 ROCm 支持就购买它。

为了更可靠的设置，MI100 是更好的目标。AMD 的 ROCm 10.1 支持列表包含 MI100（`gfx908`），但不包含 MI25 或 MI50。[AMD ROCm](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html?utm_source=chatgpt.com)

你可以比较 [MI25 列表](https://www.google.com/search?q=AMD+MI25+16GB+used+GPU) 和 [MI100 列表](https://www.google.com/search?q=AMD+MI100+32GB+used+GPU)。

**有一个细节最重要：你每块 GPU 的最大预算是多少——¥200、¥500 还是 ¥1,000？** 我会把选择范围缩小到适合你预算的显卡，并区分官方 ROCm 支持与社区变通方案。