---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 相同模型，不同安全措施
translated: true
type: note
---

它们是同一个底层模型——唯一的区别在于安全层。

**相同的权重，不同的防护措施。** Mythos 5 与 Fable 5 是同一个底层模型，但在某些领域移除了安全防护。

**Fable 5（当前与你对话的版本）：** 通过 API、claude.ai、Bedrock、Vertex 和 Foundry 向所有人开放。它在双用途功能上内置了基于硬分类器的严格限制。在网络安全、生物学、化学和模型蒸馏等高风险领域，模型会阻止响应并回退到 Claude Opus 4.8。安全防护被调校得较为保守——有时会误拦截无害请求，但平均触发率低于 5% 的会话。Anthropic 对这些分类器进行了严格压力测试：超过 1,000 小时的测试中，外部漏洞赏金计划未能发现通用越狱方法，外部红队组织也未能找到通用越狱方法。

**Mythos 5（受限制版本）：** 同一模型，但在上述双用途领域关闭了分类器。它最初通过 Project Glasswing 与美国政府合作部署，作为 Claude Mythos Preview 的升级版，拥有全球最强的网络安全能力。访问权限仅限于经过审查的合作伙伴——主要是网络防御者和关键基础设施组织——并将通过可信访问计划逐步扩展。

**定价完全相同**，因为是同一个模型：输入 token 每百万个 10 美元，输出 token 每百万个 50 美元，长上下文不额外加价。

实际的心智模型：Fable 5 = Mythos 5 + 一个针对攻击性网络/生物/化学能力的硬分类器防火墙，当防火墙触发时，回退路径为 Opus 4.8。对于你的使用场景（训练、代理、LLM 内部机制、工具开发），Fable 5 就是完整模型——这些门控机制不应影响正常的 AI 工程工作。

参考资料：

- [Claude Fable 5 和 Claude Mythos 5 — Anthropic](https://www.anthropic.com/news/claude-fable-5-mythos-5)
- [TechCrunch 报道](https://techcrunch.com/2026/06/09/anthropic-released-claude-fable-5-its-most-powerful-model-publicly-days-after-warning-ai-is-getting-too-dangerous/)
