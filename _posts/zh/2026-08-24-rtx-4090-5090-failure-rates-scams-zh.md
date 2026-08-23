---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4090 5090 故障率与骗局
translated: true
type: note
---

**问题：** RTX 4090和5090显卡的缺陷/故障率是多少？在eBay或闲鱼上出售的破损显卡情况如何？

**回答：**

---

## RTX 4090 — 故障率

4090在发布时遇到了所谓的“Cablegate”——12VHPWR接口熔化问题。实际数据如下：

- 根据NVIDIA合作伙伴和线缆供应商的信息，4090接口故障率估计约为 **0.05–0.1%**。
- 对约19.3万张已发货显卡进行的更广泛分析发现，约有260起经证实的故障——总体约为 **0.13%**。最主要的故障类型（占65%的案例）是16针电源接口未完全插紧。
- 此外，一家菲律宾零售商4年的RMA数据显示，不同品牌的GPU故障率差异很大——**技嘉为5%，微星为1.5%**。
- 一家瑞士零售商（Digitec Galaxus）发布了24个月的数据，显示了品牌缺陷率，最差的是 **蓝宝石为2.5%**，其次是华擎（2.1%）、XFX（2%）、技嘉（1.9%）、EVGA和索泰（1.8%）。

除了接口问题外，还有一个4090因体积和重量过大而特有的物理损坏问题：

- 维修技师NorthwestRepair报告称，一波4090显卡出现 **GPU插槽附近的PCB焊盘撕裂**，这是由于运输损坏或显卡未安装支撑支架所致——这可能是无法修复的损坏。
- 另一家维修渠道NorthridgeFix曾 **从单个客户处收到19张RTX 4090**，几乎所有显卡都在 **PCIe支架附近的PCB出现裂纹**——这一趋势与显卡日益加重有关。

---

## RTX 5090 — 发布即更糟

5090发布时带来了更严重的系统性问题：

- NVIDIA证实，**不到0.5%** 的RTX 5090/5090D和5070 Ti显卡出货时 **缺少一个指定的ROP（渲染输出单元）**，导致性能下降约4%。
- 多个AIB品牌——七彩虹、万丽、技嘉和华硕——都记录了早期故障，表现为显卡根本 不出现在Windows设备管理器、BIOS或NVIDIA驱动程序中。硬件分析师Der8auer得出结论，这指向 **一个基础架构或驱动兼容性问题**，而非孤立的制造缺陷，且与仓促实施的PCIe Gen 5有关。
- 5090也重复出现了接口熔化问题。微星自有品牌的16针电源线（单接头）显示的故障少得多，而NVIDIA提供的转接线是主要问题所在。
- 就在2016年8月，一张PNY RTX 5090在视频编辑过程中 **16针接口附近发生电容器爆炸**——产生烟雾、巨响，并完全失去显示。

---

## 二手市场 — eBay、闲鱼

对于买家来说，这里的情况真正变得危险：

**骗局显卡——无核心的空壳：**

- 骗子以约200美元的价格购买损坏/被拆解的4090，然后将其作为工作正常的显卡出售。维修渠道已经曝光了 **没有GPU芯片且完全没有显存** 的电路板——只是一个装在空白PCB上的散热器。
- 一种常见的骗局是移除GPU核心和显存，然后转售这些芯片牟利，或将它们改装到其他PCB上。 <br>在中国，**RTX 5090芯片和GDDR7显存模块被移植到适用于AI服务器的涡轮卡上**——留下被掏空的零售版空壳，然后通过二手市场转售，通常不提供退货选项。
- 这种AI服务器改装市场在中国很大。移植过程剩余的散热器和PCB组件随后被转售给其他公司——最终以看似完整的显卡形态到达不知情的买家手中。

**合法的损坏显卡市场（用于维修/零件）：**

- 一些零售商合法地出售损坏的RTX 5090，价格低至1760美元——这些显卡在运输过程中损坏，但所有组件仍在PCB上，仅面向维修专业人员或回收用途。
- 闲鱼上的中国卖家出售单个维修组件，例如NVIDIA PCIe接口，让人们能够在昂贵的显卡上进行板级维修，而不是完全报废它们。

**假卡问题：**

- 骗局已经变得非常复杂，以至于一张送修的显卡竟然被证明是 **一张假卡，带有激光雕刻的GPU芯片，看起来像真的一样**——核心和显存是对功能毫无用处的逼真复制品。

---

## 总结

| 显卡型号 | 接口故障 | 总体缺陷 | 二手市场风险 |
| --- | --- | --- | --- |
| RTX 4090 | ~0.05–0.13%（Cablegate） | 按品牌计1.5–5% | 高——空壳很常见 |
| RTX 5090 | 持续中（相同问题） | ~0.5%+ ROP缺陷 + 变砖 | 非常高——骗局 + AI零件剥离 |

如果购买二手：**务必在付款前要求提供显卡在系统中启动的视频**，并且对价格低于市场价约15–20%的选项保持极度怀疑。

---

**参考文献：**

- [ExpertBeacon — RTX 4090 故障率分析](https://expertbeacon.com/what-is-the-failure-rate-of-rtx-4090/)
- [Tom's Hardware — 各品牌GPU故障率](https://www.tomshardware.com/news/retailer-shares-failure-rates-for-gpus-motherboards-ssds-more)
- [Tweaktown — 瑞士零售商GPU缺陷数据](https://www.tweaktown.com/news/93052/heres-look-at-gpu-failure-rates-and-warranty-claim-times-for-all-major-brands/index.html)
- [TechPowerUp — RTX 5090 变砖报告](https://www.techpowerup.com/332047/reports-of-bricked-nvidia-geforce-rtx-5090-and-rtx-5090d-surge)
- [VideoCardz — 维修店出现的骗局RTX 5090显卡](https://videocardz.com/newz/scam-geforce-rtx-5090-cards-with-missing-gpu-and-memory-now-showing-up-in-repair-shops)
- [Tom's Hardware — 客户收到被掏空的RTX 5090](https://www.tomshardware.com/pc-components/gpus/retailer-ships-rtx-5090-with-missing-gpu-and-memory-chips-to-customer-defaced-gpu-took-over-a-year-to-ship)
- [TechRadar — 二手市场上的破损4090](https://www.techradar.com/computing/gpu/broken-and-gpu-less-rtx-4090s-are-being-sold-secondhand-by-scammers)
- [Wccftech — RTX 5090 接口熔化追踪器](https://wccftech.com/roundup/nvidia-rtx-5090-16-pin-connector-melting-issues-tracker/)
