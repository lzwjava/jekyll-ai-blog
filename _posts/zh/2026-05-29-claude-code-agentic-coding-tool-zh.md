---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code 智能代理编程工具
translated: true
type: note
---

**问题：** https://claude.com/product/claude-code 是什么？

**回答：**

这是 **Claude Code** 的官方产品页面——Anthropic 的智能编码工具。以下是与你相关的简要说明：

**它是什么：** 一个终端优先的 AI 编码智能体，直接在你的代码库中操作。不是聊天助手——它是一个能自动读取文件、运行命令、编写代码并创建 PR 的智能体。

**安装：**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**运行环境：**
- 终端（主要）
- VS Code / JetBrains IDE 扩展
- 桌面应用（并行任务管理、可视化差异对比）
- Web 端（`claude.ai/code`）
- Slack（发起任务，获取 PR 结果）
- 移动端 → 委托给你的本地机器（研究预览版）

**关键能力：**
- 智能代码库搜索——无需手动选择上下文文件，它自己就能找出相关代码
- 多文件协调编辑
- 完整的 GitHub/GitLab 工作流：读取 issue → 编写代码 → 运行测试 → 创建 PR
- 运行你的测试套件和构建系统
- 可通过 `CLAUDE.md` 文件配置；也可通过 SDK 或 GitHub Actions 进行脚本化

**所用模型：** Sonnet 4.6 和 Opus 4.7（根据页面上的定价表——注意 Opus 4.7 似乎是这里列出的较新模型）。

**定价：**
- 包含在 **Pro**（$17/月）中——有限使用，适合小型代码库
- **Max 5x**（$100/月）——在大型代码库中日常使用
- **Max 20x**（$200/月）——高级用户层级

**近期值得关注的功能（2026 年）：**
- **Routines**——定时任务，可通过 API 或事件触发（2026 年 4 月）
- **Auto mode**——比 `--dangerously-skip-permissions` 更安全的长时间运行替代方案（2026 年 3 月）
- 重新设计的桌面应用，支持并行任务管理（2026 年 4 月）

**对你而言：** 鉴于你的终端优先工作流和 AI 工程方向，Claude Code 是你自定义 CLI 智能体（如 `ww`、`zz` 等）的直接竞争对手/补充。值得在你的 MacBook Air 上运行它来处理日常编码任务。对你来说有趣的点是研究它如何处理智能循环——它是你正在构建的工具使用 + 规划架构的生产级范例。`CLAUDE.md` 配置系统也值得探索，用于项目级上下文注入。

**参考链接：**

- [Claude Code 产品页面](https://claude.com/product/claude-code)
- [Claude Code 文档](https://code.claude.com/docs/en/overview)
- [智能编码介绍](https://claude.com/blog/introduction-to-agentic-coding)