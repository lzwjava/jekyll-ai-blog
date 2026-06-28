---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 5090价格受内存紧缺推动
translated: true
type: note
---

问题：RTX 5090涨价是否由AI/算力需求推动——32GB GDDR7使本地LLM推理/训练更具吸引力、中国出口受限的数据中心显卡推高专业消费者需求，加上2025-2026年DRAM/GDDR成本压力？

让我核实具体细节，而非简单同意。

问题：RTX 5090涨价是否由AI/算力需求推动——32GB GDDR7使本地LLM推理/训练更具吸引力、中国出口受限的数据中心显卡推高专业消费者需求，加上2025-2026年DRAM/GDDR成本压力？

回答：

宏观因素基本正确，但因果侧重点略有偏差。主导因素并非直接源于对5090作为AI卡的需求，而是上游的**内存供应紧张**——AI数据中心的建设正在耗尽GDDR7的供应渠道。

**证据实际显示的情况：**

主要机制是晶圆分配，而非消费端对5090的AI需求。到2026年，AI工作负载可能占用全球近20%的DRAM晶圆产能（含HBM和GDDR7需求）。HBM每GB消耗的晶圆产能约为DDR5的三倍，而GDDR7所需的晶圆面积约为普通消费级DRAM的1.7倍。由于代工厂在HBM上利润率显著更高，它们已优先降低GDDR7的分配——从而造成供应短缺。

BOM（物料成本）集中度使5090面临独特风险。RTX 5090搭载32GB GDDR7，配备512位内存总线，其生产成本对内存价格波动极为敏感。内存占RTX 5090总物料成本的80%以上。因此，使其在本地推理中具有吸引力的32GB容量，同样也是其成本脆弱性的根源——但价格变动是由输入成本驱动的，而非推理买家竞购所致。

英伟达正积极将晶圆/内存从游戏领域重新分配。据报道，英伟达将游戏GPU产量削减30-40%，以优先生产H100和H200等高利润数据中心芯片。具体而言：当制造商分配稀缺的内存芯片时，它们会优先考虑高利润的AI加速器，而非游戏显卡。

批发环节的价格传导已实际发生：英伟达对其旗舰产品GeForce RTX 5090及中国市场特供版RTX 5090D V2实施300美元的批发价上调，自2026年5月13日生效。请注意MSRP（建议零售价）的虚构性——实际售价已是原MSRP的两倍，而英伟达官网仍标注1999美元的MSRP。

**你的框架需要修正之处：**

1. **“AI/算力需求激增”作为驱动因素**——过于直接。实际激增的是对*数据中心HBM*的需求，其在代工厂层面挤占了GDDR7的产能。5090是附带损害，而非目标。这一区别很重要，因为这意味着等待“AI炒作降温”无济于事——这是结构性问题。缓解要到2028年美光新的HBM制造产能上线后才能实现。

2. **中国出口限制的角度**——有道理，但**这些来源并未将其列为价格驱动因素**。文件提到RTX 5090D V2是中国市场特供版，但将价格变动归因于GDDR7成本，而非H100/H200出口禁令将中国买家推向专业消费级显卡。这是一个合理的假设（5090D的存在正是出于出口分级），但应将其视为你的推断，而非既定事实。历史上，中国的实际限制替代效应主要流向走私的数据中心显卡和国产加速器（华为昇腾），并非大规模流向消费级5090。

3. **“内存价格上涨加剧了供应紧张”**——正确，且比你的表述更严重。近几个月内存价格上涨了数百个百分点。DRAM价格预计到2026年第二季度将上涨40%。这不是一个叠加的次要因素；它*就是*供应紧张本身。

**总结：** 你的三个因素确实存在，但请重新排序：(1) AI/HBM在代工厂层面挤占GDDR7 → (2) GDDR7稀缺+约80%的内存BOM占比 → (3) 英伟达削减游戏产量并传导成本。中国/出口角度是一个有依据的次要假设，但来源并未证实。

参考文献：

- [Why RTX 5090 Prices Keep Climbing — BuySellRam](https://www.buysellram.com/blog/why-rtx-5090-prices-keep-climbing-nvidias-wholesale-hike-and-the-gddr7-shortage-behind-it/)
- [RTX 5090 Prices Hit $4K: Memory Crisis Why — byteiota](https://byteiota.com/rtx-5090-prices-hit-4k-5k-coming-memory-crisis-why/)
- [GPU pricing set for reset as AI-driven memory shortages push costs higher — Astute Group](https://www.astutegroup.com/news/general/gpu-pricing-set-for-reset-as-ai-driven-memory-shortages-push-costs-sharply-higher/)
- [NVIDIA Slashes RTX 50 Series Production Amid Memory Shortage — Roic News](https://www.roic.ai/news/nvidia-slashes-rtx-50-series-gpu-production-amid-memory-shortage-and-ai-demand-shift-02-05-2026)
- [NVIDIA Prepares RTX 5090 Price Hike Amid Rising GDDR7 Costs — TechPowerUp](https://www.techpowerup.com/349050/nvidia-reportedly-prepares-rtx-5090-price-hike-amid-rising-gddr7-costs)