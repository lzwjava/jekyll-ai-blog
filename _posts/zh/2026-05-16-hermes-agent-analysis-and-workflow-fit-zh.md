---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯代理分析与工作流适配
translated: true
type: note
---

Question：你对 Hermes Agent 有何看法？包括它的特性、理念、与 Claude Code (CC) 的对比、与中国团队 EvoMap 的抄袭争议，以及它如何融入个人工作流（偏好开源、HuggingFace、中文模型如 GLM 和自定义 CLI 工具）？

Answer：

## Hermes Agent — 全面评估

### Hermes Agent 究竟是什么

Hermes Agent 是由 Nous Research 构建的开源自主 AI 智能体，于 2026 年 2 月发布。它不是绑定在 IDE 上的编码助手，也不是围绕单一 API 的聊天机器人封装——Hermes 运行在你的服务器上，能记住学到的内容，运行时间越长，能力越强。

它支持你想要的任何模型——Nous Portal、OpenRouter（200+ 模型）、z.ai/GLM、Kimi/Moonshot、MiniMax、Hugging Face、OpenAI 或你自己的端点。你可以通过 `hermes model` 切换模型，无需修改代码，没有锁定问题。这种多模型开放性对于你以 GLM + HuggingFace 为首的工作流来说，是最大的实际优势之一。

---

### 值得注意的关键特性

- **子智能体**：为并行工作流生成隔离的子智能体。通过 `execute_code` 进行程序化工具调用，将多步流水线压缩为单次推理调用。
- **持久记忆 + 自我改进技能**：智能体策展的记忆，带有定期提示；复杂任务后自动创建技能；技能在使用中自我改进。
- **平台覆盖**：在你所在的地方运行——CLI、Telegram、Discord、Slack、WhatsApp、Signal、Matrix、钉钉、飞书、企业微信等——从一个网关覆盖 20+ 平台。
- **`/goal` 命令**：最近新增，类似于 CC 的目标设定流程。
- **导出/复制功能**：对你将 AI 回复上传到博客的用例很有用——这些功能在最近的更新中添加。
- **Harness / trajectory 模式**：批量轨迹生成和轨迹压缩，用于训练下一代工具调用模型——从第一天起就为研究做好准备。这对于你微调的兴趣来说是一个差异化特性。

---

### Hermes 与 Claude Code (CC) — 主要差异

| 维度 | Hermes Agent | Claude Code |
|---|---|---|
| 许可证 | 完全开源 | 专有（部分泄露） |
| 模型锁定 | 任何兼容 OpenAI 的端点 | 仅限 Claude 模型 |
| 成本 | 自托管，几乎免费 | 通过中继/API 按 token 计费 |
| 记忆 | 持久，跨会话 | 每个会话重置 |
| 技能系统 | 开放标准（agentskills.io），自动生成 | 通过 CLAUDE.md / 手动配置 |
| 成熟度 | 约 3 个月（2026 年 2 月） | 约 1 年的实战测试 |
| 子智能体 | 有，内置 | 有，但较新 |

Hermes 在更新节奏上更具侵略性和创新性——每周发布，社区 PR。CC 在纯编码任务上仍然更可靠，这些任务需要最大上下文和工具精确度。

---

### 抄袭争议（EvoMap / Evolver）

这是真实的，值得清楚理解。深圳初创公司 EvoMap 指控 Hermes Agent 严重复制其自进化引擎 Evolver 的代码结构而未注明出处。根据 EvoMap 的说法，自进化架构和模块结构与 Evolver 惊人相似，而 Hermes 在其源代码或公开渠道中从未引用或致谢 Evolver。

引用的证据包括：一个 10 步主循环在两个项目之间一一对应，系统性地替换了 12 组核心术语，并且在七份公开材料中没有任何归属说明。

Nous Research 的官方账号最初回应说：“我们的仓库创建于 2025 年 7 月。我们是基础技术的先驱……删除你的账号。” 这一回应迅速引发公众抗议，随后被删除。

文章也承认对 Hermes 有利的事实：Hermes Agent 仓库创建于 2025 年 7 月——比 Evolver 早六个月——但直到 2026 年 2 月底才公开。Hermes 的自进化模块使用了来自斯坦福/伯克利的学术框架 GEPA（ICLR 2026 Oral），与 Evolver 的框架无关。两个项目使用不同的语言（JavaScript 与 Python），并且没有发现代码级别的复制。EvoMap 的论点基于概率推理——超过十个维度同时对齐超出了巧合范围。这一论点令人信服，但并非结论性。

一位评论员提出，抄袭可能并非有意为之，而是 AI 的产物——开发人员使用的 AI 辅助编码工具可能借鉴了开源项目来生成看起来全新的代码，变量名和文件结构已更改，但核心设计保持不变。

**关于此事的底线**：架构上的相似性是真实且有记录的。至于是有意抄袭、AI 辅助趋同，还是独立的并行开发，尚无定论。Nous Research 最初不屑一顾的回应（“删除你的账号”）损害了其在中立观察者中的信誉。作为用户，了解这一点同时仍使用该工具是合理的——这不会使 Hermes 功能失常，但反映了项目当时在道德上的不佳表现。

---

### 你的工作流适配评估

你本能地将 Hermes 用作 CC 的补充而非替代，这是有道理的：

- **通过 Hermes 使用 GLM + OpenRouter**：理想。模型切换无缝，这正是 Hermes 的设计初衷。
- **博客导出/复制功能**：对你的发布工作流有很好的实际适配。
- **Harness / trajectory 模式**：这是对你来说最被低估的特性。如果微调是优先事项，从你自己的智能体会话中生成高质量轨迹是有价值的训练数据。
- **自定义 CLI 技能（约 100 条命令的 `ww` 工具）**：你自己编写 200–300 行技能脚本的方法比依赖 Hermes 自动生成的技能更可维护和个性化。但两者并不互斥——Hermes 的技能可以补充你的 CLI，特别是对于你希望智能体自主处理的任务。
- **CamouFox 浏览器问题**：那很可能与早期 Hermes WebUI / PTY 兼容性有关。根据最近的更新，原生终端和 WebUI 已显著稳定。

---

### 总结评价

Hermes Agent 确实具有创新性——不仅仅是在现有工具基础上增量改进，而是在架构上不同，秉承“与你一起成长”的理念。多模型支持、子智能体委派、轨迹导出和持久记忆使其非常适合你的开源、以 HuggingFace 为中心、面向微调的工作流。抄袭争议是该项目的真实阴影，尽管技术上尚未解决。务实使用它：无论争议如何，它的能力是真实存在的。

参考来源：

- [Hermes Agent GitHub (NousResearch)](https://github.com/nousresearch/hermes-agent)
- [Hermes Agent 官方文档](https://hermes-agent.nousresearch.com/docs/)
- [Hermes Agent 主页](https://hermes-agent.org/)
- [EvoMap 抄袭指控 — 第一财经](https://www.yicaiglobal.com/news/chinese-ai-team-evomap-changes-ai-agents-license-after-accusing-silicon-valley-ai-lab-of-copying-code)
- [技术对比分析 — KuCoin News](https://www.kucoin.com/news/flash/evomap-accuses-hermes-agent-of-architectural-copying-nous-research-rebuts-73500)
- [36氪英文报道](https://eu.36kr.com/en/p/3767967755371011)
