---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2026年5-6月重大人工智能发展
translated: true
type: note
---

**问题：** 过去一个月（2026年5月至6月），包括Claude Fable 5在内的主要人工智能发展有哪些？

**回答：**

最大的新闻发生在两天前——并且充分披露，这正是您此刻正在对话的模型：

**Anthropic：Claude Fable 5 + Mythos 5（6月9日）**

Fable 5 是一款Mythos级别的模型——比Opus高一个等级——经过安全处理后可普遍使用。它在几乎所有测试基准上都达到了最先进水平，并且随着任务变长、变复杂，其领先优势会进一步扩大。一个有趣的工程细节是其发布机制：涉及某些主题（网络安全、生物学）的查询会被安全措施拦截，转而由Opus 4.8回答，分类器采用保守调节——平均在不到5%的会话中触发。对于API集成来说，这意味着三个变化：处理拒绝响应、回退到另一个Claude模型的重试逻辑，以及新的计费规则——这基本上是第一个需要在代理循环中为分类器拒绝的请求进行架构设计的前沿模型。订阅访问权限分阶段提供：截至6月22日包含在Pro/Max/Team计划中，随后于6月23日转为使用额度计费。Mythos 5本身具有相同的基础能力，但解除了安全限制，仅限获批组织使用——Project Glasswing网络安全合作伙伴和选定的生物学研究人员。背景信息：Mythos Preview发现了数千个关键和严重级别的网络漏洞，包括所有主流操作系统和浏览器中的错误。

供您路由决策参考的价格背景：Fable 5 vs GPT-5.5 Pro的直接对比显示，Fable 5在8个编码基准测试中平均领先约11.8分，价格为每百万token 50美元 vs 180美元。

**DeepSeek V4 —— 与您的MoE研究直接相关**

您已经在使用v4-flash/v4-pro，但最新消息是：5月22日，DeepSeek将其75%折扣的"促销"定价永久化——V4-Pro每百万token收费0.435/0.87美元，在一个18项编码评测中，与GPT-5.5（5/30美元）的差距约为2个百分点，而非20个。值得深入研究的架构细节（供您探索MoE时参考）：V4-Pro拥有1.6万亿参数，活跃参数490亿，支持100万上下文，使用混合注意力机制（压缩稀疏注意力 + 高度压缩注意力）以及流形约束超连接，提供非思考/思考/Think-Max模式。KV缓存的结果最为突出：在100万上下文时，V4-Pro仅需V3.2所需KV缓存的10%，并在MRCR 100万大海捞针测试中得分83.5%——在该基准上击败了Gemini 3.1 Pro。它还在LiveCodeBench上取得了93.5%的分数，是所有模型中最高的——采用MIT许可，因此可自行托管。

**Google：Gemini 3.5 Flash（5月19日，I/O 2026）**

一款Flash级别的模型，在编码/代理基准测试中击败了Pro级别的旗舰产品——Terminal-Bench得分76.2%，MMMU-Pro多模态得分最高（84.2%），在MCP编排的工具使用方面表现最强，价格为每百万token 1.50/9美元。Gemini 3.5 Pro在I/O大会上被确认将于"下个月"发布，使其进入6月窗口期。

**其他值得关注的方向：**

* Anthropic、OpenAI和SpaceX都在走向公开市场；Anthropic还公开敦促各实验室建立协调一致的"刹车踏板"以控制前沿发展，警告递归自我改进正在临近。
* 科罗拉多州的AI法案将于6月30日生效——这是2026年实际落地的最具影响力的美国AI法规，而联邦层面的优先权（《伟大的美国AI法案》）仍在委员会中停滞不前。
* 计算资源正变得地缘政治化：美日AI合作扩大，英加签署了计算协议。
* 据报道，ChatGPT月活跃用户已突破10亿。

针对您的具体研究轨迹：我真正建议深入研究的两个方向是DeepSeek V4技术报告（混合稀疏注意力 + 10倍KV缓存减少是本季度最具复用价值的架构思路——可直接应用于您在MI300X上进行的nanoGPT规模实验）以及Fable 5的分类器回退API模式，因为带拒绝处理的多模型路由正在成为必要的代理原语，而非边缘情况。

**参考文献：**

* [Claude Fable 5 and Claude Mythos 5 — Anthropic](https://www.anthropic.com/news/claude-fable-5-mythos-5)
* [Introducing Claude Fable 5 and Claude Mythos 5 — Claude API Docs](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5)
* [Anthropic's Claude Fable 5 — TechCrunch](https://techcrunch.com/2026/06/09/anthropics-claude-fable-5-is-a-version-of-mythos-the-public-can-access-today/)
* [GPT-5.5 vs DeepSeek V4 — DataCamp](https://www.datacamp.com/blog/deepseek-v4-vs-gpt-5-5)
* [Gemini 3.5 Flash vs GPT-5.5 vs Claude vs DeepSeek — BuildFastWithAI](https://www.buildfastwithai.com/blogs/gemini-3-5-flash-vs-gpt-5-5-claude-deepseek-2026)
* [GPT-5.5 vs Gemini 3.5 Flash vs DeepSeek V4 on 18 tasks — Towards AI](https://medium.com/@chewloongnian/i-tested-gpt-5-5-vs-gemini-3-5-flash-vs-deepseek-v4-the-cheapest-shouldnt-be-this-close-3d1031a0b41e)
