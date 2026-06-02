---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 争议性云网络观点
translated: true
type: note
---

问题：关于云网络有哪些不受欢迎的观点？

答案：

云网络——包括VPC、Transit Gateway、混合/多云连接、SD-WAN集成和特定提供商的架构——引发了激烈的辩论。以下是一些源于专业讨论和经验的非主流或有争议的观点：

- **对于稳定工作负载，公有云通常比本地部署更昂贵且性能更差**：尽管有关于可扩展性的宣传，许多人认为可预测的工作负载在没有虚拟化开销、“吵闹的邻居”或出口费用影响的专用硬件上运行更便宜、更快。

- **多云策略被过分吹捧，很少值得其复杂性**：避免供应商锁定听起来很理想，但实际上，它增加了运营开销、集成挑战、工具不一致和成本，而对于大多数组织来说，并没有带来相应的收益。

- **混合云是一种暂时的妥协，而非长期战略**：真正的云原生设计应该完全拥抱公有云；保留本地基础设施将组织束缚于遗留限制，并阻碍全面的敏捷性。

- **AWS网络过于复杂和受限**：与GCP或Azure中更简单的设计相比，诸如有限的静态IP、安全组的复杂性以及传输路由限制等功能令用户感到沮丧。

- **Transit Gateway是不必要的开销；VPC peering足以满足大多数规模需求**：虽然它被宣传用于复杂的枢纽，但在许多实际设置中，直接peering更简单，数据传输成本更低，并避免了额外的连接成本。

- **云环境中的SD-WAN通常是多余的**：原生云连接（Direct Connect、ExpressRoute）和提供商骨干网提供了足够的性能和QoS，而无需第三方SD-WAN设备增加延迟或管理负担。

- **云网络安全模型（例如，没有传统边界）对于企业来说存在缺陷**：零信任假设在理论上可行，但与本地分段网络相比，它使合规性、可见性和东西向流量检查复杂化。

这些观点挑战了全面采用云和复杂互连的主流趋势，其根源通常在于意料之外的成本、运营实际情况以及性能权衡。

参考资料：

- <https://dev.to/aws-builders/cloud-outages-the-unpopular-truth-no-one-wants-to-hear-4enl>
- <https://www.reddit.com/r/sysadmin/comments/16ydav5/am_i_the_only_one_who_kinda_hates_the_cloud/>
- <https://www.cloudflare.com/learning/cloud/multicloud-vs-hybrid-cloud/>
- <https://www.infoworld.com/article/2270528/why-traditional-ip-networking-is-wrong-for-the-cloud.html>
- <https://cloudviz.io/blog/aws-vpc-peering-vs-transit-gateway>
- <https://www.reddit.com/r/aws/comments/ynrm9k/transit_gateway_or_vpc_peering_for_crossregion/>
- <https://blog.ipspace.net/2020/11/why-public-cloud-networking-so-different/>
- <https://www.networkcomputing.com/cloud-networking/cloud-connectivity-methods-and-myths>
