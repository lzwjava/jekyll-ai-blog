---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code 技能演进时间轴
translated: true
type: note
---

问题：Claude Code 中“skills”系统的时间线是什么，每个阶段的时间点又是什时候？

回答：

以下是 **Claude Code skills** 演进的**按时间顺序排列的时间线**，包括每个阶段的大致日期。

---

# 阶段 0 — 仅限 Prompt 的 Claude Code

**时间：** 2024 年初至中期
**状态：** 未开放 skills 系统

特点：

* 仅支持直接 prompting
* 没有可重用的 workflows
* 没有模块化行为
* 没有结构化的 engineering pipeline

典型用法：

```
Prompt → Claude → Code
```

局限性：

* 输出不一致
* 重复的说明指令
* 缺乏可重用的专业知识

---

# 阶段 1 — 隐藏的内部 skills 支持（未公开文档）

**时间：** 2024 年末（约 2024 年第四季度）

开发者发现：

* Claude Code 可以读取 **SKILL.md**
* 隐藏的模块化指令加载功能
* 内部可重用的 behaviors
* 官方未提供文档

这表明 **skills 在发布之前就已存在于内部**。

人们注意到的现象：

* 基于文件夹的指令可以生效
* Claude 自动重用 behavior
* skills 看起来像“mini agents”

---

# 阶段 2 — 社区 skills（Superpowers 时代）

**时间：** 2025 年初至中期

开发者创建了外部 skill 加载器，特别是：

* Superpowers
* 社区 skill 库
* 手动注入 Claude 配置

这引入了：

常见 skills：

* brainstorming
* code review
* TDD
* debugging
* git workflows
* verification

这是 **based-based development 开始流行**的时期。

Pipeline 变为：

```
Prompt → Skill → Claude → Code
```

---

# 阶段 3 — 官方 Claude Skills 发布

**时间：** 2025 年 10 月

Anthropic 正式推出了 **Claude Skills**：

特性：

* 可重用模块
* skill 文件夹
* metadata
* 自动激活
* 可共享的 skills

Skills 形式如下：

```
.skills/
  brainstorming/
  code-review/
  tdd/
```

Claude 能够：

* 检测 skills
* 自动选择 skills
* 链接 (chain) skills

这使 Claude 变成了 **workflow-based agent**。

---

# 阶段 4 — Skills 生态系统扩张

**时间：** 2025 年末（2025 年 11 月至 12 月）

出现的内容：

* skill 库
* skill 市场
* 团队共享的 skills
* domain skills
* UI skills
* infra skills

组织开始创建：

* 公司工程规范 skills
* release pipeline skills
* architecture skills

Claude 变为：

```
Agent runtime + skill modules
```

---

# 阶段 5 — 基于插件的 skills（Superpowers 集成）

**时间：** 2026 年初

Skills 演进为：

* 插件系统
* 可安装的 skill 包
* `/skills` 命令
* skill 发现机制
* skill metadata

示例（如你所见）：

```
Skills
14 skills

verification-before-completion
receiving-code-review
brainstorming
using-git-worktrees
```

现在的 skills 具有以下特点：

* 可安装
* 可组合
* 具有版本控制
* 由插件提供

---

# 完整时间线总结

```
2024 年初
仅限 Prompt 的 Claude Code
(无 skills)

2024 年末
发现隐藏的内部 skills

2025 年初
社区 skills (Superpowers)

2025 年 10 月
官方 Claude Skills 发布

2025 年末
Skills 生态系统增长

2026 年初
基于插件的 skills (/skills 命令)
```

---

# Claude Code 的演进

| 阶段 | 行为 |
| ---------- | -------------------------------------------- |
| 2024 | prompt → code |
| 2024 年末 | prompt → hidden skill → code |
| 2025 年初 | prompt → community skill → code |
| 2025 年 10 月 | prompt → official skill → workflow → code |
| 2026 | prompt → skill pipeline → multi-agent → code |

---

# 核心洞察

Skills 将 Claude Code 从：

```
code generator (代码生成器)
```

转变为：

```
workflow-driven AI engineer (工作流驱动的 AI 工程师)
```

这就是为什么现代 Claude Code 感觉更加结构化的原因。

---

参考资料：

* [https://blog.fsck.com/2025/10/16/skills-for-claude/](https://blog.fsck.com/2025/10/16/skills-for-claude/)
* [https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents](https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents)
* [https://www.tomsguide.com/ai/claude-just-got-customizable-skills-heres-how-they-could-supercharge-your-workflow](https://www.tomsguide.com/ai/claude-just-got-customizable-skills-heres-how-they-could-supercharge-your-workflow)
* [https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide](https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide)