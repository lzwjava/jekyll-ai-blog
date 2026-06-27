---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod 的增长、风险与10倍潜力
translated: true
type: note
---

问题：RunPod 的发展状况如何？它能实现10倍增长吗？其局限性又是什么？

答案：

让我先查找当前数据再回答。以下是截至2026年6月底的情况。

## 增长轨迹

数据确实惊人。RunPod的年化经常性收入（ARR）达到约2.4亿美元，相比2026年1月的1.2亿美元翻了一番——大约五个月内实现翻倍。开发者数量从2024年5月的10万人增长至2026年1月的超过50万人，目前已经突破100万开发者。在达到1.2亿美元ARR里程碑时，注册量同比增长了155%。

在融资方面：RunPod以10亿美元估值融资1亿美元——较2024年种子轮估值增长十倍——并拒绝了超过5亿美元的收购要约以保持独立。值得注意的是，其资本效率极高——从自筹资金起家（创始人地下室中改造的以太坊挖矿GPU，以及Reddit上的测试版帖子）发展到2.4亿美元ARR，仅依靠相对较少的风险投资。

## 它能实现10倍增长吗？

从当前水平增长10倍意味着约24亿美元的ARR。有可能，但并非必然。支持这一观点的理由如下：

**利好因素。** 据某些估计，2026年的人工智能计算资源短缺比2023年的芯片危机更为严重。开发者难以获取足够的GPU，这催生了一批新型公司，它们购买芯片并对外出租。RunPod直接受益于这一趋势。

**差异化优势。** 大多数新型云服务商将业务局限于推理。RunPod更侧重于广度——在单一平台上提供完整周期（实验、训练、微调、规模化），同时还支持AMD芯片，后者可能更便宜且更容易获取。这一AMD策略对你尤其重要，因为你涉及MI300X方面的工作——RunPod是少数将AMD视为一级合作伙伴的新型云服务商之一。

**用户留存。** 从注册到首次工作负载运行的中位时间不到一小时，首次部署成功率超过90%，85%的部署者会再次使用。报告显示净美元留存率约为120%。强劲的留存率加上仍在快速扩张的市场，是典型的10倍增长公式。

## 局限性与风险

这才是问题的关键：

1.  **轻资产模式 = 供应端护城河薄弱。** RunPod采用轻资产模式——租赁容量而非自有数据中心。这有利于资本效率，但也意味着它无法控制自身供应。其社区云服务聚合自经过审核的主机。如果GPU供应进一步收紧，它将与所有其他公司争夺相同的芯片，而没有CoreWeave那样的自有基础设施。

2.  **资金更充裕的竞争对手。** 风险包括来自CoreWeave和Lambda等竞争对手，以及超大规模云服务商（AWS、GCP、Azure）的竞争。CoreWeave拥有自有数据中心，资本规模是RunPod的数倍。RunPod的1亿美元融资轮与CoreWeave的数百亿美元相比显得微不足道。

3.  **利润率压缩。** 随着GPU价格下跌，以及各提供商在冷启动时间和扩展效率上展开竞争，无服务器计算领域面临利润率压缩。商品化计算服务是一场价格战。

4.  **算力短缺可能缓解。** 如果GPU算力短缺缓解，定价权可能会减弱。目前的大部分收入可以说源于稀缺性溢价。如果英伟达/AMD的供应跟上需求，有利的定价窗口将会收窄。

## 我的看法

10倍增长的问题归结为一点：**RunPod能否在计算资源商品化之前更快地提升价值链？** 纯粹的GPU租赁业务是一场逐底竞争。其可防御的赌注在于开发者体验层——RunPod Hub市场（提供高达7%的收入分成）、与Cursor和Claude Desktop的MCP集成、以及可在几分钟内配置16-64块H100 GPU的即时集群。如果这一生态系统层变得具有粘性（开发者在RunPod*上*构建，而不仅仅是*从它那里*租赁资源），那么10倍增长是可能的。如果它仍然只是一个薄弱的转销商，那么随着算力短缺缓解，其增长空间将受限。

对你个人使用而言：他们对AMD的支持以及按秒计费的无服务器模式，使其非常适合你的MI300X实验和突发训练任务——比自购更便宜，且无需签合同。在应对突发的计算密集型工作负载时，值得将其视为AMD Dev Cloud实例的一个严肃替代方案。

参考文献：

- [Runpod reaches $1B valuation with $100M funding — DigitrendZ](https://digitrendz.blog/digital-marketing/209051/runpod-reaches-1b-valuation-with-100m-funding/)
- [RunPod revenue, funding & news — Sacra](https://sacra.com/c/runpod/)
- [Runpod AI Cloud Surpasses $120M in ARR — RunPod press](https://www.runpod.io/press/runpod-ai-cloud-surpasses-120m-in-arr)
- [Runpod Raises $100M at $1B Valuation, Rejects $500M Buyout — KuCoin](https://www.kucoin.com/news/flash/runpod-raises-100m-at-1b-valuation-rejects-500m-buyout-offers)
- [Runpod Raises $100M Led by Summit Partners — Morningstar/PR Newswire](https://www.morningstar.com/news/pr-newswire/20260624la90924/runpod-raises-100m-led-by-summit-partners-to-accelerate-the-ai-developer-cloud)