---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude API 2025年定价详解
translated: true
type: note
---

以下是Anthropic Claude各模型API使用价格的清晰说明——不使用表格，只用简洁易懂的文字描述：

---

### Claude Sonnet 4

* **输入token：** 每百万3美元
* **输出token：** 每百万15美元
* **可用折扣：** 通过提示缓存最高可享**9折优惠**，通过批量处理最高可享**5折优惠**。（[custom.typingmind.com][1], [Reddit][2], [Anthropic][3], [Anthropic][4]）

---

### Claude 3.5 Sonnet（现已停用）

* **输入token：** 每百万3美元
* **输出token：** 每百万15美元
* **批处理和缓存费率：** 与其他Sonnet版本相同的分层系统：批量输入1.50美元，批量输出7.50美元，5分钟缓存命中0.30美元。（[Anthropic文档][5]）

---

### Claude 3.7 Sonnet

* **基础定价：** 与3.5版本完全相同——输入每百万3美元，输出每百万15美元——包括使用混合“思考”模式时。（[Reddit][6], [Anthropic文档][5]）

---

### Claude Opus 4

* **输入token：** 每百万15美元
* **输出token：** 每百万75美元
* **批处理和缓存折扣：** 批量输入7.50美元；批量输出37.50美元；缓存命中1.50美元。（[Anthropic][7], [Amazon Web Services, Inc.][8], [Anthropic文档][5], [维基百科][9]）

---

### 快速总结

* **所有Sonnet变体（3.5、3.7、4）：** 输入每百万3美元 / 输出每百万15美元，批处理和缓存可享受更深度折扣。
* **Opus 4：** 价格显著更高，达每百万15/75美元，但专为深度推理、长任务和更高性能需求优化。

---

### 补充说明

* **模型演进：** Claude 3.5 Sonnet在2024年6月发布时在编程能力上树立了新标杆，但尽管性能不断提升，其定价在2025年2月的3.7版本和2025年5月的Sonnet 4中始终保持不变。（[Business Insider][10], [Anthropic][7], [Anthropic文档][5], [维基百科][11]）
* **用例匹配：** 如果您的 workload 以对话为主或需要高吞吐量，Sonnet系列模型能提供卓越的性价比。对于深度复杂任务或长周期智能体工作流，Opus或混合使用不同模型的策略可能更高效。

---

如果您需要基于具体token用量的成本测算、缓存方案对比，或关于模型选择时机的指导——我很乐意为您详细解析！

[1]: https://custom.typingmind.com/tools/estimate-llm-usage-costs/claude-3.5-sonnet?utm_source=chatgpt.com "Anthropic claude-3.5-sonnet API定价计算器"
[2]: https://www.reddit.com/r/ClaudeAI/comments/1jclyjp/can_anthropic_keep_up_with_those_pricing/?utm_source=chatgpt.com "Anthropic能跟上这样的定价吗？: r/ClaudeAI"
[3]: https://www.anthropic.com/news/claude-3-5-sonnet?utm_source=chatgpt.com "Claude 3.5 Sonnet正式发布"
[4]: https://www.anthropic.com/claude/sonnet?utm_source=chatgpt.com "Claude Sonnet 4"
[5]: https://docs.anthropic.com/en/docs/about-claude/pricing?utm_source=chatgpt.com "定价说明"
[6]: https://www.reddit.com/r/ClaudeAI/comments/1ixtyj0/sonnet_37_x_cline_costs_are_skyrocketing/?utm_source=chatgpt.com "Sonnet 3.7 x Cline：成本飙升？: r/ClaudeAI"
[7]: https://www.anthropic.com/news/claude-3-7-sonnet?utm_source=chatgpt.com "Claude 3.7 Sonnet与Claude Code"
[8]: https://aws.amazon.com/marketplace/pp/prodview-h2mamlwah46ym?utm_source=chatgpt.com "AWS市场：Claude 3.5 Sonnet（Amazon Bedrock版）"
[9]: https://zh.wikipedia.org/wiki/Claude_%28%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%29?utm_source=chatgpt.com "Claude（语言模型）"
[10]: https://www.businessinsider.com/anthropic-ai-breakthrough-vibe-coding-revolution-2025-7?utm_source=chatgpt.com "『万亿美元问题』：Anthropic如何让AI在编程领域如此出色？"
[11]: https://en.wikipedia.org/wiki/Claude_%28language_model%29?utm_source=chatgpt.com "Claude（语言模型）"
