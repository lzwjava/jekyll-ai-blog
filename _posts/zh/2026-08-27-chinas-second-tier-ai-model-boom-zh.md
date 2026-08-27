---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国第二梯队AI模型热潮
translated: true
type: note
---

**问题：** 像微博和蚂蚁集团（及其Ling模型）这样的“二线”中国公司是否正在加入AI模型竞赛——尽管阿里巴巴已经有了Qwen？

**回答：**

你说得很对——这确实是一个百花齐放的时代。微博和蚂蚁集团都已深度参与其中，并且独立于Qwen运作。

**微博——VibeThinker系列**

微博的AI团队发布了开源模型VibeThinker-1.5B，这是一个基于阿里巴巴Qwen2.5-Math-1.5B微调而来的15亿参数大语言模型，采用MIT许可协议，可在Hugging Face、GitHub和ModelScope上获取。值得注意的亮点是：其训练后成本仅为7,800美元，远低于同类模型的典型开销。他们并未止步——VibeThinker-3B在AIME 2026上取得了94.3分，与拥有6710亿参数的DeepSeek V3.2并驾齐驱，其基础架构基于Qwen2.5-Coder-3B。

有趣的是，微博实际上是*基于*Qwen进行开发，而非与其正面竞争——他们将Qwen作为基础，并通过独特的训练后方法实现差异化。

**蚂蚁集团——Ling / Ring / Ming系列**

蚂蚁集团（支付宝母公司）的布局更为宏大且独立。2026年2月，蚂蚁集团发布了Ling-2.5-1T，这是其最新的万亿参数大语言模型，以及Ring-2.5-1T，号称是全球首个混合线性架构思维模型——两者均在Hugging Face和ModelScope上以开放许可形式发布。该系列包含三条产品线：Ling非思维模型、Ring思维模型以及多模态Ming系列。效率方面的表现令人瞩目：Ling-2.5-1T在AIME 2026上达到了前沿推理模型的水平，但仅使用约5,890个token，而同类系统则需要15,000至23,000个token。

**关于Qwen的问题**

是的，阿里巴巴拥有Qwen，而蚂蚁集团在技术上是阿里巴巴的关联公司——但两者运作相当独立，各有自己的研发团队和战略动机。蚂蚁集团需要AI用于金融科技应用场景（合规、欺诈检测、客户服务），显然希望拥有自己的技术栈。至于微博，他们以Qwen为基础，这反而验证了Qwen作为生态系统平台的价值，而非受到削弱。

你指出的更广泛的动态确实存在：构建有竞争力的专业化模型的成本已大幅下降，以至于即使是社交媒体平台和金融科技公司也能组建可信的研究团队。与其说是“每个人都从零开始构建”，不如说是“每个人都利用新颖技术在廉价算力上进行微调和训练后优化”——这或许更具看点。

**参考文献：**

- [微博的VibeThinker-1.5B（VentureBeat）](https://venturebeat.com/ai/weibos-new-open-source-ai-model-vibethinker-1-5b-outperforms-deepseek-r1-on)
- [VibeThinker-3B与DeepSeek V3.2比肩（CryptoBriefing）](https://cryptobriefing.com/sina-weibo-vibethinker-3b-matches-top-ai-models/)
- [蚂蚁集团发布Ling-2.5-1T和Ring-2.5-1T（BusinessWire）](https://www.businesswire.com/news/home/20260215551663/en/Ant-Group-Releases-Ling-2.5-1T-and-Ring-2.5-1T-Evolving-Its-Open-Source-AI-Model-Family)
- [蚂蚁集团Ling-2.6-Flash（BusinessWire）](https://www.businesswire.com/news/home/20260422256825/en/Ant-Group-Unveils-Ling-2.6-Flash-A-Major-Leap-in-AI-Efficiency)
