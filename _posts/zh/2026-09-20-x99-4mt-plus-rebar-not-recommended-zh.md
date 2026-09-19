---
audio: false
generated: true
image: false
lang: zh
layout: post
title: X99-4MT Plus ReBAR 不推荐
translated: true
type: note
---

**问题：** 华南X99-4MT Plus + E5-2673 V3组合对于ReBAR和大于4G解码来说好吗？

**回答：**

这里有两个独立的问题——主板和CPU。让我们来分别分析。

---

**主板：华南X99-4MT Plus**

“4MT”后缀意味着这是华南X99 micro-ATX系列中的**DDR3**版本，而不是BD4（DDR4）。这是一个关键区别——BD4是已确认在BIOS中原生支持大于4G解码和ReBAR的型号。而4MT/4MF/4MD系列主板是预算级的DDR3主板，共享更简单、更精简的BIOS。

目前没有社区特定文档确认X99-4MT Plus原生支持大于4G解码或ReBAR。考虑到中国X99 DDR3主板（精粤D3、Machinist D3等）的普遍情况，原生支持的可能性非常低。BIOS修改可能可行，但对于这个特定型号来说属于未开发领域——它没有BD4所拥有的、有据可查的BIOS交换路径。

**该主板对ReBAR的结论：⚠️ 如果ReBAR是主要需求，则不推荐。**

---

**CPU：E5-2673 V3**

2673 V3是一款Haswell-EP至强处理器，拥有12核24线程，基础频率2.4 GHz，睿频3.1 GHz（部分来源指出单核睿频最高可达3.6 GHz），30 MB三级缓存，TDP为105 W。它最初是Azure云CPU（微软OEM），并非零售部件——这就是它在二手市场上如此便宜的原因。它在LGA2011-3消费级主板上完全可用且被广泛使用。

与之前组合中的2680 V4相比，2673 V3的参数如下：

| | E5-2673 V3 | E5-2680 V4 |
| --- | --- | --- |
| 架构 | Haswell (V3) | Broadwell (V4) |
| 核心 / 线程 | 12核 / 24线程 | 14核 / 28线程 |
| 基础 / 睿频 | 2.4 / 3.1 GHz | 2.4 / 3.3 GHz |
| 缓存 | 30 MB | 35 MB |
| 内存 | DDR4 | DDR4 |
| TDP | 105 W | 120 W |
| IPC | 较低 (Haswell) | 较高 (Broadwell) |

2673 V3是一款性价比不错的CPU，但2680 V4明显更好——核心更多，架构更新，IPC更高，睿频也稍高。如果你在这两者之间选择，之前推荐的BD4 + 2680 V4组合在每个方面都是更强的选择。

---

**总体结论**

X99-4MT Plus + 2673 V3是一个**不错的多功能预算装机选择**，但如果ReBAR和大于4G解码是需求，那么这个组合就有所欠缺。DDR3主板是较弱的一环——未确认支持ReBAR，而且社区路径（华南BD4 BIOS交换）可能不兼容DDR3主板。你将面临很大的不确定性。

**如果原生ReBAR对你很重要，那么之前讨论的华南X99 BD4 + E5-2680 V4组合仍然是明确的推荐。**

---

**参考资料：**

- [指南：中国X99主板的超频BIOS修改 – WinRaid](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683)
- [E5-2673 V3规格 – OpenBenchmarking](https://openbenchmarking.org/s/Intel+Xeon+E5-2673+v3)
