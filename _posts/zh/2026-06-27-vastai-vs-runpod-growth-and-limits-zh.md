---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Vast.ai与RunPod：增长与局限
translated: true
type: note
---

Question: Vast.ai 正在如何增长，它会扩大10倍吗，它的局限性是什么——尤其是与 RunPod 相比？

回答:

让我获取当前数据。在进入正题前先快速说明：大部分搜索结果都是关于 **VAST Data**（由 Renen Hallak 创立的市值300亿美元的AI存储公司）——这与你想了解的 GPU 租赁市场平台 **Vast.ai** 是完全不同的公司。名字容易混淆，但数据完全不同。让我更精确地获取实际 Vast.ai 的数据。现在我已经掌握了真实的 Vast.ai 情况。它与 RunPod 的对比清晰且具有结构性差异。

## Vast.ai 实际上是什么

Vast.ai 是一个 **纯粹的 peer-to-peer GPU 市场**——这是轻资产模式最极端的版本。该公司本身不建造也不拥有数据中心。每一块 GPU 都属于独立的主机——可能是拥有闲置 RTX 3090 的游戏玩家、转型工作负载的加密货币矿场，或是将闲置机架空间变现的托管设施。Vast 运营市场软件、处理支付、执行租赁合约，并维护 SOC2 Type II 认证。可以把它看作 GPU 算力的 Airbnb/eBay，而 RunPod 则更接近于托管云并附带一个社区层。

当前规模：17,000+ 块 GPU，跨越 1,400+ 个提供商，分布在全球 500+ 个地点——2026 年最大的去中心化 GPU 市场。服务 200,000 日活跃用户，覆盖 40+ 个数据中心地点。成立于 2018 年，约 46 名员工，总部位于洛杉矶。

## 增长与 10 倍问题

这里是与 RunPod 的关键区别：**融资和收入透明度。** RunPod 刚刚以 10 亿美元估值融资 1 亿美元，并公开 ARR。Vast.ai 仅融资约 400 万美元（来自 DRW Holdings、Nazare、Primavera Venture Partners），拥有 46 名员工，且不披露收入。这是一个刻意精益、资本高效的赌注——而非风险投资火箭船。

市场顺风是真实存在的，并且两者共享：AI GPU 租赁市场在 2026 年达到 73.8 亿美元，预计 2027 年将增长约 28.73%。所以整个*类别*在未来十年将轻松实现 10 倍增长。问题在于 Vast.ai 能否抓住这一机会。

**实现 10 倍增长的理由：** 其结构性地位独一无二——它是价格地板。SaladCloud 和 Vast.ai 设定了消费级显卡每小时定价的地板。市场平台通常提供比主要公有云低 50-80% 的费率。只要存在长尾的闲置 GPU（矿工、专业消费者、小型托管商）和价格敏感的需求（微调、批处理作业、独立研究人员——也就是*你*），市场就会随着供应增长而机械地增长。

**代理角度是最有趣的增长向量**，并且与你的方向直接相关。Vast.ai 正在明确围绕 AI 代理自主获取算力进行重新定位：“Vast.ai 上的每一块 GPU 都通过代码配置。开发者用来在数秒内部署的同一 API，也是代理用来大规模获取和优化算力的接口。”Crunchbase 自身的描述：“Vast 是 AI 代理自主设计、获取和优化其算力的基础设施层……是以高频匹配全球供需的市场层。”如果代理工作负载成为算力的主要消费者，那么一个可查询、可编程的现货市场正是正确的原语。这是一个真正的 10 倍论点——不是“更便宜地租用 GPU”，而是“成为代理交易算力的交易所”。

## 局限性——这些比 RunPod 更为尖锐

1. **可靠性因主机而异，而非平台整体——存在“可靠性税”。** H100 标价约 $0.90/小时（市场上最低），但实际成本在未经验证的主机上会因停机重启而高出 20-40%。如果你需要可预测的成本，请预算比最低标价高 30-50% 的费用。具有冗余电源和 99.5% 正常运行时间的主机是可靠的；而单人矿工的游戏机则不然。平台提供了区分它们的工具，但可靠性需要你自己管理。

