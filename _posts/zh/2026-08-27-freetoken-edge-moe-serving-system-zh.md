---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'FreeToken: 边缘MoE服务系统'
translated: true
type: note
---

**问题：** 这个arXiv链接上的论文是什么？

**回答：**

这是一篇研究论文，标题为 **FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution**，于2026年8月17日发表在arXiv上，作者来自UC Berkeley（包括Ion Stoica、Matei Zaharia和Song Han等人）。

**内容简介：**

FreeToken是一个面向Mixture-of-Experts（MoE）大语言模型的边缘原生服务系统。它没有将个人机器仅仅视为“小GPU”，而是将其视为一个统一、弹性的推理平台。

**它解决的核心问题：**

前沿的开放权重AI模型越来越普及，但运行它们仍然在很大程度上假设了数据中心规模的基础设施。FreeToken将这种能力带到了个人硬件上。

**关键技术贡献：**

FreeToken围绕本地AI的两个关键现实，共同设计了完整的服务栈——涵盖模型布局与加载、专家驻留、CPU-GPU执行、代理状态复用以及运行时内存管理：代理工作负载会持续改变其执行模式，并且边缘硬件暴露了因机器而异的异构资源。FreeToken没有采用固定的卸载策略，而是动态地将计算映射到实际可用的任何资源上。

**令人印象深刻的结果：**

它支持超过20个MoE模型以及真实的编码/工具使用代理，硬件范围从8GB笔记本电脑GPU到单个工作站GPU——使得35B模型能在笔记本电脑上运行，284B模型能在游戏台式机上运行，甚至753B的GLM-5.2也能在单个工作站GPU上运行。

该系统已在 **flashml.ai** 公开发布。

---

**参考资料：**

- [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](https://arxiv.org/abs/2608.16157)
