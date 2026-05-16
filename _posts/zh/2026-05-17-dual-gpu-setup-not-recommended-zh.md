---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双GPU设置不推荐
translated: true
type: note
---

**问题：** 我可以在已经装有MSI RTX 4070 GPU的京东电脑上添加一块AMD GPU吗？

**回答：**

## 简短回答：技术上可行，但不推荐用于游戏

AMD GPU与Intel CPU完全兼容。AMD和Intel都遵循PCIe等通用行业标准，因此在硬件层面没有跨品牌限制。但你的具体情况是在已有RTX 4070的系统中添加*第二块*GPU，这完全是另一回事。

---

## 1. CPU × AMD GPU 兼容性 — 不是问题

AMD GPU与Intel CPU的兼容性通常很简单，因为GPU和CPU在系统架构中基本独立运行。关键因素是主板的芯片组和可用的PCIe插槽，它们负责GPU与CPU之间的通信。

因此，将Intel i9-13900KF与AMD GPU搭配使用完全没问题。

---

## 2. 你的主板（MSI MAG B760M Mortar WiFi）能否支持第二块GPU？

这里才是真正的限制所在。MSI MAG B760M Mortar WiFi是一款**Micro-ATX（mATX）**主板。它有一个PCIe 5.0插槽，但mATX主板通常只有**一个全长PCIe x16插槽**。第二块GPU需要插入较小的PCIe x1或x4插槽，这将严重限制带宽，并且物理上也不适合全尺寸独立GPU。

简而言之：**你的主板无法以有意义的方式同时容纳两块全尺寸GPU。**

---

## 3. 混合品牌双GPU（RTX 4070 + AMD）— 不支持游戏用途

即使你有物理插槽，混合使用GPU品牌也无法实现联合游戏性能。问题在于使用不同显卡的多GPU设置。除非你的系统中是兼容的APU与AMD GPU组成双显卡配置，否则多GPU设置必须使用相同型号的显卡。

现代游戏和渲染引擎不支持跨品牌GPU协作。NVIDIA的NVLink/SLI和AMD的CrossFire仅在相同品牌（通常是相同GPU型号系列）内有效——而且这些技术在当今游戏中已基本**被弃用**。

---

## 4. 关于AMD Smart Access Memory (SAM)？

如果你想用AMD GPU替换RTX 4070，请注意AMD Smart Access Memory仅在你同时拥有AMD CPU和AMD GPU时才有效。由于你使用的是Intel CPU，你将无法享受到SAM带来的收益。这影响不大（某些游戏中约5-15%的性能提升），但并非决定性因素。

---

## 5. 电源供应问题

你的配置使用**Corsair CX650F 750W电源**。RTX 4070在负载下功耗约200W，i9-13900KF可达250W。添加第二块GPU（即使是中端AMD显卡，功耗150-200W）将使系统总功耗超过600W，接近或超过电源的安全工作范围。**这会存在风险。**

---

## 总结表

| 考虑因素 | 结论 |
|---|---|
| Intel CPU + AMD GPU 兼容性 | ✅ 完全兼容 |
| B760M Mortar WiFi 支持两块完整GPU | ❌ 仅有一个PCIe x16插槽 |
| RTX 4070 + AMD GPU 用于游戏 | ❌ 不支持（不同品牌） |
| AMD SAM 在Intel CPU上生效 | ❌ 不可用 |
| 750W电源用于双GPU | ⚠️ 可能不足 |
| 机箱（Aigo Mini）容纳两块GPU | ❌ 迷你机箱很少支持双GPU |

---

## 建议

你现有**仅用RTX 4070的配置**在1440p甚至4K游戏上表现出色。在这个特定配置中添加一块AMD GPU因主板、机箱、电源和软件限制并不实际。如果未来需要更强GPU性能，最佳方案是**更换**RTX 4070为更高端的显卡，而不是添加第二块。

**参考来源：**

- [Can You Use A AMD GPU With An Intel CPU – techygpu.com](https://www.techygpu.com/2024/09/26/can-you-use-a-amd-gpu-with-an-intel-cpu/)
- [Can You Use An AMD GPU With An Intel CPU? – cgdirector.com](https://www.cgdirector.com/use-amd-gpu-with-intel-cpu/)
- [AMD GPU with Intel CPU Compatibility – computerknown.com](https://computerknown.com/can-you-use-a-amd-gpu-with-an-intel-cpu/)
- [MSI MAG B760M MORTAR WIFI – us.msi.com](https://us.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/)
- [PCPartPicker: Intel CPU with AMD GPU discussion](https://pcpartpicker.com/forums/topic/98670-i-can-use-a-intel-cpu-with-a-amd-gpu)