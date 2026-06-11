---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Marvell：定制AI芯片与互连
translated: true
type: note
---

**问题：** 介绍一下芯片公司 Marvell。

**回答：**

Marvell Technology（纳斯达克：MRVL）是目前 AI 基础设施建设中最重要的半导体公司之一——在定制 AI 芯片领域，可以说是仅次于 Broadcom 的第二大玩家。公司由 Sehat Sutardja、其妻子 Weili Dai 及其兄弟 Pantas Sutardja 于 1995 年创立，总部位于圣克拉拉，拥有约 7480 名员工，2026 财年营收达 81.9 亿美元。其首款产品是用于硬盘驱动器的 CMOS 读取通道——在头二十年里，Marvell 主要被视为存储控制器和网络芯片供应商（你旧硬盘里很可能就有一颗 Marvell 控制器）。

**向数据基础设施的转型。** 转型始于 2016 年 Matt Murphy 出任 CEO，他将公司重新聚焦于数据中心基础设施和定制芯片。2021 年以 100 亿美元收购 Inphi，带来了关键的电子光学和互连技术，营收从 2023 财年的 55 亿美元增长至 2026 财年的 82 亿美元。同时剥离非核心业务——2025 年 8 月，以 25 亿美元现金将汽车以太网业务出售给英飞凌。

**如今他们实际制造什么。** 作为 AI 工程师，你需要关注三大支柱：

1. **定制 AI ASIC（XPU）**——当超大规模云厂商想要自己的加速器而非购买 Nvidia GPU 时，Marvell 就是他们的设计合作伙伴。该公司已与亚马逊的 Trainium 以及谷歌的 Axion 相关项目合作。商业模式：超大规模厂商拥有架构，Marvell 提供物理设计、先进封装、SerDes、HBM 集成以及台积电合作关系。随着亚马逊、谷歌、微软和 Meta 纷纷扩大专有芯片项目，定制 AI 芯片的潜在市场规模预计到 2028 年将超过 400 亿美元。

2. **互连 / 电子光学**——这是 Inphi 的 DNA。包括 PAM4 和相干 DSP、激光驱动器、跨阻放大器、硅光子、共封装光学以及线性可插拔光学芯片组。当你在 10 万 GPU 集群上进行训练时，机架间的光链路就运行在这类芯片上。这部分正是 Jensen Huang 所关心的。

3. **网络**——以太网控制器、网络适配器、PHY、交换机和光纤通道适配器，以及 DPU（OCTEON 系列）。

**为何现在如此火爆。** 在 2026 年 Computex 上，Jensen Huang 称 Marvell 为“下一个万亿美元公司”，次日股价飙升近 33%，创下其单日最大涨幅。Nvidia 已于 3 月承诺向 Marvell 投资 20 亿美元。Huang 的逻辑直接源于规模定律的经济学：随着计算分布在巨型集群中，连接性成为关键——互连带宽，而非 FLOPs，正日益成为前沿训练任务的瓶颈。Marvell 于 6 月 22 日加入标普 500 指数，过去 12 个月股价回报率达 274%。业绩指引：2027 财年营收约 115 亿美元（同比增长 40%），其中互连业务增长超过 70%，2028 财年预计约 165 亿美元。

**核心思路：** Nvidia 销售计算能力；Broadcom 和 Marvell 销售*替代*计算（定制 ASIC）以及让这一切在集群规模下运行的“布线”。市值约在 2200–2530 亿美元之间，因此市场将其定位为核心 AI 基础设施公司，而非传统芯片供应商。

主要风险，直接来自其 10-K 文件：数据中心终端市场的客户高度集中，以及客户垂直整合并开发自家解决方案的风险——即超大规模厂商自建物理设计团队，这对 ASIC 业务构成生存威胁。

如果你想深入了解，技术上有趣的线索包括 224G SerDes 设计、PAM4 与相干 DSP 调制，以及共封装光学——这些才是 Marvell 真正的护城河所在。

**参考资料：**

- [Marvell Q4 & FY2026 业绩（investor.marvell.com）](https://investor.marvell.com/news-events/press-releases/detail/1011/marvell-technology-inc-reports-fourth-quarter-and-fiscal-year-2026-financial-results)
- [Marvell FY2026 年报（SEC）](https://www.sec.gov/Archives/edgar/data/0001835632/000110465926060265/tm261486d6_ars.pdf)
- [Marvell Technology — 维基百科](https://en.wikipedia.org/wiki/Marvell_Technology)
- [MRVL — Yahoo Finance](https://finance.yahoo.com/quote/MRVL/)
- [Barchart: Marvell 于 6 月 22 日加入标普 500](https://www.barchart.com/story/news/2407602/dear-marvell-technology-stock-fans-mark-your-calendars-for-june-22)