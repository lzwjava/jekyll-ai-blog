---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为MI50选择B550主板
translated: true
type: note
---

问题：使用 R5 5600（AM4）+ 一块二手 MI50 16GB（数据中心显卡，无显示输出），如何选择主板？

答案：

这里的瓶颈不在 CPU，而在 MI50。它是一块被动散热、无显示输出的计算卡，需要 BIOS 中许多消费级 AM4 主板默认缺少或隐藏的功能。根据实际部署报告确认：需要禁用 CSM（禁用传统 BIOS 启动）、启用 Above 4G Decoding，并支持 ReBAR。有用户特别提到，由于旧款 AM4 主板的 BIOS 中根本没有“Above 4G decoding”选项，他们不得不购买新主板。该显卡需要双 8-pin PCIe 供电，物理上运行在 PCI Express 4.0 x16 插槽中，但向下兼容 Gen3。

**芯片组选择：B550，而非 A320/B450。**

| 芯片组 | Above 4G Decoding | 结论 |
| --- | --- | --- |
| A320 | 旧固件上经常缺失/不完整 | 避免 |
| B450 | 部分主板有，早期 BIOS 版本缺失——取决于品牌/AGESA 版本 | 有风险，先确认手册 |
| B550 | 所有现代 UEFI（2020+）标配，原生 PCIe4 | **推荐** |
| X570 | 与 B550 相同 + 保证 Gen4 x16 电气连接，PCIe4 芯片组通道 | 对于此组合性能过剩——5600 + MI50 不会跑满 Gen3 x16 带宽 |

购买 B550，省下 X570 的溢价。任何具备全长 x16 插槽的 B550 ATX/mATX 主板均可。

**购买前，请检查具体型号的手册中是否有：**

1. BIOS 中的 `Above 4G Decoding` 开关（搜索“[主板型号] above 4g decoding”——大多数技嘉/华硕/华擎/微星的 B550 主板都位于 Advanced → PCI Subsystem Settings 下）
2. 两个 8-pin PCIe 接口或电源需提供两个——主板不给 GPU 供电，但请确认机箱空间足够，因为卡体加上被动散热器长度较长
3. 插槽间距——MI50 是双槽被动散热，因此第二个插槽（M.2 散热片、芯片组风扇）需要留出空间
4. MI50 无显示输出——利用 5600 的核显……等等，普通 5600 **没有核显**（带核显的是 5600G/5600GT）。你需要一块单独的廉价显示 GPU 或能无头启动的方式，因为 MI50 不会显示 BIOS/POST。

最后一点才是真正的陷阱：请确认你另有办法看到 POST/BIOS 输出，因为 MI50 在 Linux 加载 ROCm 之前不会输出任何画面。

**实用建议：** 任选一块 B550 主板（技嘉 B550 AORUS Elite、微星 B550-A PRO、华擎 B550M Pro4）+ 一块备用廉价 GPU 或主板自带显示接口（用于初始设置）+ 一个对准 MI50 的被动 120mm 风扇支架，因为该卡出厂不带风扇，采用双槽被动散热，在非服务器机箱中需要强制风道。

参考：

- [MI50 实际 Above 4G Decoding 要求 — Willy Tarreau](http://wtarreau.blogspot.com/2025/12/amd-radeon-instinct-mi50-32gb-best-ai.html)
- [MI50 VBIOS/BIOS 设置要点](https://gist.github.com/evilJazz/14a4c82a67f2c52a6bb5f9cea02f5e13)
- [MI50 32GB PCIe 4.0 列表，供电/插槽规格](https://www.ebay.de/itm/397226850914)
