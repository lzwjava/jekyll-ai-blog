---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PingCAP IPO进展与TiDB采用情况
translated: true
type: note
---

**问题：PingCAP 融资/IPO 状态的最新进展如何？TiDB 是否有实际采用？**

**回答：**

**融资/IPO：没有新消息，没有公开的 IPO 计划。**

- 上一轮融资是 2021 年 7 月的 E 轮，由红杉中国、5Y Capital、BAI Capital、GGV Capital 和 GIC 投资。根据来源不同（Crunchbase/PitchBook 数据不一致），总融资额约在 3.35 亿至 6.42 亿美元之间——但自 2021 年以来没有新融资。
- 估值在 2021 年 7 月为 30 亿美元——此后未报告更新的估值。
- 没有 S-1 文件，没有 IPO 日期，当前搜索结果（2026 年 7 月）中未发现即将上市的传闻。EquityZen 等平台仍将其列为可供二级交易的 pre-IPO 股份，这通常意味着公司本身尚未透露 IPO 意向。
- 因此：距离上次融资已有 5 年，仍为私有状态，无 IPO 消息。如果他们已实现盈利/现金流为正，可能只是不需要融资——或者正在低调进行（对于中国创始、美国总部的公司，由于与中国相关股权结构的地缘政治敏感性，F 轮/Pre-IPO 轮次有时不会公开报道）。

**采用情况：是的，有实际生产环境使用，尽管“许多公司”是相对的。**

- 34,000+ GitHub 星标，定位为最受欢迎的开源分布式 SQL 数据库，兼容 MySQL。全球超过 1,200 名贡献者。TiKV 是 CNCF 毕业项目，这在一定程度上表明其生态系统成熟度超越了 PingCAP 自身的宣传。
- 知名生产用户：ENGIE（法国公用事业公司，业务覆盖 70+ 国家）在多个生产系统中使用 TiDB 以实现可扩展性和可靠性；Square 采用 TiDB 来扩展其不断增长的 MySQL 工作负载；Dailymotion 使用 TiDB 消除实时交易的可扩展性瓶颈，并通过 TiDB Cloud 降低基础设施成本；此外还有 EasyPost 和 Chainbase（Web3 领域，基础设施成本降低约 50%）等较小案例。
- 公司规模：根据 PitchBook/Tracxn 数据，截至 2026 年约有 500-600 名员工——不算很大，这与“通过客户而非大型风投轮次融资”的说法一致。
- 他们显然正在围绕 AI 工作负载重新定位——GitHub 描述现在写着“为不可预测增长的代理工作负载而构建，具有 ACID 保证，原生支持事务、分析和向量搜索”，并在 Microsoft Build 2026 上展示 TiDB 作为“AI 代理的分布式 SQL 数据库”。考虑到你正在构建具有高写入分支状态（ww/iclaw/zz）的代理，这种定位——代理分支共享一个带有向量搜索的 HTAP 数据库——值得认真考虑，而不是在遇到并发/扩展瓶颈时自行搭建 Postgres+pgvector 方案。

**总之：没有融资/IPO 消息，因为基本上没有——自 2021 年以来他们在股权结构方面一直保持沉默，押注于企业内生增长和云收入。实际采用是存在的，但属于第二梯队（有知名品牌标志，但不像 Postgres/MySQL 那样“人人都在用”）。**

**参考资料：**

- [PingCAP - 2025 Funding Rounds & Investors (Tracxn)](https://tracxn.com/d/companies/pingcap/__fYybWiFfmjNK0hJZgdlj0JiGtGvK9rFRupmMP7aYTis/funding-and-investors)
- [PingCAP Company Profile (PitchBook)](https://pitchbook.com/profiles/company/182210-59)
- [PingCAP Customers - Case Studies](https://www.pingcap.com/customers/)
- [pingcap/tidb - GitHub](https://github.com/pingcap/tidb)
- [About PingCAP](https://www.pingcap.com/about-us/)
