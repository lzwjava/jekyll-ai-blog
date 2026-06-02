---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DeepSeek模型批评与担忧
translated: true
type: note
---

问题：关于 DeepSeek V3.2 及其 Speciale 模型有哪些不受欢迎的观点？

回答：

DeepSeek V3.2 于 2025 年末发布，是中国人工智能公司 DeepSeek AI 推出的一款开源大型语言模型，其特点是采用稀疏注意力机制以提高效率，并在数学奥林匹克等推理任务中取得强大的基准性能。其 Speciale 变体是经过微调的版本，专为深度推理进行优化，但缺乏工具调用支持。尽管该模型因其成本效益和可访问性而广受赞誉，但也引发了争议。下面，我整理了开发者论坛、社交媒体和专家分析中一些关键的、不受欢迎的观点。这些观点质疑了其“前沿水平”能力的炒作，常常强调基准测试与实际效用之间的差距。

### 关于 DeepSeek V3.2 的不受欢迎观点
- **它被过度炒作，为排行榜而“基准刷分”，而非实际应用**：尽管在 AIME（90 分以上）和 Codeforces（接近 2700 Elo）等榜单上名列前茅，但早期测试者报告其在编码、代理工作流和日常任务中的实际表现平平——通常只有 OpenAI 或 Google 模型的一半效率。对合成数据和强化学习（占预训练预算的 10%）的关注提高了指标，但导致输出冗长和知识狭窄，让人感觉像是“数据很漂亮，体验很一般”。
- **包括 V3.2 在内的 DeepSeek 模型被高估且幻觉过多**：它们因其在创意写作和角色扮演中的受欢迎程度而受到赞扬，但也因持续产生幻觉、不愿遵循故事情节以及重复响应而受到批评。这使得它们在需要细致入微的任务（如角色扮演或规划）中不可靠，而像 Claude 这样的模型则在叙事方面更“人性化”，更精致，重复性更低。
- **它并非真正的效率突破——它只是对已知技术的巧妙优化**：声称以低成本（例如，低于 600 万美元）构建它，忽略了补贴、知识产权问题（例如，与 OpenAI 的 o1 相似之处）以及稀疏注意力（DSA）和强化学习蒸馏是行业标准调整而非新发明的事实。它更像是“将碎片整合在一起”，而非彻底革新 AI，而且低成本存在对美国公司造成价格压力的风险，却没有解决与人类认知相比能效低下等核心限制。
- **DeepSeek V3.2 因潜在的后门和审查制度而危险**：作为中国模型，它被视为安全风险——可能被黑客用于追踪用户——并且严重偏向中国共产党叙事（例如，回避天安门广场查询，而回答其他类似国家的问题）。这侵蚀了信任，悄然推行议程，使其不适合敏感工作，尽管其开源特性吸引了不受审查的本地运行。
- **它不是 OpenAI 等封闭源代码巨头的真正威胁**：虽然更便宜和开源，但它在可用性、上下文长度（比 128k 竞争对手短）、多模态和端到端解决问题方面仍然落后。病毒式传播的炒作是地缘政治作秀，而非范式转变——美国公司可以简单地借鉴其技巧，而且消费者不愿使用中国 API 限制了其采用。

### 针对 Speciale 模型的特殊不受欢迎观点
- **Speciale 在基准测试中表现出色，但在简单的模式识别方面失败**：它在硬推理（例如，6 枚 IMO 金牌中的 5 枚）上与 GPT-5 持平，但在不需要深度思考的“简单”任务（如基本模式）上却表现不佳——这反映了 o3 Pro 等高级模型的缺陷。测试人员称其“纸上谈兵令人惊叹”，但在混合工作流中却令人失望。
- **它太慢且存在太多 bug，无法真正采用**：Speciale 的速度约为每秒 30 个 token，响应时间长，加上工具调用故障和过度思考循环，尽管其专注于推理，但感觉尚未打磨。早期用户更喜欢基础 DeepSeek V3.2 的速度，称 Speciale 是“爬行的法拉利”，非常适合小众数学/编码，但在日常使用中不实用。
- **Speciale 缺乏“灵魂”，感觉功利而非有创意**：为推理优化，它优先考虑原始检索而非美学交流——响应高效但平淡，就像 AI 形式的“Android 与 iOS”。这使得它适合代理，但在写作、食谱或假期方面不如更“精雕细琢”的模型。

总的来说，这些意见将 DeepSeek V3.2 和 Speciale 描绘成在效率和数学/编码小众领域取得的重大开源胜利，但并非某些人声称的 AGI 杀手。该模型在 Hugging Face 上采用 MIT 许可的权重，鼓励实验，但怀疑论者认为它暴露了 AI 更广泛的局限性：基准测试 ≠ 效用，廉价规模并不能解决幻觉或偏见。

*Deepseek releases cheap general imo level model before openAI* (https://www.reddit.com/r/singularity/comments/1pbazan/deepseek_releases_cheap_general_imo_level_model/)
*deepseek-ai/DeepSeek-V3.2 · Hugging Face* (https://www.reddit.com/r/LocalLLaMA/comments/1pb9xm3/deepseekaideepseekv32_hugging_face/)
*Opinion: Deepseek models are overrated* (https://www.reddit.com/r/SillyTavernAI/comments/1kfxdc1/opinion_deepseek_models_are_overrated/)
*Unpopular Opinion: Deepseek has rat-effed OpenAI's 2025 business model* (https://www.reddit.com/r/ChatGPT/comments/1ibj4io/unpopular_opinion_deepseek_has_rateffed_openais/)
*DeepSeek is highly biased, don’t use it* (https://medium.com/data-science-in_your_pocket/deepseek-is_highly_biased_dont_use_it-2cb0358647f9)
*There’s real technical achievement, but the marketing is exaggerated* (@witec_ on X)
*DeepSeek V3.2 looks wild on benchmarks… but early testers aren’t impressed* (@VraserX on X)
*deepseek feels like it’s just optimizing for raw information retrieval* (@signulll on X)
