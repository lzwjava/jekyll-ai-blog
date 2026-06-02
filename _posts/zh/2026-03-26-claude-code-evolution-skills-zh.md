---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code 技能的演变
translated: true
type: note
---

问题：Claude Code 中 “skills” 的历史是什么？

回答：

Claude Code 的 **Skills** 系统经历了**三个主要阶段**：隐藏的内部能力 → 社区黑客行为 (Superpowers) → 官方平台功能。

---

# 阶段 0 — Skills 出现之前 (Prompt-only 时代)

**时间：** 早期 Claude Code (≈ v1.0)
Claude Code 最初纯粹通过 prompts 工作：

* 你告诉它做什么
* 它直接生成 code
* 没有可重用的 behaviors
* 没有持久的 workflows

这导致了：

* 不一致的 formats
* 缺乏标准的 engineering process
* 每个任务都需要重复进行 prompting

因此，用户开始手动构建 **structured prompts**。

---

# 阶段 1 — 发现隐藏的内部 “skills”

开发者注意到 Claude Code 已经对 skill 文件有了**未公开的支持**。

一篇描述该发现的博客指出：

* Claude Code 拥有一个**隐藏的 skills 系统**
* 支持 `SKILL.md` 文件
* 可能早在 **Claude Code 1.0** 时就已经存在
* 但尚未正式记录到文档中 ([blog.fsck.com][1])

这意味着：

> Skills 在正式发布之前就已经在内部存在了。

---

# 阶段 2 — 社区构建的 skills (Superpowers 时代)

在官方发布之前，开发者创建了自己的系统。

其中最具影响力的是：

* Superpowers
* 由 Jesse Vincent 创建
* 实现了 skill loading
* 结构化的 workflows
* multi-agent 开发

早期的安装方式比较原始：

* 获取 `SKILL.md`
* 修改 `~/.claude/CLAUDE.md`
* 教会 Claude 手动加载 skills ([blog.fsck.com][2])

这一时期引入了：

* brainstorming skill
* TDD skill
* code review skill
* debugging skill
* git workflow skill

这基本上发明了 **Claude skill-based programming**。

---

# 阶段 3 — 官方 Anthropic Skills 发布 (2025 年 10 月)

Anthropic 正式发布了 **Claude Skills**：

* 可重用的 modules
* 自动触发的 behaviors
* 自定义 workflows
* 在 Claude App 和 API 之间共享 ([The Verge][3])

Skills 变成了：

* 基于 folder 的
* `Skill.md`
* metadata + instructions
* 可选的 scripts

它们的功能类似于：

> Claude 内部的 mini-agents

---

# 阶段 4 — Plugin + marketplace 生态系统

官方发布后：

* skills 目录
* skill marketplaces
* 自动激活的 skills
* 企业级 skills
* 社区库

例如：

* 超过 200 个可用的 skills
* UI design skills
* PDF skills
* coding skills
* workflow skills ([Claude Code Agents][4])

Skills 变得：

* 可组合 (composable)
* 可共享
* 具有版本控制
* 自动检测

---

# 阶段 5 — Superpowers 成为官方插件 (2026 年)

Superpowers 后来成为了：

* 官方 marketplace 插件
* 结构化的 dev workflow
* multi-agent coding
* TDD 强制执行管道 ([Pasquale Pillitteri][5])

现在 skills 被用于：

* 规划 (planning)
* 编码 (coding)
* 测试 (testing)
* 评审 (reviewing)
* 合并 (merging)

---

# 最终演进时间线

```
Prompt-only Claude
        ↓
隐藏的 skill 支持 (未记录)
        ↓
社区黑客行为 (Superpowers SKILL.md)
        ↓
官方 Skills 发布 (Anthropic)
        ↓
Plugin 生态系统
        ↓
自动触发的 agent workflows (现状)
```

---

# 为什么 Skills 很重要

Skills 将 Claude Code 从以下状态改变：

之前：

```
Prompt → code
```

之后：

```
Prompt → skill → workflow → subagents → code
```

这就是为什么现代 Claude Code 感觉像：

* 资深工程师 (senior engineer)
* 而非自动补全 (autocomplete)
* 结构化开发工具 (structured developer)

---

# 核心见解

Skills = **可重用的 agent behaviors**

它们是：

* prompt templates
* 执行计划 (execution plans)
* 开发方法论 (development methodology)
* mini AI agents

---

参考文献：

* [https://blog.fsck.com/2025/10/16/skills-for-claude/](https://blog.fsck.com/2025/10/16/skills-for-claude/)
* [https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents](https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents)
* [https://www.tomsguide.com/ai/claude-just-got-customizable-skills-heres-how-they-could-supercharge-your-workflow](https://www.tomsguide.com/ai/claude-just-got-customizable-skills-heres-how-they-could-supercharge-your-workflow)
* [https://blog.fsck.com/2025/10/27/skills-for-openai-codex/](https://blog.fsck.com/2025/10/27/skills-for-openai-codex/)
* [https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide](https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide)

[1]: https://blog.fsck.com/2025/10/16/skills-for-claude/?utm_source=chatgpt.com "Skills for Claude!"
[2]: https://blog.fsck.com/2025/10/27/skills-for-openai-codex/?utm_source=chatgpt.com "Porting Skills (and Superpowers) to OpenAI Codex"
[3]: https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents?utm_source=chatgpt.com "Anthropic 用 'skills' 让 Claude 在工作中更实用"
[4]: https://www.claudecodeagents.com/skills?utm_source=chatgpt.com "175 个 Claude Code 自动激活技能 | 触发词 | Claude Code Agents"
[5]: https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide?utm_source=chatgpt.com "Claude Code 的 Superpowers：2026 完整指南"
