---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 产品驱动的规模化胜过服务驱动的
translated: true
type: note
---

**问题：** 与Tata（TCS）和Infosys等传统IT服务公司相比，ByteDance是否拥有根本上更好的扩展模式？

**回答：**

是的，而且这种差异是结构性的——这是典型的**产品主导 vs. 服务主导**的扩展分水岭。

**ByteDance的扩展模式：**

ByteDance的秘密武器是它的“Shared Services Platform”（SSP），其中包括算法和技术人员（工程师、分析师），他们跨多个产品工作，而不是被隔离在单一产品线中。这使产品团队在利用共享基础设施的同时保持精简。

在SSP的推动下，ByteDance同时进行广泛探索（2年内推出140+个应用）、快速迭代（快速发布，淘汰表现不佳者）和选择性聚焦。

其数据驱动文化意味着一个洞察可以催生多个突破——例如，Toutiao上视频观看量的激增直接促成了Douyin的开发，并最终催生了TikTok。

在基础设施层面，ByteDance的HeteroScale系统在超过10,000个GPU的集群上以工业级规模运行LLM，每天处理数万亿的prefill tokens和数千亿的decode tokens——这种工程能力进一步放大了其优势。

**TCS/Infosys的扩展模式：**

像Infosys和TCS这样的IT服务公司通常部分根据项目部署的人数向客户收费。GenAI现在已经使得用更少的人处理IT项目成为可能，迫使他们转向与结果而非成本挂钩的基于价值的定价。

服务公司出售的是人力——其收入随员工人数*线性*增长。项目越多意味着招聘越多。利润率较低，难以差异化，并且可扩展性有限，因为他们无法轻易自动化咨询或定制软件。

**数据说明问题：**

TCS的每名员工收入约为49,902美元，Infosys为60,164美元。这些数字增长缓慢——与FY22相比仅为4–5%。相比之下，产品工程公司即使在动荡的市场中也经常实现9–11%的增长率。而ByteDance/Big Tech产品公司每名员工创造的收入比这高出几个数量级。

**核心不对称性：**

产品公司可以实现价值交付自动化——一旦建成，产品就能以最小增量成本服务数百万人。这就是为什么它们能获得高估值倍数：投资者押注指数级增长。服务公司是算术级增长；产品公司是几何级增长。

所以是的——ByteDance的模式从根本上更具可扩展性，因为其收入与员工人数脱钩，由算法和共享技术基础设施驱动。TCS和Infosys多年来一直知道这一点，并正在争相转型，但从劳动力套利模式转向软件/产品模式是一个非常艰难的过程。

---

**参考资料：**
- [ByteDance如何征服世界 – The Hustle](https://thehustle.co/03152022-bytedance)
- [Import AI: ByteDance的HeteroScale](https://bedwards.github.io/hex-index/article/0480c54d-a5b5-4d61-a27a-00479aab02b0/index.html)
- [生产力差距：印度IT公司 vs 全球科技](https://www.indiabusinesstrade.in/?p=5348)
- [产品 vs 服务商业模式](https://lzwjava.github.io/product-vs-service-en)
- [GenAI改写印度IT转型 – Mint](https://www.magzter.com/de/stories/newspaper/Mint-Hyderabad/GENAI-RECODES-INDIAN-IT-SHIFT)