---
audio: false
generated: true
image: false
lang: zh
layout: post
title: xAI内部结构之苏莱曼·戈里
translated: true
type: note
---

问题：Sulaiman Ghori 对 xAI/Grok 内部如何运作有何说法？

答案：Ghori 曾是 xAI 的技术团队成员（2025年3月至2026年1月），负责 Grok 与 X 平台的集成。随后他在 *Relentless* 播客中接受了一次广泛传播的采访，详细透露了 xAI 的内部情况——据称因披露专有信息，他因此被解雇。以下是该采访中涉及的关键技术/运营主张：

**速度优先于流程**
xAI 将速度置于首位，并利用其硬件基础设施实现每日模型迭代，打破了传统时间表。模型迭代每天发生，有时甚至一天多次——从预训练阶段开始，硬件机架在数小时内即可开始训练，而其他公司则需要数天或数周。

**马斯克亲自扫清瓶颈**
马斯克亲力亲为，迅速解决瓶颈问题，例如连夜部署补丁以在新硬件上运行模型。他被描述为擅长提前数月乃至数年预测瓶颈，并据此反向推进工作；团队也效仿这种做法，聚焦核心财务/物理指标。

**Colossus / 基础设施才是真正的护城河**
Colossus 数据中心——Grok 训练所用的集群——在 122 天内建成，Ghori 认为这才是 xAI 相比其他实验室的真正优势，而不仅仅是算法。

**消除人为软件开销**
xAI 通过消除人为开销并专注于物理极限（即把延迟/吞吐量视为物理问题而非配置问题），将软件性能提升了 2 到 8 倍。

**文化：无固定角色，自下而上**
他的入职体验：拿到一台笔记本电脑和一张工牌，但没有具体指示或团队分配；最初几天他自行寻找项目帮忙，最终参与了 Grok 与 X 平台的集成。公司重视能够找到简单解决方案并挑战需求的工程师，培育了一种自下而上的文化，好的想法能迅速落地。

**超越聊天机器人的路线图**
xAI 正在开发“MacroHard”，一个人类模拟器，并探索利用特斯拉车载电脑进行部署——即利用汽车中闲置的 FSD 芯片算力作为分布式推理/训练网络，而非建设更多数据中心，最终目标是通过分布式特斯拉芯片模拟数百万人类。

以上内容均未涉及架构层面的细节（无注意力机制变体、MoE 配置、上下文长度内部信息）——主要涉及组织/基础设施/文化，这与导致他被解雇（而非泄露技术规格）的原因相符。

参考资料：
- [WTF is happening at xAI — Sulaiman Ghori, Relentless (Podwise)](https://podwise.ai/dashboard/episodes/6885430)
- [Podcast Notes: WTF is happening at xAI](https://www.podchemy.com/notes/wtf-is-happening-at-xai-sulaiman-ghori-48474640483)
- [Inside xAI's Culture of Relentless Speed and Hardware Leverage — StartupHub.ai](https://www.startuphub.ai/ai-news/ai-video/2026/inside-xais-culture-of-relentless-speed-and-hardware-leverage)
- [Inside xAI and Future of Millions of Emulated Humans — NextBigFuture](https://www.nextbigfuture.com/2026/01/inside-xai-and-future-of-millions-of-emulated-humans.html)
- [Sulaiman Khan Ghori — Grokipedia](https://grokipedia.com/page/Sulaiman_Khan_Ghori)