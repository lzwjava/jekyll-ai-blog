---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 为协作安装Claude GitHub应用
translated: true
type: note
---

通过在 Claude Code（Anthropic 的 AI 驱动编程工具）中使用 `/install-github-app` 命令安装 Claude GitHub 应用，可实现与 GitHub 的无缝集成。这使您能够在 GitHub 议题或拉取请求的评论中直接提及 @claude，让 Claude 以“虚拟团队成员”的身份在 GitHub 界面内协助工作——包括回复反馈、修复错误或建议代码修改。该命令将引导您完成设置流程，包含使用 Claude Max 订阅账号登录及选择代码库。[1][2][3] 这一功能将 Claude 从终端工具转变为开发工作流中的活跃参与者，特别适合协同编程和 CI/CD 流水线场景。[3][4][5][6][7]

引用文献：
[1] <https://github.com/anthropics/claude-code-action>
[2] <https://www.reddit.com/r/ClaudeAI/comments/1kvabkk/use_claude_github_app_with_your_claude_max_w/>
[3] <https://github.com/apps/claude>
[4] <https://www.youtube.com/watch?v=0kJh4KuJ1nY>
[5] <https://apidog.com/blog/claude-code-github-actions/>
[6] <https://www.youtube.com/watch?v=FjHtZnjNEBU>
[7] <https://www.youtube.com/watch?v=L_WFEgry87M>
