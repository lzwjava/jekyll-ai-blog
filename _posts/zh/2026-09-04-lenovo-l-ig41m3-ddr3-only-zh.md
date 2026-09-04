---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想L-IG41M3：仅支持DDR3
translated: true
type: note
---

问题：联想 L-IG41M3 主板是否支持 DDR4 内存？  
回答：**不，联想 L-IG41M3 不支持 DDR4。** 它仅支持 **DDR3** 内存。

原因如下：

- L-IG41M3 基于 **Intel G41 芯片组** 并采用 **LGA775 插槽**——它需要使用 **PC3-8500（1066 MHz）或更慢速率的 DDR3 内存**。
- 根据其规格，它最高支持 **800 MHz** 的内存频率。
- DDR4 是完全不同的物理标准——内存模组上的缺口位置不同，因此 **物理上无法插入** DDR3 插槽。

**快速总结：**

| 特性 | L-IG41M3 支持情况 |
|---|---|
| DDR3 | ✅ 是（最高 1066 MHz） |
| DDR4 | ❌ 否 |
| 最大内存速度 | 800–1066 MHz |
| 插槽 | LGA775（非常旧的代际） |

> ⚠️ **注意：** 即使升级到更快的 DDR3（例如 DDR3-1600）也可能在此主板上导致启动问题。建议使用较旧、密度较低的 DDR3 内存条——最好为 **2×4GB DDR3-1333 MHz 1.5V** 规格。

这是一个非常老的平台（约 2008–2009 年）。如果需要 DDR4 支持，则需要全新的主板、CPU 和内存。

参考来源：
- [Lenovo L-IG41M3 主板指南 – Alibaba Electronics](https://electronics.alibaba.com/buyingguides/lenovo-l-ig41m3-motherboard-guide)
- [哪些内存支持 L-IG41M3 – Tom's Hardware 论坛](https://forums.tomshardware.com/threads/which-ram-supports-lenovo-l-ig41m3-motherboard.2530280/)
- [L-IG41M3 内存不兼容 – Tom's Hardware 论坛](https://forums.tomshardware.com/threads/possible-ram-incompatibility-l-ig41m3-old-motherboard.3787600/)