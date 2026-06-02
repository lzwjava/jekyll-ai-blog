---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek V4 基准现实检验
translated: true
type: note
---

**问题：** 有人预测 DeepSeek V4 Flash 和 Pro 将在两周内跻身大语言模型基准测试前五——这可信吗？

**回答：**

让我核实一下 DeepSeek 当前发布的版本和基准测试状态。

**问题：** DeepSeek V4-Flash 和 V4-Pro 已经发布了吗？它们能否在基准测试中进入前五？

**回答：**

好消息：你不需要等待。**它们已经发布了。**

DeepSeek V4-Pro 和 V4-Flash 于 2026 年 4 月 24 日以预览版形式推出——两者均采用 MIT 许可开源，支持 100 万 token 上下文，可立即通过 API 和 Hugging Face 获取。

所以，那个说“两周”的人大约滞后了一个月。以下是实际情况：

**架构：**
V4-Pro 是一个总参数量 1.6T、激活参数 49B 的 MoE 模型；V4-Flash 总参数量 284B、激活参数 13B。两者均支持 100 万 token 上下文，最大输出 384K token。

**基准测试现实检验：**
DeepSeek 声称 V4 仅落后最先进的闭源模型 3-6 个月，同时成本仅为 OpenAI 和 Anthropic 等竞争对手的一小部分。但目前的排行榜情况令人清醒——GPT-5、Claude Opus 4.6、Gemini 3.1 Pro、Grok 4 和 DeepSeek V3.2 目前处于 Arena Elo 的前沿区间。V4 尚未取代这一梯队。

DeepSeek V4 Pro 目前在 BenchLM 的临时排行榜上位列 117 个模型中的第 34 名，总分为 70/100。这还不是前五的水平。

**V4 真正的优势所在：**
V4 Flash 在 SWE-bench Verified 上得分为 79%，输入成本为每百万 token 0.14 美元——比 GPT-5.4 Nano 更便宜。在编程基准测试中，Flash 和 Pro 彼此相差不到 1.6 个百分点，但在复杂的智能体任务（Terminal-Bench 2.0：Flash 56.9% 对 Pro 67.9%）上差距明显拉大。

目前，成本方面的优势比基准测试更具说服力。鉴于其性价比，值得将其集成到你的智能体工具中，但“整体前五”仍然由闭源前沿实验室占据。
