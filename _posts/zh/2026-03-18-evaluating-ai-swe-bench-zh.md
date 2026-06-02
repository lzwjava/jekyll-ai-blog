---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 SWE-bench 基准评估 AI
translated: true
type: note
---

问题：What is SWE-bench, how does it evaluate AI models, and is it trustworthy?

回答：

## SWE-bench：全面介绍

### SWE-bench 是什么？

SWE-bench（Software Engineering Benchmark）是一个基准测试，旨在衡量 AI 语言模型解决**real-world GitHub issues**的能力。它通过爬取 12 个流行 Python 仓库的 Pull Requests 和 Issues，收集了 2,294 个任务实例。每个实例基于一个 pull request，该 pull request（1）与一个 issue 相关联，并且（2）修改了一个或多个 testing-related files。

它在 2024 年 ICLR 的一篇论文中引入：《"SWE-bench: Can Language Models Resolve Real-world GitHub Issues?"*》，由 Princeton 的研究人员撰写。

---

### 基准测试变体

SWE-bench 已发展成为一系列相关基准测试：

- **SWE-bench Full** — 原始数据集，包含来自 12 个 Python 仓库的 2,294 个任务。
- **SWE-bench Lite** — 一个较小的精选子集，用于成本更低的评估（300 个任务）。
- **SWE-bench Verified** — 与 OpenAI 合作于 2024 年 8 月发布的经人工验证的 SWE-bench 子集，旨在更可靠地评估 AI 模型解决真实世界软件问题的能力。
- **SWE-bench Multimodal** — 包含视觉元素的 issues（517 个任务）。
- **SWE-bench Multilingual** — 涵盖 Python 之外的 9 种编程语言的 300 个任务。

---

### SWE-bench 如何评估 AI 模型？

评估过程遵循清晰、结构化的管道：

**1. 任务设置**

每个实例都会构建一个执行环境（Docker image），其中仓库在 Pull Request 基于的 commit 上成功安装。没有 Pull Request 的更改时，一些测试会失败。Pull Request 合并后，相同的测试集会通过。这些“Fail-to-Pass”测试是评估的主要信号。

**2. 模型输入**

模型获得一个代码仓库的访问权限，以及需要修复的 issue 描述。然后，模型必须调查并修改仓库以解决问题。

**3. Patch 生成**

AI 系统（agent）自主导航代码库，生成代码更改，并产生一个“patch”——一个修改仓库以解决问题的 diff。

**4. 基于测试的评分**

提出的编辑通过运行 FAIL_TO_PASS 和 PASS_TO_PASS 测试进行评估。如果 FAIL_TO_PASS 测试通过，则表示编辑解决了问题。如果 PASS_TO_PASS 测试通过，则表示编辑没有无意中破坏代码库的其他部分。两组测试都必须通过，编辑才算完全解决了原始 GitHub issue。

**5. 容器化执行**

SWE-bench 通过将模型生成的 patches 应用到真实世界仓库并运行仓库的测试来评估模型，以验证问题是否得到解决。评估在容器化的 Docker 环境中进行。

**6. 分数报告**

关键指标是 **% Resolved** —— AI 成功生成通过的 patch 的任务实例百分比。截至 2026 年初，顶级 agent 在 SWE-bench Verified 上的得分超过 70%。

---

### SWE-bench Verified 人工验证过程

该数据集通过涉及 93 名软件开发者的严格人工标注过程进行精选。每份样本由三位独立的标注者审查，以确保 issue 描述规范明确、unit tests 合适，并且样本没有其他可能导致评估不可靠的主要问题。

---

### SWE-bench 是否可信？

SWE-bench 受到广泛尊重并被广泛使用，但存在几个已知局限性和批评，这些会影响对其分数的面值信任程度。

#### ✅ 优势

- **真实世界基础**：任务来自生产代码库中的实际 GitHub issues，而不是合成谜题。
- **自动化、可重复评分**：基于 Docker 的执行确保评估一致性。
- **人工验证**（Verified 变体）：标注者过滤掉不可解或模糊的任务。
- **公开排行榜和开源工具**：社区透明度高。

#### ⚠️ 已知弱点和批评

**1. Data Contamination**

超过 94% 的 SWE-bench Verified issues 及其 ground-truth pull requests 早于领先 LLM 的知识截止日期。这提高了许多模型在训练期间可能接触到底层数据，从而通过记忆而非真正推理来夸大报告分数的可能性。

**2. Weak Test Oracles**

用于验证每个提交的测试套件通常仅运行 PR 中修改的测试文件，而不是所有可用测试，这导致通过率被高估 4–7%（绝对值），因为遗漏了回归案例。换言之，一个 patch 可以通过测试但在语义上仍然不正确。

**3. Benchmark Overfitting / Overestimation**

像 SWE-bench Verified 这样的基准测试由于过度依赖正式的 GitHub issue 描述、语言一致性和过拟合，会系统性地高估 agent 能力高达 ~20%。

**4. 任务范围有限**

SWE-bench Verified 预测 AI 是否能修复简单问题（软件工程师最多需要几小时解决）在代码库中。此外，代码库的低多样性限制了外部有效性。值得注意的是，Django 占所有 issues 的近一半，五个仓库占基准的 80% 以上。

**5. 残余错误率**

一些样本可能仍然模糊——先前估计的错误率为 5–10%。

**6. Harness Dependency**

SWE-bench 的一个显著复杂性在于它同时评估 agentic harness 和底层 foundation model。这导致 foundation model 实验室在报告结果时采用不同的方法。换言之，分数会因模型的 scaffolding 方式而显著不同，而不仅仅是模型本身。

---

### 新兴响应：SWE-bench Pro

为了解决上述局限性，新兴基准测试如 **SWE-bench Pro** 已出现。SWE-bench Pro 旨在解决 data contamination、任务多样性有限、问题过于简单以及测试不可靠等问题。它包含来自 41 个专业仓库的 1,865 个任务，包括私有专有代码库。虽然大多数顶级模型在 SWE-bench Verified 上的得分超过 70%，但表现最好的模型在 SWE-bench Pro 上的得分仅约为 23%，这突显了新基准的难度和真实性增加。

---

### 总结判断

SWE-bench 是当今评估 AI 软件工程 agent **最广泛采用且最可信的基准测试**。其分数有意义且在方向上可靠，用于比较模型。但是，由于 data contamination 风险、代码库多样性有限、测试覆盖薄弱以及 harness 变异性，**原始数字不应被视为绝对真理**。最好将其用作*相对*信号，而不是真实世界能力的精确衡量。

参考文献：

- [SWE-bench Official Site](https://www.swebench.com)
- [SWE-bench Original Paper (ICLR 2024)](https://openreview.net/forum?id=VTF8yNQM66)
- [OpenAI: Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)
- [Epoch AI: SWE-bench Verified Review](https://epoch.ai/benchmarks/swe-bench-verified)
- [Epoch AI Substack: What does SWE-bench Verified actually measure?](https://epochai.substack.com/p/what-skills-does-swe-bench-verified-evaluate)
- [SWE-bench Evaluation Docs](https://www.swebench.com/SWE-bench/guides/evaluation/)
- [Scale Labs: SWE-bench Pro Leaderboard](https://labs.scale.com/leaderboard/swe_bench_pro_public)
- [Vals.ai SWE-bench Analysis](https://www.vals.ai/benchmarks/swebench)
