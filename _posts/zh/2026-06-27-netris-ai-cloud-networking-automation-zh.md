---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Netris: AI云网络自动化'
translated: true
type: note
---

Question: 什么是Netris，a16z投资的这家GPU相关公司？

Answer:

我需要查一下——我对Netris这家公司的细节没有印象，而"a16z投资了"这类事实恰好需要核实。Question: 什么是Netris，a16z刚刚投资的这家GPU相关公司？

Answer:

Netris本身并不是一家GPU公司——它是**GPU云的网络自动化层**。a16z领投了1500万美元的A轮融资（2026年6月25日公布），合伙人Guido Appenzeller加入董事会。理解其技术切入角度很重要，因为这与你关心的AI基础设施栈直接相关。

## 它们实际解决的问题

当你搭建一个neocloud（以GPU优先的AI云）时，获得H100/MI300X是最简单的部分。难点在于：让数据中心为AI推理和训练做好准备可能需要数月时间——而时间越长，那些昂贵的GPU闲置的就越久。Netris自动化了网络架构配置，使运营商可以在数周内上线，而非数月。

架构上的洞察是关键。现代AI数据中心拥有**两套**网络：

1. **前端网络** —— 经典的胖树交换机结构，用于服务器↔服务器、服务器↔存储、服务器↔互联网（PCIe NIC）。
2. **后端网络** —— 第二套网络，直接连接GPU之间。这就是NVLink/InfiniBand结构。这一架构变化正是NVIDIA凭借NVLink和Infiniband等协议成为主要网络供应商的原因。

对于你的训练思维模型：当你进行分布式训练（数据/张量/流水线并行）时，all-reduce和all-to-all集合操作都运行在后端结构上。LLM的训练运行需要数千个GPU之间近乎完美的同步，即使微秒级的延迟也会严重影响性能。这就是后端网络的作用——而在数千条链路上正确配置它极其困难。

## 产品到底是什么

它被称为NAAM——网络自动化、抽象与多租户（Network Automation, Abstraction, and Multi-Tenancy）。从机制上看：Netris在网络交换机上安装代理，外加一个控制平面平台连接到这些交换机，以自动化设置、配置和运维。TechBuzz的描述是最清晰的类比——把它想象成网络层的Kubernetes：一个面向物理网络基础设施的云端控制平面，让运营商通过API而非CLI和手动配置来管理交换结构。

多租户部分对商业模式很重要：它在硬件层面隔离服务器和资源，这样neocloud可以服务于多个客户——即硬件强制的VPC，而非软件覆盖层。

## 反向的技术赌注——以及为何对你来说有趣

鉴于你倾向于AI原生的视角，这部分值得深入理解：**Netris在其产品中刻意不使用任何AI。**它依赖AI热潮之前开发的确定性算法。Saroyan的观点很犀利："AI不是确定性的……对于改变数千个交换机配置，你不需要创造力。你需要的是非常持久和可重复的操作。"

这是一个有用的反例，用来制衡你"偏爱AI原生方法"的启发式思维。网络配置是一个**确定性就是全部价值主张**的领域——在一个价值数十亿美元的集群上，一个非确定性的代理随意切换交换机配置是 liabilities（负担），而不是功能。这个教训可以推广：AI原生在探索/创造力/模糊性主导的领域胜出；确定性系统在正确性和可重复性不容妥协的领域胜出。关键在于判断你所处的是哪个领域。

传统方法为何不足：数据中心曾使用SDN（软件定义网络），但SDN之所以不足是因为它是软件——而对于AI，流量量如此之高，以至于一切都必须硬件加速。

## 为什么是a16z

这并非随意的基础设施投资——而是一次团队重聚。Appenzeller领投了这轮（前Big Switch Networks联合创始人、前VMware Cloud/Networking CTO），得到了Martin Casado和Raghu Raghuram的支持。Casado创立了Nicira——这家初创公司开创了SDN，于2012年被VMware收购——而Raghuram后来成为VMware的CEO。一句话总结其论点：Netris可能成为AI云的NSX——即像NSX为虚拟化数据中心所做的那样，为AI时代重新定义SDN。

## 市场牵引力（验证这轮融资的数据）

- 年度经常性收入（ARR）增长800%，在35+个GPU集群上运行，总计约100万块GPU。
- 此前2025年ARR同比增长622%；在这轮融资前总共融资不到600万美元。
- 客户：Lightning AI、TensorWave、富士康支持的Visionbay（台湾最大GPU集群）、Firmus（澳大利亚最大可再生能源驱动的主权AI工厂）、TELUS、HPE。
- 成立于2018年，总部位于圣克拉拉，团队分布在美国、英国、台湾、澳大利亚、亚美尼亚和印度。在亚美尼亚的业务布局有迹可循——Saroyan和创始团队具有亚美尼亚血统。

如果你愿意，我可以勾勒出后端GPU结构（rail优化的拓扑、基于RoCE/InfiniBand的NCCL集合操作）在数据包层面的实际样子——这正是Netris抽象出来的层次，并且与你基于MI300X的多节点训练直接相关。

参考文献：

- [投资Netris——a16z](https://a16z.com/announcement/investing-in-netris/)
- [Netris从a16z获得1500万美元A轮融资——TechCrunch](https://techcrunch.com/2026/06/25/netris-raises-15m-series-a-from-a16z-to-help-ai-neoclouds-go-live-faster/)
- [为什么a16z和Netris让SDN团队重聚——Futuriom](https://www.futuriom.com/articles/news/why-a16z-and-netris-are-getting-the-sdn-band-back-together/2026/06)
- [Netris获得1500万美元A轮融资——Crypto Briefing](https://cryptobriefing.com/netris-a16z-series-a-ai-networking/)