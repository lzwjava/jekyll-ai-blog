---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Scale Labs AI 排行榜概览
translated: true
type: note
---

**https://labs.scale.com/leaderboard** 页面是 Scale AI 的主要 **Scale Labs Leaderboards** 枢纽。它作为一个中央仪表板，展示专家驱动的基准测试，用于测试前沿 AI 模型、agentic capabilities、reasoning、coding、tool use、安全等方面。排行榜在 20 多个严格的、往往面向真实世界的基准上评估了来自主要实验室（OpenAI、Anthropic、Google、Meta 和开源贡献者）的 100 多个模型。

Scale Labs 专注于通过超出简单问答的任务挑战当前 AI 极限——强调 long-horizon agentic behavior、deep reasoning、honest/safe outputs、multimodal understanding 以及 professional-domain expertise。

### Key Highlighted Benchmarks (as of March 19, 2026)
以下是一些突出的可用排行榜：

- **SWE Atlas - Codebase QnA**  
  **SWE Atlas** 套件的一部分（SWE-Bench Pro 的下一个演进）。  
  焦点：复杂真实世界代码库中的 deep code comprehension 和 reasoning。  
  代理必须探索 repositories、在 sandboxes 中运行代码、trace execution，并回答 natural-language questions，而不修改代码。  
  指标：Task Resolve Rate（完美满足每个 expert rubric item 的任务百分比）。  
  顶级模型得分仅 ~30–35%，表明这仍然非常困难。

- **MCP Atlas**  
  通过 **Model Context Protocol (MCP)** 评估真实世界的 tool use。  
  涉及 1,000 个 human-authored tasks（500 个 public）、36 个 real MCP servers、220+ 个 tools，以及 multi-step workflows（每个任务 3–6 个 tool calls）。  
  测试 realistic tool discovery、sequencing、cross-server composition 和 conditional logic。  
  顶级性能：~62% pass rate（例如，Claude Opus 4.5）。

- **SWE-Bench Pro (Public Dataset)**  
  在 public open-source repositories 中的 long-horizon software engineering tasks（bug fixes、features）。  
  编码代理的基础性、广受尊重的基准。

- **SWE-Bench Pro (Private Dataset)**  
  类似任务，但是在 commercial-grade private/proprietary codebases 中——显著更难。

- **Humanity's Last Exam**（以及 Text-Only 变体）  
  处于人类知识前沿的极难问题。

- **SciPredict**  
  预测真实科学实验的结果。

- **Professional Reasoning Benchmark**（Finance 和 Legal）  
  领域特定的 professional reasoning tasks。

- **AudioMultiChallenge**（变体：Audio Output、Text Output）  
  多轮 spoken dialogue systems。

- **Remote Labor Index (RLI)**  
  衡量 AI 代理执行经济上宝贵的 remote work 的能力。

- **PropensityBench** / **MASK**  
  Safety & honesty benchmarks（模拟选择有害行为或撒谎的压力）。

- **VisualToolBench (VTB)** / **VISTA**  
  多模态：对 visual information 的 reasoning 和交互。

- **MultiChallenge** / **MultiNRC**  
  多样化的、跨学科的和 multilingual reasoning challenges。

- **EnigmaEval**  
  复杂的 multi-step reasoning。

- **Fortress**  
  前沿 risk evaluation，用于 national security 和 public safety（CBRNE、terrorism 领域）。

许多排行榜使用 **percentage pass rates** 或 resolve rates，带有 confidence intervals/standard deviations，排名通常纳入 statistical significance（例如，Rank Upper Bound）。

页面包含指向单个排行榜的直接链接、model rankings（顶级表现者如 gpt-5 variants、Claude Opus 4.x 等），以及通常指向 datasets（Hugging Face）、papers 或 announcements 的链接。它反映了 Scale AI 推动更现实、以结果为导向的 agentic AI 评估。

有关最新排名和完整细节，请直接访问主页面，因为 scores 会随着新 model releases 而演变。

References:  

- [Scale Labs Leaderboards Main Page](https://labs.scale.com/leaderboard)
- [SWE Atlas - Codebase QnA Leaderboard](https://labs.scale.com/leaderboard/sweatlas-qna)
- [Scale AI Blog: Can Coding Agents Become Engineers? We're Finding Out.](https://scale.com/blog/swe-atlas)
- [MCP Atlas Leaderboard](https://labs.scale.com/leaderboard/mcp_atlas)