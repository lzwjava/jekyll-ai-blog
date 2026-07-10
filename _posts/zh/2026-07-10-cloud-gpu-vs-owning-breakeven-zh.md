---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 云GPU与自购：盈亏平衡？
translated: true
type: note
---

问题：一个结论：未来是远程优先的工作模式，除非公司能为每人提供3-5台机器或2-3块GPU——公司的真正优势在于有足够的资金来资助大模型训练，所以实际上只是少数资金充裕的公司与其他人竞争。否则，一家公司无法胜过那些实验跑得更快、消耗token更快的单人或小团队AI创始人。未来的工程师就像工作坊，类似于今天的工厂。云GPU是更好的解决方案吗？

回答：

你的框架在方向上是对的，但它把两种截然不同的竞争混为一谈，而正是这个区别让云GPU改变了计算方式。

**竞争1：预训练前沿模型。** 这是算力规模的战争——DeepSeek-V4、Llama、Kimi——需要数千块H100/H800/MI300X级别的芯片连续运行数周，外加数据管线团队和RLHF基础设施。没有哪个独立创始人能参与其中，无论是否用云。原因不在于$/小时的价格，而在于所需的*总*GPU小时数（10^23+ FLOPs）以及互连（NVLink/InfiniBand网络），租用的单节点Pod根本无法提供。无论云GPU变得多便宜，这一层级仍然锁定在预算1亿美元以上的实验室手中。

**竞争2：基础模型下游的一切**——微调、LoRA、在开源模型上进行RLHF/GRPO、智能体架构、RAG、部署、自定义工具使用管线、数据集工程。这才是你我实际运作的领域，在这里你的论点是对的：一个迭代速度快、没有官僚流程的独立创始人，可以比中型公司的机器学习团队做更多实验，因为瓶颈不是原始算力，而是**迭代速度**——你尝试一个想法、失败、再试下一个的速度有多快。一家拥有3-5台专用机器的公司拥有比你更多的原始算力，但如果每次运行实验都要经过工单队列、数据治理审查和经理审批，那么即使硬件更少，他们在每个想法的实际测试时间上也会输给你。

**云GPU是更好的解决方案吗？是的，而且目前的数据强烈支持这一点。**

租赁市场在2026年价格已大幅下降。目前代表性的按需H100价格：

| 提供商层级 | H100 $/小时 |
|---|---|
| RunPod Secure Cloud | $2.39–2.89 |
| RunPod Community Cloud | $1.99 |
| Vast.ai（最低价） | ~$1.49 |
| Spheron spot | $1.66 |
| Lambda / CoreWeave | $2.89–3.90+ |

直接购买一块H100需要$25,000–$30,000以上。拥有 vs 租赁的快速盈亏平衡计算：

```python
def breakeven_hours(purchase_price, rental_rate_per_hr, power_cost_per_hr=0.15):
    """在拥有成本低于租赁成本之前所需的使用小时数（忽略折旧/转售、利息、过时）。"""
    net_rental_cost = rental_rate_per_hr  # 云定价已包含电力成本
    return purchase_price / (net_rental_cost - power_cost_per_hr)

# H100 SXM购买 vs RunPod Secure Cloud租赁
hrs = breakeven_hours(27000, 2.69)
print(f"{hrs:.0f} 小时（{hrs/24:.0f} 天全天候使用）才能达到盈亏平衡")
```

以$27K购买 vs $2.69/小时租赁计算，大约需要10,600小时——**约440天连续全天候使用**——拥有硬件才能回本，而且这还没算上折旧（随着H200/B200/下一代芯片出货，H100转售价值下降很快）、电费、冷却费用、故障风险以及将资金锁定在大部分时间闲置的显卡上的机会成本。

对于你实际的工作负载模式——突发的微调任务、偶尔的预训练实验（GPT-2 760M规模、nanochat规模），而不是全天候满载——**租赁显然胜出**。你自己的AMD Dev Cloud droplet（约$2/小时）是正确的思路：按需获得MI300X级别192GB HBM3算力，只为活跃小时付费，永远不用承担折旧风险。你的RTX 4070盒子适合迭代/开发/调试（便宜、常开、不计每小时费用），而云则适合真正昂贵的训练任务。

**真正的“工作坊vs工厂”动态**不是算力所有权——而是这样：

- **工厂（资金充足的实验室）：** 拥有工厂级算力，在前沿模型预训练和基础研究上竞争
- **工作坊（你）：** 弹性租赁算力，在专业化、速度和直接客户关系上竞争——你能在一家公司的内部机器学习团队获得GPU分配审批之前，为香港的客户完成定制微调

这其实与软件领域已有的工作方式非常接近——没有人为了跑一个SaaS产品而拥有自己的AWS数据中心；你租用EC2。AI的GPU算力只是在重复同样的商品化曲线，只是落后几年。“护城河”从来不是拥有硬件——而是模型/数据/管线方面的专业知识，加上无需审批流程就行动的意愿。这正好符合你的“Tinker级别技能即护城河”论点，而且站得住脚。

有一个值得关注的注意事项：随着spot/社区价格持续下降（Vast.ai已接近$1.49/小时，有些记录显示<$1/小时），经济性更倾向于全部租赁。我仍然会考虑拥有硬件的一个领域是你的开发循环机器（4070盒子），用于便宜、常开的迭代，如果使用云计费会产生“计时焦虑”，从而在心理上拖慢你——即使不在电子表格中，这也是一个真实成本。

参考文献：

- [H100 Rental Prices Compared — IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [RunPod H100 PCIe Pricing](https://www.runpod.io/gpu-models/h100-pcie)
- [RunPod Pricing Calculator — UsagePricing](https://www.usagepricing.com/tools/pricing-calculator/runpod)
- [H100 Cloud Pricing Comparison — getdeploying.com](https://getdeploying.com/gpus/nvidia-h100)