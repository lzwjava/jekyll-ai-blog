---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: MiniMax M2开源AI模型
translated: true
type: note
---

### 什么是 MiniMax M2？

MiniMax M2 是中国人工智能公司 MiniMax AI 最新发布的开源大语言模型，该公司专注于文本、音频、图像和视频的基础模型。该模型于几小时前（截至 2025 年 10 月 27 日）刚刚发布，是一款混合专家模型，专为编程和智能体工作流优化——可将其视为能够规划、执行工具并处理全栈开发、数据分析或多步骤研究等复杂任务的自主 AI 智能体。它并非 GPT 或 Claude 那样的通用模型，但在端到端编程和智能体应用领域表现卓越，并能与 Claude Code、Cursor 或浏览器/Shell 解释器等工具无缝集成。

核心规格：

- **参数量**：总参数量 2300 亿，激活参数量仅 100 亿（追求高效）
- **上下文长度**：最高支持 128K token
- **部署方式**：在 Hugging Face 平台基于 MIT 协议开放，支持 SGLang、vLLM 等自托管框架
- **访问权限**：通过 MiniMax Agent 提供免费 API 试用至 2025 年 11 月 7 日。付费 API 定价为输入 token 每百万 0.3 美元，输出 token 每百万 1.2 美元——约为 Claude 3.5 Sonnet 成本的 8%

该模型采用"交错思考"技术（使用 `
