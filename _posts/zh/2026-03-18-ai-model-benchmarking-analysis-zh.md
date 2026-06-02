---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Artificial Analysis 的 AI 模型基准测试
translated: true
type: note
---

**问题：** What is artificialanalysis.ai, and is it trustworthy?

**回答：**

## 什么是 Artificial Analysis？

Artificial Analysis 对 AI models、inference API endpoints 和 systems 进行 intelligence、quality、performance 和 price benchmarking——涵盖 proprietary 和 open-weights models。与使用 crowdsourced human votes 的 Arena.ai 不同，Artificial Analysis 采用更 technical、data-driven 的方法。

该网站涵盖多个维度：

- **Intelligence** — 模型在 reasoning、coding、math 和 science 任务中的能力
- **Speed** — API providers 的每秒 output tokens
- **Price** — 每百万 tokens（input 和 output）的成本
- **Latency** — first token 时间和端到端响应时间
- **Image, Video, Speech** — 多模态模型的专用排行榜

---

## 它如何工作

其 performance benchmarking 测量 AI inference 服务真实客户体验的端到端 performance，结果并非代表最大可能的 hardware performance，而是各 provider 的实际 real-world customer experience。

Artificial Analysis Intelligence Index 是一个 composite benchmark，聚合了十个 challenging evaluations——包括 GDPval-AA、τ²-Bench Telecom、Terminal-Bench Hard、SciCode、AA-LCR、AA-Omniscience、IFBench、Humanity's Last Exam、GPQA Diamond 和 CritPt——旨在防止 narrow specialization，并提供单一分数来跟踪 mathematics、science、coding 和 reasoning 的进展，所有 evaluations 均由 Artificial Analysis 独立进行。

例如，其 GDPval-AA evaluation 在 agentic loop 中测试 AI models 在 44 个 occupations 和 9 个 major industries 的 real-world tasks，提供 shell access 和 web browsing capabilities，并通过 blind pairwise comparisons 得出 ELO ratings。

---

## 它可靠吗？优势和局限性

### ✅ 优势

**1. 独立且自动化**

与 Arena 不同，Artificial Analysis 运行自己的 automated benchmarks，而不是依赖 user votes。这消除了 voter manipulation 或 AI labs 的 selective private testing 等问题。

**2. 透明的方法论**

网站发布了每个 metric 的详细定义——包括 blended prices 的计算方式、output speed 的测量方法、time-to-first-token 的定义，以及 reasoning tokens 对 inference performance 的含义——从而可以审视和复制其方法论。

**3. 多维度分析**

它不是单一的“最佳模型”分数，而是帮助您权衡 trade-offs：intelligence 与 cost、speed 与 price，或 provider reliability。这对选择 API providers 的 developers 和 businesses 特别有用。

**4. Provider 级比较**

它独特地跟踪同一模型在多个 cloud providers（如 AWS Bedrock、Together.ai、Azure、Groq）上的表现，这对 real deployment decisions 极为有用，而不仅仅是模型比较。

**5. 专有的 benchmarks**

其 AA-Omniscience index 测量 knowledge reliability 和 hallucination——奖励正确答案并惩罚 hallucinations，分数范围从 -100 到 100，负分表示模型的错误答案多于正确答案。这比简单 accuracy scores 更 nuanced。

---

### ⚠️ 局限性

**1. Benchmark 选择仍是一种主观决定**

Intelligence Index 反映了 Artificial Analysis 选择测量的内容。如果您的 use case 涉及 creative writing、多轮 conversations 或 culturally nuanced tasks，则分数可能不完全 representative。

**2. Automated benchmarks 也可以被 gaming**

就像 Arena 可以通过针对 human preferences 的 targeted fine-tuning 被 gaming 一样，标准 automated benchmarks（如 GPQA、HLE、MMLU）也可以被 labs overfitted。Artificial Analysis 通过使用更 difficult、更 recent 和 proprietary evaluations 来对抗此问题——但风险依然存在。

**3. 缺乏社区 peer review**

与 Arena（已发布多篇 peer-reviewed academic papers）不同，Artificial Analysis 的专有 benchmarks（如 AA-Omniscience 或 AA-LCR）是 self-defined，且尚未被学术社区广泛验证。

**4. Coverage 空白**

一些 newer 或 less prominent models 可能尚未被测试，尤其是缺乏 publicly accessible API endpoints 的模型。

---

## Arena.ai 与 Artificial Analysis：快速比较

|

| **Arena.ai** | **Artificial Analysis** |
|---|---|---|
| **Method** | Human votes (crowdsourced) | Automated benchmarks |
| **Best for** | Judging conversational quality | Comparing speed, cost, intelligence |
| **Bias risks** | Gaming by labs, voter demographics | Benchmark overfitting, self-defined metrics |
| **Transparency** | Moderate (leaderboard policy published) | High (detailed methodology page) |
| **API provider comparison** | No | Yes |
| **Academic validation** | Multiple ICML/NeurIPS papers | Self-published methodology |

---

## 结论

Artificial Analysis **通常更可靠用于 technical 和 business use cases**——特别是在选择 API provider 或平衡 cost 与 performance trade-offs 时。其方法论透明且独立于 AI labs。尽管如此，没有单一 benchmark 网站是完美的。最佳方法是**同时使用两者**——Arena 用于 human-feel quality signals，Artificial Analysis 用于 quantitative performance 和 cost decisions——并理想情况下在您关心的 tasks 上进行自己的 testing。

---

**参考文献：**

- [Artificial Analysis – Homepage](https://artificialanalysis.ai)
- [Artificial Analysis – Methodology](https://artificialanalysis.ai/methodology)
- [Artificial Analysis – Intelligence Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)
