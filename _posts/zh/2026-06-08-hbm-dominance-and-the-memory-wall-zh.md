---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HBM主导地位与内存墙
translated: true
type: note
---

**问题：** 为什么SK海力士在AI时代如此重要？仅仅是内存容量的问题，还是另有更深层次的原因？竞争格局又是怎样的？

**回答：**

SK海力士的重要性不在于内存*容量*，而在于**内存带宽瓶颈**，并且他们是解决这一问题的全球领导者。

## 内存墙问题

在AI基础设施中，“内存墙”已成为技术进步的主要障碍，因为内存速度无法跟上处理器的发展步伐。以下是这对你工作的重要性：

当你在MI300X上训练模型时，GPU能以约192 TFLOPS的算力执行浮点运算，但从内存中提取数据的速度受限于内存接口。标准DDR5甚至GDDR6内存速度太慢——数据吞吐量成为瓶颈，而非算力。

**HBM（高带宽内存）** 通过使用硅通孔（TSV）垂直堆叠DRAM来解决此问题，可实现约1-10 TB/s的带宽。SK海力士的HBM3每堆叠可提供约460 GB/s的带宽。这对以下至关重要：

- **训练**：足够快地通过模型传输梯度和激活值
- **推理**：持续为注意力计算提供KV缓存数据（对DeepSeek v4等长上下文模型至关重要）
- **MoE路由**：混合专家模型中的专家路由需要快速内存访问，以在不同的参数集之间切换

从2024年第一季度到2025年第四季度，HBM在所有AI芯片组件支出中的占比从52%上升至63%——超过了逻辑裸片（英伟达GPU的占比从14.2%下降至12.9%）。这并非炒作；AI基础设施支出正围绕内存进行重构。

## SK海力士的竞争优势

**市场地位：** SK海力士保持着最明确的HBM领导者地位，与英伟达的整合最为紧密。他们已大规模出货HBM3，并完成了HBM4的开发，其带宽是上一代的两倍，能效提升超过40%。

**下一代创新：** SK海力士即将推出的iHBM（集成HBM5，计划2029年+发布）将冷却直接置于热量集中的Die-to-Die物理层内部，热阻降低30%。这至关重要——在1TB/s的吞吐量下，热管理已成为工程现实。

**战略合作：** 英伟达和SK海力士宣布了针对下一代内存的多年联合工程合作，该消息在数小时前刚刚公布。这标志着深层结构性协同，而非交易性供应。

## 竞争对手

**三星：** HBM4E样品已出货，但在良率、可靠性、热行为、供应量和产品路线图对齐方面仍在追赶。他们有潜力但落后于人。

**美光：** HBM领域的较小玩家。专注于消费级/DRAM；尚未成为AI内存领域的重要力量。

**真正的竞争态势：** 对于初创公司构建加速器、推理盒或专用服务器而言，内存访问、供应承诺和功耗表现可能决定产品能否以成本和规模出货。这正是英伟达与SK海力士携手的原因——没有HBM供应保障，就无法出货AI加速器。

## 这对你的意义

如果你在规模化训练模型，你已经在承担HBM的成本。MI300X的192GB HBM3并非摆设——它是实现146B参数模型所需5.3TB/s吞吐量的唯一途径。在智能体AI时代，CPU的重要性将提升，且向边缘设备的扩展很可能发生，单个AI推理服务器所需的DRAM容量将增加一倍以上。这意味着以内存为中心的架构问题正从训练GPU扩展到推理和边缘部署。

如果你正在构建需要规模化运行推理的智能体或系统，尽早理解内存瓶颈将有助于架构决策——无论是针对数据中心还是边缘部署。

---

**参考文献：**

- [SK海力士CEO在2025年SK AI峰会上关于内存中心架构的演讲](https://news.skhynix.com/sk-hynix-redefines-its-vision-at-sk-ai-summit-2025-from-ai-memory-provider-to-creator/)
- [iHBM热架构及HBM5路线图，Network World](https://www.networkworld.com/article/4177750/as-ai-datacenter-memory-becomes-hot-commodity-sk-hynix-makes-it-cooler.html)
- [HBM支出份额超越GPU逻辑裸片支出，Epoch AI数据](https://startupfortune.com/sk-hynix-shows-why-ai-investors-are-moving-into-memory/)
- [英伟达–SK海力士多年合作，2026年6月宣布](https://nvidianews.nvidia.com/news/sk-hynix-ai-factory)
- [智能体AI与DRAM需求加速，NH投资证券](https://en.sedaily.com/business/2026/06/08/nh-investment-raises-samsung-sk-hynix-targets-on-agentic-ai)
