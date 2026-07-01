---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 卡帕西的AI编码指南
translated: true
type: note
---

问题：什么是卡帕西（Karpathy）的指南，以及其中的"元技能"概念是什么？

答案：

## 卡帕西指南——概述

**卡帕西指南** 指的是一个广为流传的 GitHub 仓库（`forrestchang/andrej-karpathy-skills`），其中包含一个单一的 `CLAUDE.md` 文件。它由开发者 Forrest Chang 创建，他将 Andrej Karpathy 关于 LLM 编码常见陷阱的广为传播的观察提炼成一个可直接操作的 `CLAUDE.md` 文件。

卡帕西式的指南提出了一个非常实用的建议：不要只是提示你的代理（agent），而是通过简单的规则来训练它的行为。这通常是通过一个与代码并存的 `CLAUDE.md` 文件来完成的。与其试图对每个提示进行微观管理，不如定义代理应该如何思考和行动。而四条原则就足以解决大多数现实问题。

---

## 卡帕西指出的问题

LLM 编码助手速度很快，但它们倾向于过度工程化、重构没人要求的内容，并且隐藏假设。这些并非能力问题——模型能够编写正确、精简的代码——它只是默认做得太多。如果不加约束，你最终会审查比实际需要大三倍的差异（diff）。

具体来说，卡帕西指出了三种反复出现的失败模式：

1. **隐藏的假设** —— 模型做出错误假设并直接执行，不加检查，隐藏了困惑，也没有暴露权衡。
2. **过度工程化** —— 模型使代码过于复杂，膨胀抽象层，用 1000 行代码就能解决的问题却写成 1000 行。
3. **意外的副作用** —— 模型修改或删除了它们不完全理解的代码和注释，即使这些内容与当前任务无关。

---

## 四项原则

指南强调：

- 提前暴露假设和权衡，而不是默默做决定或隐藏困惑
- 最小可行代码，不包含任何超出请求范围的推测性功能、抽象或错误处理
- 精准、聚焦的编辑，仅触及必要内容，匹配现有代码风格，不改进相邻代码
- 将任务转化为可验证的目标，包含明确的成功标准和多步骤计划，从而实现独立的验证循环

更简洁地，四项原则是：

| 原则 | 核心理念 |
| --- | --- |
| **编码前思考** | 陈述假设，不确定时提问，行动前暴露权衡 |
| **简洁优先** | 编写解决问题的最小代码——不要推测性功能，不要额外抽象 |
| **精准修改** | 只触及必要部分；不要重构相邻的正常工作代码 |
| **目标驱动执行** | 提前定义成功标准；让代理根据目标自行验证输出 |

"目标驱动执行"原则特别体现了卡帕西的见解："LLM 非常擅长循环执行直到达成特定目标……不要告诉它该做什么，给它成功标准，然后看着它去做。"

---

## 什么是"元技能"？

`karpathy-guidelines` 技能被描述为一种**元技能**。它并不执行特定任务，而是约束助手处理*任何*任务的方式。这意味着它与任务特定的技能互补，不会产生冲突。

换言之，与告诉 Claude "如何编写提交信息"或"如何格式化报告"的技能不同，karpathy-guidelines 技能支配着 AI 在其所有其他操作中应用的**推理行为与自律**。它位于所有其他技能之上——因此称为"元"。

该技能坦诚地说明了其权衡：这些准则偏向于谨慎而非速度。对于简单任务，你可能希望助手直接行动。对于任何非平凡的任务，这种额外的自律会通过更小的差异和更少的意外来回报你。

---

## 指南生效的迹象

如果你看到以下情况，说明指南正在生效：

- 差异中不必要的更改更少——只出现要求的更改
- 由于过度复杂化而导致的重写更少——代码第一次就简单
- 澄清性问题出现在实现之前——而不是在犯错之后
- 简洁、最小的 PR——没有附带的重构或"改进"

---

## 更广阔的视角

`andrej-karpathy-skills` 仓库体现了卡帕西所谓的"想法文件"模式——分享想法而非实现。`CLAUDE.md` 文件不是任何人都能导入的库，而是一套任何人都可以改编的原则。这是一种新型的开源：不是开放代码，而是开放思想。

参考文献：

- [forrestchang/andrej-karpathy-skills — GitHub](https://github.com/forrestchang/andrej-karpathy-skills)
- [Karpathy's CLAUDE.md Skills File: The Complete Guide — Agentpedia](https://agentpedia.codes/blog/karpathy-claude-code-skills-guide)
- [Karpathy Guidelines: Keeping AI Assistants from Overthinking Your Code — Romain Lespinasse](https://www.romainlespinasse.dev/posts/karpathy-guidelines-skill/)
- [Andrej Karpathy's Claude Code Skills — Medium](https://medium.com/data-science-in-your-pocket/andrej-karpathys-claude-code-skills-3db42cc634c8)
