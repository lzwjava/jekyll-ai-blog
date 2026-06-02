---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Dify AI平台概览
translated: true
type: note
---

### 什么是 Dify.ai？
Dify.ai 是一个开源的、低代码平台，用于构建和部署由大语言模型（LLMs）驱动的生成式 AI 应用。它于 2023 年推出，专注于智能体工作流、检索增强生成（RAG）管道和 AI 智能体，使开发者、团队和企业能够更轻松地创建聊天机器人、副驾驶和复杂自动化应用，而无需深入的编码知识。该平台支持自托管，提供拖放式界面，并通过可扩展的基础设施、模型管理和插件市场强调生产就绪性。可以将其视为"云端的 LangChain"，但更加用户友好和可视化，与 Flowise 或 Vercel AI 等工具竞争。

截至 2025 年 11 月，Dify 在 AI 智能体热潮中蓬勃发展，拥有强大的社区势头和企业采用率。它在亚洲地区（例如与阿里云的集成）以及 B2B 用例（如客户支持自动化和知识管道）中尤其受欢迎。

### 主要特性
- **可视化工作流构建器**：用于多步骤 AI 智能体的拖放式界面，包括迭代循环、条件逻辑和工具编排。
- **RAG 与知识管道**：从网络、数据库或文件摄取数据；索引到向量存储；并启用上下文感知响应。
- **LLM 灵活性**：在 100 多个模型（如 Llama 等开源模型或 GPT/Claude 等专有模型）之间切换，并内置性能基准测试。
- **插件与集成**：市场中有 120 多个插件，包括 2025 年新增的 Firecrawl（网络爬取）、Qdrant/TiDB（向量存储）、Tavily（搜索）、Bright Data（结构化数据）、TrueFoundry（AI 网关）和 Arize（可观测性）。支持用于 API/数据库桥接的 MCP。
- **部署选项**：云托管（后端即服务）、自托管或可嵌入；具备单点登录（SSO）、审计日志和高流量可扩展性等企业功能。
- **从无代码到专业**：提供适合初学者的模板，但可通过自定义代码、调试工具和监控进行扩展。

最近的更新包括 v1.0.0（2025 年 2 月发布），具有解耦插件以便于扩展；基于 HTTP 的 MCP 支持（2025 年 3 月协议）；以及一个新的官方论坛，用于社区问答。

### 发展现状如何？增长与指标
Dify 的增长在 2025 年加速，乘着 AI 智能体采用的浪潮。其大部分成功是通过开源贡献（GitHub Star 数达数万）和开发者间的病毒式分享自主实现的。

| 指标                  | 详情（截至 2025 年 11 月）                  |
|-------------------------|-------------------------------------------|
| **年度经常性收入（ARR）** | 310 万美元（自 2023 年推出以来持续增长） |
| **团队规模**          | 28 名员工（精简、高效的运营） |
| **总融资额**      | 139 万美元（A 轮融资于 2024 年 8 月由阿里云和 VCshare 领投；2025 年未宣布重大融资轮次） |
| **用户群/流量**  | 全球部署了数百万个应用；月访问量超过 6000 万（62% 为直接流量，开发者占很大比例）；受众 63% 为男性，25-34 岁年龄段占主导 |
| **采用亮点**| 受到沃尔沃汽车（AI 导航）、消费电子公司（将任务分析时间从 8 小时减少到 3 小时）以及大型组织中 20 多个部门的信任；在生物医学、汽车和 SaaS 领域活跃 |

它虽然尚未像 n8n 那样成为独角兽，但收入同比增长了两倍，自托管模式在注重隐私的团队中推动了有机传播。

### 用户评价与反馈
反馈大体上是积极的，特别是在易用性和快速原型设计方面——用户喜欢它如何"民主化 AI 智能体"，而无需处理 SDK 的麻烦。在 G2 上（来自 100 多条评论，平均评分 4.5-4.7/5），优点包括直观的 UI、强大的 RAG 以及相较于定制构建的成本节约。缺点包括：偶尔的生产环境扩展问题（例如，高负载下的调试）以及高级智能体的学习曲线。

来自近期 X 平台（主要是英语/日语开发者社区）的讨论：
- 对集成的兴奋："使用 Firecrawl 后性能提升了 10 倍"以及"Qdrant 用于企业 RAG 具有颠覆性"。
- 社区成果：新论坛因快速修复错误（例如 Gemini 问题）而受到好评。
- 小抱怨：计费故障（例如学生计划退款）以及希望有更多"类方法"的可重用块。
- 整体氛围：活跃、协作——关于 DeepResearch（自动化多步骤搜索）等工作流的帖子显示了其实用性。

对于独立开发者和中端市场 B2B 来说，它很可靠，但企业用户指出其在超大规模应用方面仍在成熟中（为此可与 Higress 等网关配合使用）。

### 为何备受关注
在 2025 年的"智能体经济"中，Dify 通过弥合无代码可访问性与专业扩展性之间的差距（且全部开源）而大放异彩。随着 AI 从炒作转向运营（例如，自动化研究或客户互动），其对可观测、可扩展工作流的关注使其定位良好。如果您正在构建 LLM 应用，它是一个首选——提供免费层级供入门，付费计划面向团队（根据抱怨推断为 59 美元+/月，但请查阅官网确认）。

参考文献：
[Dify AI Review 2025](https://www.gptbots.ai/blog/dify-ai)
[How Dify Hit $3.1M Revenue](https://getlatka.com/companies/dify.ai)
[Dify Buyer's Guide 2025](https://skywork.ai/blog/dify-review-buyers-guide-2025/)
[Dify Strategic Overview](https://www.baytechconsulting.com/blog/what-is-dify-ai-2025)
[Dify Funding Profile](https://pitchbook.com/profiles/company/539409-43)
[Dify G2 Reviews](https://www.g2.com/products/dify-ai/reviews)
[Dify v1.0.0 Release](https://dify.ai/blog)
[Dify Traffic Analytics](https://www.similarweb.com/website/dify.ai/)
[Dify Integrations Blog](https://dify.ai/blog/dify-x-qdrant-building-and-powering-the-next-gen-ai-applications)
[Dify Forum Launch](https://forum.dify.ai/)
[Dify X Posts](https://x.com/dify_ai)
