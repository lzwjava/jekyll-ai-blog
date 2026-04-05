---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 智能化人工智能迁移项目工作流
translated: true
type: note
---

**问题：** 对于复杂的智能体任务，使用 OpenClaw 搭配 MiniMax M2.7，并在遇到困难决策时通过网页聊天转用 Claude Sonnet 4.6，这是个好主意吗？具体针对一个 PHP 7.x → PHP 8.x 和 CodeIgniter 3 → 4 的迁移项目——用廉价的中国模型处理执行，而用 Claude 处理关键架构决策？

**答案：**

## 简短回答：是的——这是一个聪明的分层工作流

你的直觉是正确的。这本质上是一种 **"廉价模型负责执行，智能模型负责决策"** 的模式，并且与专业工程团队在 2026 年越来越多地构建 AI 辅助工作流的方式非常吻合。

---

## 理解技术栈

### OpenClaw + MiniMax M2.7

MiniMax M2.7 构建于 OpenClaw 智能体框架之上，在训练期间自主运行了超过 100 轮的脚手架优化，实现了 30% 的性能提升——全程无需人工干预。

M2.7 的成本为每百万输入令牌 0.30 美元，每百万输出令牌 1.20 美元，该公司声称其在同等智能水平下的运行成本不到 GLM-5 的三分之一。

在 MiniMax 自家的 MMClaw 评估（涵盖工作和生活中的真实任务）中，M2.7 达到了 62.7% 的准确率，接近 Claude Sonnet 4.6 的水平。

OpenClaw 支持隔离的智能体工作空间、工具调用、图像处理以及跨消息应用的智能体路由，专为编码智能体、个人助理和能无缝切换模型的多智能体团队而构建。

因此，对于 **常规、重复的迁移工作**（逐文件重构、样板化的命名空间更改、语法替换），在 OpenClaw 中运行的 M2.7 能力很强且极具成本效益。

---

### 使用 Claude Sonnet 4.6 处理困难决策

这正是你的工作流的亮点所在。Claude Sonnet 4.6 更擅长处理：

- **架构决策**（例如，如何重构一个遗留的“上帝类”控制器）
- **模糊的迁移权衡**（例如，是使用 CI4 的 Model 还是引入 Repository 模式）
- **安全敏感的逻辑**（CI3 和 CI4 之间在认证、会话、CSRF 处理方面的变化）
- **编写汇总的"上下文简报"**，然后你将其反馈给 OpenClaw

---

## 为什么这适用于 CI3→CI4 + PHP 7→8 的迁移

CodeIgniter 4 是框架的**重写**，不向后兼容。最好将其视为*转换*你的应用，而非*升级*。这意味着许多决策并非无关紧要，需要更深入的推理。

需要智能处理的关键破坏性变更：

- 模型现在必须位于 `app/Models` 目录，使用 `namespace App\Models` 和 `use CodeIgniter\Model` —— 用 `extends Model` 替换 `extends CI_Model`。
- 控制器移至 `app/Controllers` 目录，使用 `namespace App\Controllers` 和 `extends BaseController` 替换 `extends CI_Controller`。
- CI3 中存在的几个助手（Helper）在 CI4 中已不存在，包括 CAPTCHA 助手、Email 助手、Path 助手和 Smiley 助手。

这些正是需要 **Claude 进行推理决策** 的范畴，然后才能让 OpenClaw 执行成百上千的文件更改。

在 PHP 方面，你需要处理已弃用的函数（如 `create_function()`、`each()`），修改函数签名以适应更严格的类型要求，并考虑使用 Rector 等工具来自动化部分重构工作。类似 Rector 的自动化任务非常适合 OpenClaw 中的 M2.7 —— 它可以运行并验证它们。但是*决定哪些类型转换是安全的*则属于 Claude 的范畴。

---

## 推荐的工作流模式

以下是实施你想法的操作方式：

