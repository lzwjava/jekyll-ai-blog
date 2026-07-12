---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI50 双8针PCIe电源连接器
translated: true
type: note
---

问题：在 AMD Instinct MI50 上，它的两个电源接口是什么，这两个 8-pin 接口类型相同还是不同？

回答：

MI50（Vega 20，7nm，被动散热双槽卡，300W TDP）使用**两个完全相同的 8-pin PCIe 风格电源接口**——不是 6+8 的组合，也不是一个 CPU/EPS 加一个 PCIe。多家零售商的列表直接证实了这一点：其 300W 的最大功耗来自 2 个 8-pin 电源连接，servershop24 的 SKU 规格明确将其列为 "300W / 2x8P-PCIe"。

所以直接回答：**是的，这两个 8-pin 接口类型相同**——它们都是标准的 8-pin PCIe（6+2 pin）接口，与普通游戏显卡上的插口完全相同。它们的防呆设计没有区别，你无需担心哪根线缆插哪个接口——来自你电源（PSU）的任何一根 PCIe 8-pin 线缆都可以插入任意一个接口，具有相同的线路（12V 供电线路 + 检测引脚），相同的额定电流（每个接口约 150W，合计 300W）。

**关于旧报道的注意事项**：2018 年一篇 Tom's Hardware 的文章声称该卡采用 6-pin + 8-pin 的组合，依赖一个 6-pin 和一个 8-pin PCIe 电源接口——这似乎是发布时的早期/错误报告；此后所有的实际硬件列表和规格表（technical.city, itcreations, servershop24）都确认是 2x 8-pin，而非 6+8。请相信硬件列表而非发布当天的文章。

**搭建机器时的一个实际注意事项**：某些 OEM 服务器机箱（如 HPE ProLiant）为 MI50 配备了专有供电线束——一套 "8-pin 转 2x 8-pin (PCIe)" 的线缆套件——这意味着来自服务器背板的单个 8-pin 接口会分成两个 8-pin GPU 输入。如果你打算从 HPE 服务器机箱中拆出一块 MI50 用于 DIY 组装（这很常见，因为这些卡会从退役的 Radeon Instinct/MI50 集群中以二手的便宜价格出现），你需要来自你电源的标准双 PCIe 8-pin 线缆，而不是 HPE 的专用分线器——该分线器是机箱特定的，无法正确映射到普通 ATX 电源的线路布局。

给你的机器做个实用检查：如果你计划将它与你现有的 RTX 4070 工作站一起使用，或者搭建一个多 GPU 推理机，只需从电源直接连接两条独立的 PCIe 8-pin 线缆到显卡（避免使用单根电源线上的两个接口进行 daisy-chaining 连接——在总计 300W 功耗的情况下，应尽可能使用两条独立的线路/线缆，以确保每条线缆的功耗保持在其约 150W 的安全余量内）。

参考资料：

- [AMD Radeon Instinct MI50 - technical.city](https://technical.city/en/video/Radeon-Instinct-MI50)
- [AMD Radeon Instinct MI50 GPU - itcreations.com](https://www.itcreations.com/amd-gpu/amd-radeon-instinct-mi50-gpu)
- [AMD RADEON INSTINCT MI50 GPU - Servershop24](https://www.servershop24.de/en/amd-radeon-instinct-mi50-gpu/a-133803/)
- [PCIe 8-pin vs EPS-12V 8-pin power connections - Exxact](https://support.exxactcorp.com/hc/en-us/articles/20180443940119-PCIe-8-pin-vs-EPS-12V-8-pin-power-connections)
