---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod上A100 GPU租赁收益
translated: true
type: note
---

**问题：** 如果我拥有一块A100 GPU并在RunPod上出租，能赚多少钱？

**答案：**

首先需要澄清一个重要问题：**RunPod的Community Cloud**（独立主机商列出其GPU的地方）主要面向消费级游戏显卡，如RTX 3090/4090。在RunPod上托管数据中心级A100并不那么简单——通常需要你成为经过审核的数据中心合作伙伴，加入Secure Cloud层级，而非个人主机商。即便如此，以下是完整情况：

**租户在RunPod上为A100支付的价格（需求侧）：**

RunPod的Secure Cloud定价显示，A100 PCIe为1.39美元/小时，A100 SXM为1.49美元/小时。这是租户支付的价格——作为主机商，你将在RunPod抽成后获得其中一部分。

**粗略收入估算（如果你能将其列出来）：**

| 场景 | 费率 | 每月小时数 | 总收入 |
| --- | --- | --- | --- |
| A100 PCIe，50%利用率 | ~1.39美元/小时 | ~360小时 | ~500美元/月 |
| A100 PCIe，80%利用率 | ~1.39美元/小时 | ~576小时 | ~800美元/月 |
| A100 PCIe，100%利用率 | ~1.39美元/小时 | ~720小时 | ~1,000美元/月 |

这是**扣除**RunPod平台费用和你的电费之前的毛收入。

**关键要点：**

- 持续计算会使显卡运行温度更高、时间更长，增加磨损（主要是风扇），并略微缩短寿命。良好的气流和将GPU功耗限制在约80–90%可以降低热量和电费，同时收入损失极小。
- 电费是实际成本——一块显卡在负载下会消耗大量功率，按0.15美元/千瓦时计算，高端GPU满负荷24/7运行每月电费大约为40–50美元。在电价高的地区，电费可能吞噬大部分利润。
- RunPod使用2–3级数据中心，与超大规模基础设施相比，以牺牲一定可靠性换取较低成本。
- 对于数据中心级A100，**Vast.ai**可能是一个更好的市场，因为它是一个更开放的点对点平台，主机商可以直接在定价上竞争。

**总结：** 如果充分利用，RunPod上的A100每月毛收入大约为**800–1,000美元**，但扣除电费、平台费用和利用率波动后，实际净收入可能会低得多——在良好条件下可能为**500–750美元/月**。实际利用率完全取决于市场需求。

**参考：**

- [RunPod Pricing 2026 (UsagePricing)](https://www.usagepricing.com/tools/pricing-calculator/runpod)
- [How to Make Money Renting Out Your GPU in 2026 (EarnifyHub)](https://earnifyhub.com/learning-guides/make-money-renting-out-gpu-2026)
- [H100 Rental Prices Compared (IntuitionLabs)](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
