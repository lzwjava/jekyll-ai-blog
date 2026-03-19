---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SWE Atlas 代码库问答排行榜概览
translated: true
type: note
---

**SWE Atlas - Codebase QnA** 排行榜，托管在 https://labs.scale.com/leaderboard/sweatlas-qna，是 Scale AI 的 **SWE Atlas** 基准套件的一部分。SWE Atlas 使用真实世界的复杂代码库，在专业软件工程任务上评估 AI coding agents。

**Codebase QnA** 专门衡量 **deep code comprehension and reasoning** ——在进行任何代码更改之前所需的上游技能。它测试 AI 代理理解和解释大型生产级软件系统行为的能力。

### Key Features
- **Dataset**：来自 11 个活跃维护的开源仓库（从 SWE-Bench Pro 中选取）的 124 个具有挑战性的 QA 任务，涵盖 Go、Python、C 和 TypeScript。示例包括邮件服务器、终端仿真器、对象存储系统、可观测性平台和秘密扫描器。
- **Task Type**：代理接收自然语言的、往往不完整的查询，这些查询模仿真实工程师的询问（例如，“How does the system handle disk failure in this configuration?”）。它们必须自主探索代码库，在沙箱化的 Docker 环境中构建和运行软件，追踪跨多个文件的执行路径，分析运行时行为，并提供详细、准确的答案。
- **Constraints**：代理可以使用 shell 工具（bash、grep 等），但严格禁止修改任何源代码——违规将导致自动失败。
- **Evaluation**：
  - 使用结构化的、由人类专家定义的 rubric，每个任务平均 ~12.3 个 atomic factual criteria。
  - LLM judge（Claude Opus 4.5）评分每个 criterion 是否完全满足。
  - 主要指标：**Task Resolve Rate** ——代理答案通过 **所有** rubric 项并获得完美分数 1.0 的任务百分比。
- **Purpose**：突出当前前沿模型在深度推理真实代码执行和架构方面的差距，超出静态分析或简单 bug fixing。

### Performance Highlights (as of March 2026)
即使顶级模型也面临重大挑战：
- 领先分数约为 **30–35%** resolve rate。
- 顶级条目包括：
  - gpt-5.4-codex (xHigh, Codex CLI)：**35.48% ± 8.70**
  - claude-opus-4.6 Thinking (Claude Code Harness)：**31.50% ± 8.62**
  - gpt-5.2-2025-12-11 (High, SWE-Agent)：**29.03% ± 8.53**
- 领先开源模型：GLM-5 约为 21.77%。

这比标准 SWE-Bench 任务明显更难（在 bug-fixing 上顶级模型可能超过 40–70%），表明深度、运行时感知的理解仍是一个主要挑战。

整体而言，SWE Atlas 包括三个计划中的排行榜（Codebase QnA 是第一个发布的；Test Writing 和 Refactoring 即将推出）。完整数据集在 Hugging Face 上公开可用：ScaleAI/SWE-Atlas-QnA。

References:  

- [Scale Labs SWE Atlas - Codebase QnA Leaderboard](https://labs.scale.com/leaderboard/sweatlas-qna)
- [Hugging Face Dataset: ScaleAI/SWE-Atlas-QnA](https://huggingface.co/datasets/ScaleAI/SWE-Atlas-QnA)
- [Scale AI announcement on LinkedIn (introducing SWE-Atlas)](https://www.linkedin.com/posts/scaleai_were-introducing-swe-atlas-to-measure-which-activity-7435008304940052480-xXCr)