2. **缺乏托管云原语。** Vast.ai 缺乏内置的自动扩展、监控和正常运行时间保证。对于生产环境，你必须限制在已验证的数据中心主机，并自行实施外部监控、健康检查和自动故障转移。RunPod 提供了无服务器、低于 500ms 的冷启动和持久化存储。Vast 则给你一个放在别人机器上的原始 Docker 容器。

3. **合规天花板。** SOC2 认证覆盖平台，而非个别主机。需要 HIPAA 或 FedRAMP 的受监管医疗、金融和政府工作负载无法依赖市场模式。这限制了驱动 RunPod 2.4 亿美元 ARR 的高利润企业收入。它在结构上限制了 Vast 能向高端市场走多远。

4. **本质上的无状态。** 任何需要持久块存储、可预测 IP 或托管数据库集成的工作负载都应另寻他处。

5. **供给紧张时的双刃剑。** 当供给紧张时，Vast 的长尾聚合是金子。Vast.ai 记录到高端硬件价格大幅上涨——Blackwell B200 从 $3.81 涨到 $7.50——并正式从目录中移除过时的架构（V100 16GB、A40、RTX A6000）。如果供给紧张缓解，市场利润压缩最为严重，因为没有自有基础设施或签约的企业客户群来缓冲。

## 我对你的具体解读

**这两家公司是对同一市场的不同赌注。** RunPod 在价值阶梯上攀升（托管开发体验、无服务器、企业级、生态锁定）——它试图成为基础设施。Vast.ai 则加倍押注于成为**成本最低、最具可编程性的现货交易所**，并赌注代理将成为买家。RunPod 更可能是传统的 10 倍赢家，因为它拥有资金、企业收入和产品表面。Vast.ai 的 10 倍则方差更大：如果代理式算力获取的论点成立，它会大赢；如果不成立，则仍是一个利基的价格地板工具。

对于你的实际工作流：Vast.ai 正是你所运行任务的正确工具——微调预训练模型、有界限时间且可以设置检查点的运行，以及不需要 InfiniBand 多节点网络的任务。在单个 H100 上以 $1.47/小时进行微调，其成本等同于在 CoreWeave 上以 $6.16/小时运行 42 分钟。你的 nanoGPT/nanochat 规模的实验、LoRA 运行、批量评估任务——固定在已验证的主机上，积极将检查点存储到外部存储，你就能在消费级显卡上低于 AMD Dev Cloud 实例（$2/小时）。当你想要无服务器推理或零运维时，使用 RunPod；当你想要最原始的廉价 GPU 小时并愿意自己承担可靠性时，使用 Vast。鉴于你已经开始编写所有脚本，API 优先的市场模式正符合你的优势——你可以编写一行代码，根据可靠性评分和价格进行过滤，然后抓取满足阈值的最便宜机器。

参考：

- [Vast.ai Review 2026: Pricing, Reliability & Alternatives — GPUnex](https://www.gpunex.com/blog/vast-ai-review-2026/)
- [Vast.ai Review: GPU Rental Prices and Real Tradeoffs 2026 — AI Tool Discovery](https://www.aitooldiscovery.com/ai-infra/vast-ai-review)
- [5 Best GPU Rental Marketplaces for AI — Fluence](https://www.fluence.network/blog/best-gpu-rental-marketplaces/)
- [AI GPU Rental Market Trends June 2026 — Thunder Compute](https://www.thundercompute.com/blog/ai-gpu-rental-market-trends)
- [GPU Marketplaces in 2026 — Spheron](https://www.spheron.network/blog/top-gpu-rental/)
- [Vast.ai company profile — PitchBook](https://pitchbook.com/profiles/company/531153-01)
- [Rent GPUs — Vast.ai](https://vast.ai/)