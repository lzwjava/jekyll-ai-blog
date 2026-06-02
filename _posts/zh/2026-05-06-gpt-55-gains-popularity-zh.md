---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-5.5凭借高效性能广受欢迎
translated: true
type: note
---

问题：为什么OpenAI的Codex with GPT-5.5在某些开发者群体中变得更受欢迎，有人声称它比Claude Code with Opus表现更好？

答案：

这是一个非常及时的话题。GPT-5.5由OpenAI于**2026年4月23日至24日**发布，因此这是一场非常新鲜且持续进行的辩论。以下是关于它为何越来越受欢迎以及它与Claude Code（Opus 4.7）实际对比的全面分析。

---

## Codex中的GPT-5.5是什么？

GPT-5.5是OpenAI最新的前沿模型，旨在更快地理解你试图完成的任务，并自行承担更多工作。它擅长编写和调试代码、在线研究、分析数据、创建文档和电子表格、操作软件以及在任务完成前跨工具移动。你无需管理每一步，只需给GPT-5.5一个杂乱、多部分的任务，并信任它能规划、使用工具、检查工作、在模糊性中导航并持续推进。

---

## 为什么一些开发者更偏爱GPT-5.5 / Codex而非Claude Code

### 1. 令牌效率（实际成本更低）

这可以说是某些社区发生转变的**最大原因**。

在相同的编码任务上——相同的提示，相同的目标——GPT-5.5产生的输出令牌比Claude Opus 4.7大约少72%。如果你运行一个每天处理500个任务的编码代理，每个任务在GPT-5.5上平均消耗2000个输出令牌，那么同样的任务在Opus 4.7上大约需要7100个输出令牌。在当前的定价层级下，这种差异在规模化应用时会累积成每月数千美元的成本。

此外，GPT-5.5在实现与GPT-5.4相当的结果时使用的令牌显著更少，其Codex设置运行更快，并为大多数用户提供更高质量的结果。尽管GPT-5.5是一个能力更强的模型，但这些效率提升支持了慷慨的使用限制。

### 2. 速度

更少的令牌意味着更快的响应。GPT-5.5在等效任务上返回结果更快——既因为它生成的令牌更少，也因为其架构针对结构化输出进行了优化。在交互式工作流中，这种延迟差异是明显的。在完全自动化的代理管道中，它决定了吞吐量。

### 3. 代理与计算机使用能力

GPT-5.5在OSWorld-Verified上得分为78.7%，该测试衡量模型能否自主操作真实计算机环境。在针对复杂客户服务工作流的Tau2-bench Telecom上，它达到了98.0%。在Codex中，GPT-5.5可以承担从实现、重构到调试、测试和验证的工程工作。它生成文档、电子表格和演示文稿。结合计算机使用能力，它可以查看屏幕上的内容、点击、输入、导航界面并精确地跨工具移动。

### 4. 紧密的Codex生态系统集成

GPT-5.5在代理任务上确实具有竞争力，尤其是与Codex搭配时。Codex集成为GPT-5.5提供了沙盒执行的自然环境，这在模型需要运行代码、查看输出并迭代时至关重要。与在DIY设置中运行Opus 4.7相比，OpenAI生态系统中的反馈循环更加紧密。

### 5. 工程师的积极评价

测试过该模型的高级工程师表示，GPT-5.5在推理和自主性方面明显强于GPT-5.4和Claude Opus 4.7，能提前发现问题，并在没有明确提示的情况下预测测试和审查需求。一位提前获得访问权限的NVIDIA工程师甚至表示：“失去GPT-5.5的访问权限感觉就像我被截肢了一样。”

### 6. 广泛的企业采用

超过10,000名NVIDIAN员工——涵盖工程、产品、法律、营销、财务、销售、人力资源、运营和开发者项目——已经在使用由GPT-5.5驱动的Codex来实现他们所说的“令人震撼”和“改变生活”的结果。

---

## Claude Code（Opus 4.7）仍然占优的方面

这**绝非一面倒的故事**。Claude Opus 4.7具备真正的优势：

Claude Opus 4.7在代理编码可靠性方面领先——包括SWE-bench性能、长任务指令遵循能力以及更大的上下文窗口。它倾向于在多步骤中保持任务连贯性，不会中途偏离或重新解释目标。当规格说明不明确时，它更可能提出澄清问题，而不是做出糟糕的假设——这在演示中可能令人烦恼，但在生产环境中却极具价值。

在基准测试的直接对比中，Opus 4.7在10项共享基准测试中的6项上领先，GPT-5.5在4项上领先，差距在2到13个百分点之间。Opus 4.7在GPQA、HLE、SWE-Bench Pro、MCP Atlas和FinanceAgent上领先；GPT-5.5在Terminal-Bench 2.0、BrowseComp、OSWorld和CyberGym上领先。

关于延迟：Opus 4.7流式输出第一个令牌大约需要0.5秒，而GPT-5.5的基线约为3秒。对于交互式界面，首令牌时间差距是主导变量。

GPT-5.5仍然存在OpenAI模型的特征模式：它会自信地完成一个任务，但结果可能微妙地错误。

---

## 定价对比（截至2026年5月）

| | GPT-5.5 | Claude Opus 4.7 |
|---|---|---|
| 输入（每百万令牌） | $5 | $5 |
| 输出（每百万令牌） | $30 | $25 |
| 上下文窗口 | 100万令牌 | 100万令牌 |

GPT-5.5在输出上贵约17%。OpenAI的卖点是GPT-5.5完成相同任务所需的输出令牌大约少40%，因此实际账单相比旧型号仅增加约20%——但你的计费仪表盘会告诉你这在实践中是否成立。

---

## 结论

决定取决于你的具体工作负载：Opus 4.7适用于可靠性要求高、周期长的任务；GPT-5.5适用于速度和OpenAI生态系统集成。

在一些开发者社区中对GPT-5.5的炒作是真实且合理的，**针对特定用例**——尤其是高吞吐量的代理管道、已经使用OpenAI技术栈的团队，以及原始速度和令牌效率最重要的任务。然而，Claude Code with Opus 4.7在编码基准测试可靠性和指令遵循连贯性方面仍然领先。没有哪个模型能“普遍获胜”——最佳选择在很大程度上取决于你的工作流程。

参考资料：

- [GPT-5.5 vs Claude Opus 4.7: Real-World Coding Performance - MindStudio](https://www.mindstudio.ai/blog/gpt-55-vs-claude-opus-47-coding-comparison)
- [Claude Opus 4.7 vs GPT-5.5: Which Model Should You Build On? - MindStudio](https://www.mindstudio.ai/blog/claude-opus-4-7-vs-gpt-5-5)
- [GPT-5.5 vs Claude Opus 4.7: Benchmarks, Pricing - Lushbinary](https://lushbinary.com/blog/gpt-5-5-vs-claude-opus-4-7-comparison-benchmarks-pricing/)
- [Introducing GPT-5.5 - OpenAI](https://openai.com/index/introducing-gpt-5-5/)
- [GPT-5.5 vs Claude Opus 4.7: Pricing, Speed, Benchmarks - LLM Stats](https://llm-stats.com/blog/research/gpt-5-5-vs-claude-opus-4-7)
- [OpenAI's New GPT-5.5 Powers Codex on NVIDIA Infrastructure - NVIDIA Blog](https://blogs.nvidia.com/blog/openai-codex-gpt-5-5-ai-agents/)
- [ChatGPT 5.5 vs Claude Opus 4.7: I Tested Both - Emerging AI](https://emergingai.substack.com/p/chatgpt-55-vs-claude-opus-47-i-tested)
