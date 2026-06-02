---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GitHub Actions定时任务采用UTC时间
translated: true
type: note
---

**GitHub Actions 定时工作流（使用 `on: schedule:` 触发器和 cron 语法）始终以 UTC（协调世界时）解析 cron 时间。**

工作流 YAML 中暂无原生支持直接指定其他时区的功能。若希望任务在特定本地时间（例如太平洋标准时间上午 9:00）运行，必须将其转换为对应的 UTC 时间并据此编写 cron 表达式。

### 官方文档核心要点：
- 定时工作流采用 POSIX cron 语法，在特定的 **UTC 时间** 运行。
- 示例：`cron: '0 5 * * *'` 表示每日 UTC 时间凌晨 5:00 运行（非本地时间）。

这一机制已持续多年且截至 2025 年末仍保持不变——`schedule` 事件暂未提供原生时区参数（这与 Dependabot 等 GitHub 其他功能有所不同）。

[触发工作流的事件 - GitHub 文档](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
[GitHub Actions 的工作流语法 - GitHub 文档](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#on-schedule)
