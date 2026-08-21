---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4090D与4090的区别
translated: true
type: note
---

**问题：** RTX 4090D 与 RTX 4090 有何区别？

**回答：**

RTX 4090D 是 RTX 4090 的中国特供版本，专为遵守美国出口限制而设计。以下是具体差异：

**为何存在**

美国出口管制禁止向中国出口满规格的 RTX 4090，因其 AI 算力超出监管阈值。英伟达推出了 RTX 4090D（"D" 代表 "Domestic"），仅面向中国大陆市场。

**关键规格差异**

| | RTX 4090 | RTX 4090D |
| --- | --- | --- |
| CUDA 核心 | 16,384 | 14,592 |
| TDP | 450W | 425W |
| 显存 | 24GB GDDR6X | 24GB GDDR6X |

4090D 采用 AD102-250 GPU，核心数更少，但其他方面与标准版 4090 基本一致。

**性能差距**

4090D 的综合性能约为 RTX 4090 的 95%，即多数场景下存在约 5% 的差异。在 2K 或 4K 游戏测试中，帧率差距通常在个位数。

**超频注意事项**

华硕定制的 ROG Strix RTX 4090D 可通过超频将 TDP 从 425W 提升至 600W，在某些基准测试中甚至能超越标准版 RTX 4090。

简而言之：4090D 是针对中国市场的略微弱化版本，根据工作负载不同，性能下降约 5–10%，但显存相同，功耗略有降低。

**参考来源：**

- [RTX 4090 China Guide: 4090 vs 4090D Explained](https://electronics.alibaba.com/buyingguides/rtx-4090-china-guide-4090-vs-4090d-explained)
- [RTX 4090 vs 4090D – Oreate AI Blog](https://www.oreateai.com/blog/rtx-4090-vs-4090d-unpacking-the-nuances-of-nvidias-flagship-gpus/346eabc62c7e033966dab3fef1107ca4)
- [ASUS RTX 4090D Outperforming RTX 4090 – Game Rant](https://gamerant.com/asus-rtx-4090d-outperforming-rtx-4090/)