**阶段 1 — 决策层（通过网页聊天使用 Claude Sonnet 4.6）**
- 向 Claude 提供**模块摘要**（非整个代码库），并询问该模块的迁移策略
- 让 Claude 输出一个**结构化的指令简报**："以下是 5 个关键决策，以下是每个控制器/模型应遵循的模式"
- 对于模糊的遗留模式，使用 Claude 的扩展思考 / 深度思考功能

**阶段 2 — 执行层（OpenClaw + M2.7）**
- 将指令简报作为智能体的操作上下文输入到 OpenClaw
- 让 M2.7 执行重复性的文件转换、命名空间替换和语法升级
- M2.7 在 40 项复杂技能上保持 97% 的技能遵从率（超过 2000 个令牌案例），这意味着它能可靠地遵循详细指令

**阶段 3 — 审查检查点（再次使用 Claude）**
- 当 M2.7 遇到模糊情况或生成无法编译的代码时，将该输出复制给 Claude
- 让 Claude 诊断并生成修正后的模式，然后恢复 OpenClaw 的工作

---

## 注意事项与风险

- **上下文碎片化**：当你在工具间复制摘要时，有丢失细微差别的风险。要谨慎决定传递给 Claude 的上下文内容——包含原始的 CI3 代码片段和 M2.7 的尝试结果。
- **M2.7 在边缘案例上可能产生幻觉**：即使使用强大的 AI 工具，自动迁移过程中也可能遗漏某些功能或细节。对生成的代码进行彻底的审查和测试至关重要。不要让 OpenClaw 直接提交到生产分支。
- **CI3→CI4 是一次完全重写**：一个业务逻辑简单的小型 CI3 应用可能在 2-4 周内迁移到 CI4，但复杂应用程序的完整重建可能需要 3-6 个月。设定切合实际的期望。
- **PHP 版本目标**：PHP 8.1 已于 2025 年 12 月 31 日终止支持。当前受支持的 PHP 版本是 8.2（支持至 2026 年 12 月）、8.3（支持至 2027 年 12 月）和 8.4（支持至 2028 年 12 月）。最低目标应为 PHP 8.2+，而不是 8.1。

---

## 总结性判断

| 层级 | 工具 | 用途 |
|---|---|---|
| 关键决策 | Claude Sonnet 4.6（网页聊天） | 架构、模式、模糊逻辑、安全性 |
| 执行 | OpenClaw + MiniMax M2.7 | 逐文件转换、样板代码、重复性重写 |
| 检查点 | Claude Sonnet 4.6 | 审查 M2.7 输出中失败或看起来有误的部分 |

这种分层方法——**顶层使用战略智能，底层使用廉价执行**——正是平衡大型迁移项目成本与质量的正确方式。只需在工具间切换时，对上下文简报保持严谨。

**参考文献：**

- [MiniMax M2.7 概述 — WaveSpeedAI](https://wavespeed.ai/blog/posts/minimax-m2-7-self-evolving-agent-model-features-benchmarks-2026/)
- [MiniMax M2.7 + OpenClaw 设置指南 — AllClaw](https://allclaw.org/blog/minimax-2.7-with-openclaw)
- [MiniMax M2.7 官方模型页面](https://www.minimax.io/models/text/m27)
- [MiniMax M2.7 新闻 — MiniMax](https://www.minimax.io/news/minimax-m27-en)
- [2026 年 CodeIgniter 3 迁移选项 — Pegotec](https://pegotec.net/still-running-codeigniter-3-your-options-in-2026/)
- [官方 CI4 升级指南](https://codeigniter4.github.io/userguide/installation/upgrade_4xx.html)
- [AI 辅助 CI 迁移案例研究 — Medium](https://medium.com/@lksudha/from-spaghetti-php-to-codeigniter-4-an-ai-assisted-migration-journey-293e5894dfa8)
- [PHP 7.4 → 8.x 迁移最佳实践](https://www.augustinfotech.com/blogs/upgrading-a-complex-website-from-php-7-4-to-php-8-x-a-canadian-case-study/)