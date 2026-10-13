---
audio: false
generated: true
image: false
lang: zh
layout: post
title: XTX Markets：AI驱动的量化交易
translated: true
type: note
---

## 问题：英国公司 XTX Markets 是做什么的？

**答案：XTX Markets 是一家总部位于伦敦的 quantitative trading 公司，利用 machine learning、数学和大量计算基础设施在金融市场中赚钱。**

可以把它看作一家 AI 公司，其产品是金融交易，而不是向客户销售 AI 软件。

其官方网站是 [xtxmarkets.com](https://www.xtxmarkets.com/)。[XTX Markets](https://about.xtxmarkets.com/?utm_source=chatgpt.com)

### 1. XTX Markets 到底做什么？

XTX 的主要业务分为三个领域。

**A. Algorithmic trading**

它使用数学模型和 machine learning 来预测价格并在金融市场中执行交易。

其市场包括：
- 外汇（FX）。
- 股票和 ETFs。
- 债券和其他固定收益工具。
- 大宗商品。
- 加密货币市场。

根据其官方网站，XTX 为超过 53,000 种金融工具生成价格预测。[XTX Markets](https://www.xtxmarkets.com/?utm_source=chatgpt.com)

**B. 向金融机构提供流动性**

这是其业务中特别重要的一部分。

想象一家银行想将 1000 万欧元兑换成美元。

银行需要一个愿意以有竞争力的价格进行交易的对手方。

XTX 可以报价并执行交易，从买卖价差中赚钱，同时管理其头寸风险。

它向包括银行和经纪商在内的机构客户提供流动性。其业务主要不是向零售投资者销售交易软件。[XTX Markets](https://about.xtxmarkets.com/clients/?utm_source=chatgpt.com)

**C. 利用 AI 获得交易优势**

XTX 使用 machine learning 来估计金融工具的公允价值并识别交易机会。

例如，假设其模型估计某货币对应该交易在 1.1002，而市场价格为 1.1000。

这一差异可能代表潜在机会。然而，在交易具有经济意义之前，模型必须考虑交易成本、市场波动、执行质量和风险。

在规模化条件下，即使微小的优势也可能变得有价值。

核心思想是：

\\[
\text{Profit} \approx \text{Trading volume}
\times \text{Net edge per trade}
\\]

这是一个近似式，而不是完整的会计恒等式。实际盈利能力还取决于库存风险、对冲、运营成本和亏损。

### 2. 为什么 XTX 从 AI 工程角度来看很有意思？

XTX 之所以特别有意思，是因为其业务直接将 machine learning 和计算基础设施变现。

其官方网站报告了以下数据：

| 指标 | 报告数值 |
|---|---:|
| 覆盖的金融工具 | 53,000+ |
| 每日交易量 | $250 billion |
| GPU 研究集群 | 25,000+ GPUs |
| 可用存储 | 超过 1 exabyte |
| 员工 | 约 300 人 |

这些是 XTX 自己发布的数据，并非独立核实的测量结果。[XTX Markets](https://about.xtxmarkets.com/?utm_source=chatgpt.com)

考虑这些数据背后的工程含义。

**1. 大规模 data pipelines**

公司需要处理市场价格、订单簿信息、历史数据和其他信号。

**2. Machine learning 研究**

研究人员构建从金融数据中提取预测信号的模型。

**3. High-performance computing**

公司需要大量计算资源用于研究、模型训练、实验以及潜在的 inference workloads。

**4. Low-latency systems**

一旦模型识别出机会，交易基础设施必须高效地执行订单。在竞争激烈的市场中，毫秒可能至关重要。

**5. Production reliability**

一个在实验中表现良好但在真实市场条件下失败的模型是没有用的。数据质量、风险管理、执行和监控至关重要。

对于对 LLM 基础设施、GPU 集群和 AI 系统感兴趣的人来说，XTX 是一个有趣的例子，它展示了先进计算与收入直接关联的公司形态。

然而，其核心 machine learning 专注于金融预测和交易，不一定是 large language models。

### 3. 与 AI 咨询公司相比，XTX 如何赚钱？

两者的商业模式根本不同。

| 维度 | XTX Markets | AI 咨询公司 |
|---|---|---|
| 产品 | 交易和流动性 | 软件和 AI 解决方案 |
| 客户 | 银行、经纪商和机构市场参与者 | 需要技术解决方案的企业 |
| 主要优势 | 预测模型、执行、数据和基础设施 | 工程能力、领域知识和交付能力 |
| 收入来源 | 交易利润和做市业务 | 项目费、顾问费和软件合同 |
| 可扩展性 | 可以在不按比例增加员工的情况下增加交易活动 | 随着项目增长，通常需要增加工程师 |
| 主要风险 | 市场亏损、模型性能下降、执行和监管 | 客户获取、交付成本和竞争 |

AI 咨询公司通常通过帮助客户解决问题来赚钱。

XTX 利用 AI 和计算在金融市场中直接竞争。

**重要区别在于，XTX 是将自身技术优势变现，而不是主要出售工程劳动力。**

在设计 AI 业务时，这个区别值得理解。

### 4. XTX 是一家合法的英国公司吗？

是的。英国政府的 Companies House 注册名录将 XTX Markets Limited 列为在营私人有限公司，成立于 2015 年 1 月 30 日。其注册业务分类为自营证券交易。[Find and Update Company Information](https://find-and-update.company-information.service.gov.uk/company/09415174?utm_source=chatgpt.com)

一个重要警告：XTX 明确表示，它不接受个人零售投资者的存款，也不向个人零售投资者提供交易服务，并且不发行加密货币。声称提供 XTX 品牌零售交易或加密产品的网站与该公司无关。[XTX Markets](https://about.xtxmarkets.com/news/notice-regarding-retail-cryptocurrency-scams/?utm_source=chatgpt.com)

公司官方信息：[Companies House — XTX Markets Limited](https://find-and-update.company-information.service.gov.uk/company/09415174)。

---

### 5. 我的看法：为什么你应该关注 XTX

鉴于你对 AI 基础设施、GPU 计算和建立 AI 公司的兴趣，我会研究 XTX，原因只有一个。

**它展示了一个组织的软件能创造可衡量的经济价值时，一个相对较小的技术组织如何能以巨大规模运作。**

传统的软件服务公司可能需要数百名工程师才能产生可观的收入。

而 quantitative trading 公司可以大力投资于研究人员、计算、数据和交易系统，然后将由此产生的优势在巨大的交易量中变现。

但有一个问题：这种模式需要难以复制的组合——金融专业知识、专有数据、研究人才、执行基础设施和风险管理。

你无法仅通过租用 GPU 和训练模型来复制 XTX 的经济效益。

对于你自己的公司，更实际的教训可能是从出售工程服务逐步转向构建客户愿意付费使用的可复用 AI 系统。

例如：

1. 从面向付费客户的 AI agent 和软件项目开始。
2. 识别多个客户之间的重复性问题。
3. 构建可复用的 agents、工具和基础设施。
4. 将最有价值的组件转化为产品或按使用量计费的服务。
5. 让软件（而不是单纯的人员数量）推动收入增长。

这与 quantitative trading 是不同的业务，但它应用了类似的原理：**利用技术能力创造一种超越你个人工作小时数的可扩展优势。**

### 参考文献
- [XTX Markets — 官方网站](https://www.xtxmarkets.com/)
- [XTX Markets — 技术与公司概览](https://about.xtxmarkets.com/)
- [XTX Markets — 机构客户与流动性服务](https://about.xtxmarkets.com/clients/)
- [英国 Companies House — XTX Markets Limited](https://find-and-update.company-information.service.gov.uk/company/09415174)