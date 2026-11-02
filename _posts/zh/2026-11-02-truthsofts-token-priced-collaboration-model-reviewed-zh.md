---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Truthsoft通证定价协作模式评析
translated: true
type: note
---

问题：https://truthsoft.dev 说得通吗？他们按 token 定价的长期协作模式会是软件开发的未来吗？

回答：

**truthsoft.dev 到底是什么**

它是一家中国的 AI-native 开发工作室（求真软件）——不是 Replit 那样的平台，而是一支真人团队，提供：模型训练、AI 咨询、AI agents/应用，以及通用应用开发（移动端、微信小程序、Web）。标语是 “Think clearly. Build what matters.” 他们的 token 计费（¥20/百万，预付，无过期，cache hits 半价）适用于他们自己的人力/AI 成本，而不是你自己运行的 SaaS 工具。

**这个定位说得通吗？**

说实话——*部分说得通*。下面是拆解：

**做得好的地方：**
- **通过透明度建立信任**——展示真实的过往工作（训练 GPT-2、52GB GPU 集群、猿辅导等客户），而不是含糊的承诺，这确实有差异化。大多数开发工作室都躲在行话后面。
- **按 token 计费与 AI 工作的实际成本结构一致**——企业 AI 成本正在上升，因为从固定费率订阅转向按用量计费；在这种消费模式下，每次 prompt、每轮迭代交互和每个 multi-agent workflow 都会产生直接的 token 成本。Truthsoft 是在诚实地反映这一现实。
- **“长期合作伙伴”定位**——迭代式、非瀑布式的方法适合 AI 时代的产品，因为这些产品一开始需求确实不清晰。

**有风险或不清楚的地方：**
- **把 token 定价转嫁给客户是一个 UX 问题。** 2026 年最聪明的做法是把每百万 token 定价视为众多输入之一，而不是北极星指标。客户很难对不可预测的开支做预算。
- **利润挤压是真实存在的。** Gartner 预测，到 2028 年，AI 编程成本可能超过开发者平均薪资。一个把 token 成本转嫁出去的工作室利润空间很薄，且面临定价压力。
- **“长期合作伙伴”很难变现。** 这是一个很好的卖点，但合同约束偏软——一旦客户内化了相关技能，或者 AI 工具好到他们不再需要开发工作室，客户就容易流失。

---

**相比 Replit 的方向，这是未来吗？**

这些实际上是**不同的押注**：

| | Replit / Cursor / Claude Code | truthsoft.dev |
|---|---|---|
| 模式 | 平台 + 自助式工具 | 以 AI 为杠杆的真人团队 |
| 客户 | 开发者 | 非技术创始人/公司 |
| 可扩展性 | 高（SaaS） | 低（人力工时） |
| 防御性 | 网络效应 + 工具 | 关系 + 信任 |

AI 开发工具的按席位定价正在消亡——随着 OpenAI Codex、Claude Code 和 Cursor 等工具演变为完整的基于 agent 的编程环境，经济模型会发生根本变化。Replit 的方向是在押注任何人都能在 AI 辅助下自己构建软件。这是一个可信的押注。

Truthsoft 的押注更微妙：**大多数公司实际上仍然无法用这些工具真正交付**——他们需要有人知道何时使用哪种工具、如何架构系统、如何管理范围。这同样是一个可信的押注，至少在接下来 3–5 年内如此。

**结论：** 标语 “priced by the token, collaborating anytime” 是真实的——它只是在描述当下 AI 工作的成本方式，不是什么噱头。这个模式作为面向中国市场的 *boutique AI studio* 是说得通的。问题是，随着 AI agents 在自主交付方面变得更强，这种模式能否存活。目前来看：是的，这个方向是真实的。执行力和信任建设（而不是定价模型本身）将决定成败。

参考资料：
- [The Era of Affordable AI Is Over](https://builtin.com/articles/affordable-ai-era-over)
- [Why Per-Token Pricing in 2026 Is a Trap for Most AI Builders](https://tkmxai.it.com/why-per-token-pricing-in-2026-is-a-trap-for-most-ai-builders)
- [Gartner: AI Coding Costs Will Surpass Average Developer Salary by 2028](https://www.devopsdigest.com/gartner-ai-coding-costs-will-surpass-average-developer-salary-by-2028-as-token-consumption-surges)
- [OpenAI Codex Goes Pay-As-You-Go](https://www.contextstudios.ai/blog/openai-codex-goes-pay-as-you-go-what-it-means-for-dev-teams)