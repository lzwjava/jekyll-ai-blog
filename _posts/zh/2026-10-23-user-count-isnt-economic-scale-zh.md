---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用户数不等于经济规模
translated: true
type: note
---

问题：在大型公司中，内部工具和平台不对外营销，这意味着它们只有数千名用户——那么它们的经济规模本质上不是很小吗？

答案：这是一种常见的直觉，但在企业环境中，**用户数量 ≠ 经济规模**。原因如下：

| 指标 | 消费者应用 | 内部平台 |
| --- | --- | --- |
| 规模信号 | MAU / DAU | 节省的小时数 × 员工人数 × 薪资 |
| 收入模式 | 直接货币化 | 生产力提升/错误减少 |
| 用户数量 | 数百万 | 数千 |
| 每用户价值 | 低（约～美元/月） | 非常高（约每年1万-10万+美元） |

如果一个内部工具每周为每位工程师节省2小时，而公司有10,000名工程师，年薪20万美元，那么这大致相当于每年**～2亿美元的生产力恢复**——而这还是来自“仅数千名用户”。

**其他比用户数量更重要的扩展因素：**

- **流程关键性** — 一个内部CI/CD平台、数据管道或风险系统可以控制*数十亿*美元的业务运营。停机时间 = 直接收入损失。
- **对核心业务的影响力** — Amazon的内部物流工具、Google的Borg（集群调度器）或Goldman Sachs的交易基础设施不需要数百万用户来证明巨大投资的合理性。
- **构建成本随时间摊销** — 一旦构建，一个拥有10,000用户的内部平台可以运行十年，使其ROI不断累积。
- **切换成本** — 内部平台通常变得如此根深蒂固，以至于替换它们的成本高于最初构建的成本。

**你*确实*对的地方：**

- 小用户基数*确实*会带来实际的问题：
  - 更难证明专门团队的规模合理性
  - 反馈循环更慢且多样性更少
  - 没有网络效应
  - 功能被削减，因为“这是内部的，足够好了”

这种张力正是为什么许多公司最终将其内部工具**开源或商业化**（例如：Google → Kubernetes, Facebook → React, Netflix → 各种开源项目）——正是为了摆脱你所描述的经济陷阱。

参考资料：

- [为什么大型科技公司构建内部工具（以及为什么这很重要）](https://medium.com/swlh/why-big-tech-companies-build-internal-tools-and-why-it-matters-2e3d2b9bf2e3)
- [内部开发者平台的经济学——Thoughtworks](https://www.thoughtworks.com/insights/blog/platform-engineering/economics-of-internal-developer-platforms)
- [从内部工具到开源：Google Kubernetes的故事](https://kubernetes.io/blog/2018/07/20/the-history-of-kubernetes-the-community-behind-it/)
