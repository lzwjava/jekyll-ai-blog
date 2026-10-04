---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 有AI智能体的一人公司
translated: true
type: note
---

**问题：** 人们真的会从家里运行一个一人公司（OPC）吗？使用多台计算机或 AI agents 并行工作，为客户进行 software consulting？它能成功吗？鉴于人类无法如此 multitask，目前的结果如何？

**答案：**

是的，人们正在这样做，而你的 multitasking 担忧是主要限制。

**现状**

- OPC 模型是真实且不断增长的，尤其在中国。截至去年底，中国新注册的 OPC 接近 732 万，同比增长 42.3%，这得益于修订后的《公司法》和 agentic AI 工具。
- 超过 20 个中国城市推出了针对 OPC 的扶持政策。
- 注册数量并不能说明这些公司中有多少真正赚钱。

**他们真的运行 10 台机器吗？**

- 大多不是。AI agents 是软件，所以它们通常运行在云端或一台机器上。据报道，大多数一人公司运行 3–6 个专门 agents（research、content、code、sales、support），共享一个 memory。
- 限制不在于计算机。而在于一个人可以监督多少事情。

**你的 multitasking 观点是正确的**

- Agents 可以将执行并行化，但你仍然要负责审查、决策、客户沟通、销售，并为结果承担责任。
- 一篇关于 agent-assisted coding 的评论指出，你必须定义哪些 repos 和 environments 允许 auto mode，哪些更改仍然需要人工参与，以及如何记录 actions。这就是人类的 bottleneck。
- 据报道的 gains 比“10 个人”要温和。一份报告称，典型案例展示了 3–5 倍的 efficiency gains，一个人完成了 5 人团队的工作。
- 十个 parallel agents 并不能带来 10× 的 output。它们带来了 10 倍你需要检查的 output，而交付给客户的糟糕 code 是你的 liability。

**报告的结果**

- 成功案例主要是 product builders，而非 consultants。例如，Base44 的创始人在六个月内独自构建了它，并以 8000 万美元卖给了 Wix。此外，YC 最新 batch 中 19% 的创始人是 solo 创始人，核心团队中位数为 3 人。
- 对证据的提醒：我发现的大部分信息来自 trend newsletters 和推广 blogs，有些是 auto-generated 的，而非来自 audited studies。有消息称 77% 的 solopreneurs 在第一年 profitable，但我会持怀疑态度，因为没有明确的 survivorship-bias 修正。

**Software consulting 能以这种方式成功吗？**

- 可以，如果你保持 small 和 realistic。Consulting 是一个很好的 fit，因为客户按 outcomes 付费，而 agents 可以加快 scoping、prototyping、boilerplate、tests 和 docs。
- 成功通常取决于：
  - **狭窄的 niche**，例如一个 industry 或一种 integration。
  - **限制 active projects** 数量，以你能亲自 review 为准，通常是 2–4 个，而不是 10 个。
  - **审查所有发给客户的内容**，以 tests 作为 safety net。
  - **Sales 和 trust**，这是 AI 无法替代的，并且往往是真正的 bottleneck。
  - **按 value 定价**，而不是按 hours，因为你的 hourly cost 在不断下降。
- 风险包括客户自己使用 AI 来做这件事、competitors 使用同样 tool 带来的 price pressure、quality 和 security errors，以及持续 context-switching 导致的 burnout。

简而言之，一个人加上 agents 可以完成一个小团队的工作，但不是一支 army。期望获得一个不错的 solo consulting income，而不是一个 10 人 agency，并通过 quality 和 niche 来 scale，而不是 machine count。

**参考文献：**

- [One-Person Company Software: The Solo AI Tool Stack (2026)](https://www.taskade.com/blog/one-person-companies)
- [AI-Enabled One-Person Companies Present a Corporate Law Quandary](https://news.bloomberglaw.com/legal-exchange-insights-and-commentary/ai-enabled-one-person-companies-present-a-corporate-law-quandary)
- [One Person Company (Baidu Wiki)](https://baike.baidu.com/en/item/One%20Person%20Company/1479943)
- [How to Start a One-Person Business with AI Agents](https://nevermined.ai/blog/one-person-business-with-ai-agents)
- [Agents Become the Customer: How Solo Founders Capture the August 2026 Agent-Stack Dividend](https://opcreport.github.io/2026/08/29/opc-report-2026-08-29-1006/)
- [OPC AI Startup Trends: From WAIC Challenge to Zero-Human Company Law](https://opcreport.cn/opc-report-2026-07-14-1804/)
