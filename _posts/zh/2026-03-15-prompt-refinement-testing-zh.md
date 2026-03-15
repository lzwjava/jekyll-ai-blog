---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过实证测试优化提示
translated: true
type: note
---

问题：Claude Code 团队如何开发和完善其 system prompts 和 skills——他们是否使用添加/移除 prompt 部分并运行 interference tests 来比较 prompt 是否有可衡量效果的方法？

回答：

是的，你的直觉基本正确。Claude Code 团队使用严谨的、迭代的、实证方法来开发和完善 system prompts 和 skills——这个过程远超简单的猜测。下面是其工作原理的全面分解：

---

## 1. 早期阶段：快速反馈迭代

Claude Code 从基于 Anthropic 员工和外部用户的反馈进行快速迭代开始。在这个早期阶段，团队会添加或更改 prompt 内容，在内部部署（称为 "dogfooding"），并观察行为上的定性差异——正是你描述的非正式“添加/移除一个 prompt 并查看是否有影响”的方法。

---

## 2. 添加正式 Evals（评估）

后来，他们添加了 evals——首先针对狭窄领域如 concision 和 file edits，然后针对更复杂的如 over-engineering。这些 evals 有助于识别问题、指导改进，并聚焦研究-产品协作。

Evals 本质上是自动化测试套件，用于测量模型是否按预期行为。可以在不部署到生产环境或影响真实用户的情况下，对代理运行数千个任务进行自动化评估。

---

## 3. A/B 测试和生产监控

结合生产监控、A/B 测试、用户研究等，evals 提供了信号，以继续改进 Claude Code 并实现规模化。

这就是你提到的“interference test”概念：两个版本的 prompt 并行运行，团队比较结果，以确定特定 prompt 子句是否有真实的可衡量效果，还是只是噪声。

---

## 4. 模块化 System Prompt 架构

Claude Code 的 system prompts 不是一个巨大的单体 prompt，而是高度模块化。它们包括独立的 prompt 部分，如“Doing tasks (avoid over-engineering)”、“Doing tasks (no premature abstractions)”、“Doing tasks (no compatibility hacks)”和“Doing tasks (no time estimates)”——每个部分独立范围并计算 token 数。

这种模块化设计使团队能够隔离单个 prompt 部分，并测试移除、添加或改写它们是否影响模型行为——这本质上是受控的 ablation testing。

---

## 5. Skills：“Skill Creator”和 Evals 管道

对于 skills（扩展 Claude Code 能力的模块化 SKILL.md 文件），Anthropic 通过 **Claude Code Skills 2.0**（2026 年 3 月 3 日更新）进一步正式化了开发方法。

更新的框架包括：开发测试用例和 benchmarks 来测量 skill 对任务性能的影响；迭代完善 skill 描述以提高触发准确性和可靠性；并使用训练和测试数据集进行精确调整。

更新的 skill-creator 现在由四个并行工作的可组合子代理操作：执行 skill 对 eval prompts 的 executor；评估输出是否符合定义预期的 grader；对 skill 版本进行盲 A/B 比较的 comparator；以及揭示聚合统计可能隐藏模式的 analyzer。

---

## 6. Benchmark 模式：“这个 Skill/Prompt 真的有帮助吗？”

Benchmark 模式在整个 eval 集上运行标准化评估并记录指标。Benchmark 比较 skill 激活时的性能与无 skill（baseline）时的性能，并并排显示，从而提供客观数据来回答根本问题：“这个 skill 真的改善了事情吗？”

还有一个称为 **outgrowth detection** 的概念：如果基础模型即使不加载 skill 也能通过 evals，系统会告诉你“丢弃这个 skill；模型已经足够好了”。这防止了死 prompt 权重随时间积累。

---

## 7. 通过迭代算法的 Prompt 优化

Prompt 优化即使对顶级编码代理也能显著改进——仅优化 Claude Code 的 system prompt 就在通用编码性能上带来了 5%+ 的提升，在专用于单个 repository 时提升更大。该过程使用 benchmark 任务（如 SWE-Bench）的 train/test splits 来验证 prompt 更改是否泛化，而非仅 overfit。

---

## 总结

| Method | Description |
|---|---|
| Fast feedback / dogfooding | 早期阶段的内部使用和用户反馈 |
| Eval-driven development | 针对特定行为的自动化测试套件 |
| A/B testing | 生产环境中 prompt 版本的并排比较 |
| Ablation / modular prompts | 隔离并测试单个 prompt 部分 |
| Benchmark mode | 激活 vs. baseline 的指标比较 |
| Outgrowth detection | 识别并移除模型不再需要的 prompts |

所以是的——你的描述是准确的。团队确实会添加和移除 prompt 子句，并运行“interference”风格的比较，但是在规模化基础上，并使用正式的评估基础设施，使结果具有统计意义而非轶事性。

参考文献：

- [Anthropic: Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Piebald-AI: Claude Code System Prompts (GitHub)](https://github.com/Piebald-AI/claude-code-system-prompts)
- [Claude Code Skills 2.0: Evals, Benchmarks and A/B Testing](https://www.pasqualepillitteri.it/en/news/341/claude-code-skills-2-0-evals-benchmarks-guide)
- [Tessl: Anthropic Brings Evals to Skill-Creator](https://tessl.io/blog/anthropic-brings-evals-to-skill-creator-heres-why-thats-a-big-deal/)
- [Arize: CLAUDE.md Best Practices from Prompt Learning](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
- [Geeky Gadgets: Claude Code Skills 2.0](https://www.geeky-gadgets.com/anthropic-skill-creator/)