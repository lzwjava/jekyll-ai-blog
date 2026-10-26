---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 测试工具与 DeepSeek 测试工具
translated: true
type: note
---

好问题，分两部分——它们其实是相关的。

---

**问题：** “harness”是什么意思？什么是 DeepSeek Harness (DSH)？

---

**回答：**

### 1. “Harness”——一般概念

在 LLM 领域，**harness** 是模型*周围*的一切，它把模型从文本预测器转变为一个真正的 agent。DeepSeek 自己的公式完美地概括了这一点：

> **模型 + Harness = Agent**

模型是“大脑”——它负责推理和生成文本。Harness 是“身体”——它给模型眼睛、双手和记忆。具体来说，harness 负责处理：读写文件、运行终端命令、浏览网页、管理对话会话、调用其他工具或 API、规划多步任务，以及连接 MCP 服务器。

没有 harness，LLM 就只是一个聊天窗口。有了 harness，它就变成了一个能够真正*做事*的 agent。

这就是为什么之前回答中的引言——*“2026 年是打磨 harness 的一年”*——意味着：模型本身并没有显著变得更聪明，而是它们周围的 scaffolding 有了很大改进，这让整个组合系统感觉像是一次巨大飞跃。

---

### 2. DeepSeek Harness (DSH)——具体产品

DSH (DeepSeek Harness) 是 DeepSeek 于 2026 年 8 月 13 日北京时间晚上 8:30 左右发布的开源 agent runtime，采用 MIT 许可证，使用 TypeScript 编写。它以 v0.1 开发者预览版的形式发布。

它是一个你可以安装并运行的程序——npm 包是 `@deepseek-ai/dsh`——它将你提供的任何模型（默认是 DeepSeek V4 Flash）连接到你的文件系统、终端、网络和其他 agent。

DSH 团队将模型描述为“Agent 的灵魂”，而 harness “赋予 Agent 理解其环境、使用工具并在现实场景中持续工作的能力”。DSH 采用“一切皆 plugin”的设计理念——model、tools、skills、sessions、sandbox、storage、loops、scheduling 和 UI 全部由可自由替换和重新组合的 plugins 构成。

该 monorepo 包含 49 个 packages——core、llm、mcp、sandbox、context、plan、goal 等——发布时包含 100 多个 first-party plugins，发布后 24 小时内 GitHub 上收集了 288 个社区 plugin repositories。

VentureBeat 将其定位为 Claude Code 的开源竞争对手。它与 DeepSeek V4-Pro 同一天发布，将模型和 harness 作为捆绑组合一起推出。

要安装并运行它：

```bash
npx @deepseek-ai/dsh web
```

**简而言之：** “Harness” = 让模型变成有用 agent 的 scaffolding。DSH = DeepSeek 开源的该类 scaffolding，是他们对标 Claude Code 的方案，于 2026 年 8 月发布。

**参考链接：**

- [DeepSeek Harness Explained — Orca Router](https://www.orcarouter.ai/blog/deepseek-harness-explained)
- [DSH Usage Guide — Orca Router](https://www.orcarouter.ai/ar/blog/deepseek-dsh-usage)
- [DeepSeek Harness 开放测试报道 — 澎湃新闻](https://m.thepaper.cn/newsDetail_forward_33783308)
- [DeepSeek Harness 深度解析 — 华为云社区](https://bbs.huaweicloud.com/blogs/485547)
