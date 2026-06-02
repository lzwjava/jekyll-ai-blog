---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Pro 与 Max 计划概览
translated: true
type: note
---

**Question:** Claude 的 Pro 和 Max 计划之间有什么区别？使用 Claude Code 是否需要 Pro 或 Max 订阅？

**Answer:**

## Claude 计划概览 (2026)

---

### Free Plan
Free plan 提供在 web、iOS、Android 和 desktop 上访问 Claude 的权限。用户可以生成 code，分析 text 和 images，创作 content 以及 search the web。然而，Free plan 不支持 Claude Code 访问 —— 你至少需要 Pro 订阅或 API credits 才能使用 Claude Code。

---

### Claude Pro — $20/月 (或按年计费 $17/月)

Pro 计划在按年订阅时每月费用为 $17（按月计费为 $20）。它包含了 Free plan 的所有功能，并新增了在 terminal 中访问 Claude Code、file creation 和 code execution 的权限，以及支持用于管理 documents 和 chats 的无限数量的 projects。Pro 用户还可以访问 research tools，连接 Google Workspace，使用远程 MCP connectors 集成其他工具，并能通过更多 Claude models 获得扩展的 reasoning 能力。

Pro 非常适合在中小规模 codebases 上工作的 developers、正在学习 Claude Code 的人，或者进行集中式 coding sessions 而非全天持续运行 Claude Code 的用户。Pro 的不足之处在于：如果你在大型 codebases 上工作、运行 Agent Teams workflows，或者每天将 Claude Code 作为主要 coding partner 使用 6 小时以上，你将会经常达到 session limits。

---

### Claude Max — $100/月 (5x 档位) 或 $200/月 (20x 档位)

Max 计划起步价为每人每月 $100，面向 power users。它包含 Pro 的所有功能，并提供相比 Pro 高出 5 倍或 20 倍的 usage 选择。Max 用户受益于更高的大型任务 output limits、跨对话的 persistent memory、Claude 新功能的 early access，以及在流量高峰时段的 priority access。

**Max $100/月 (5x 档位):**
Claude Max $100 提供对 Claude Sonnet 4.6 的访问，其 usage limits 比 Pro 高出 5 倍，此外还可以访问具有 1M context window 的 Claude Opus 4.6、agent teams (research preview) 和 adaptive thinking。它为所有任务提供更高的 output limits、Claude 高级功能的 early access，以及高流量期间的 priority access。

**Max $200/月 (20x 档位):**
Claude Max $200 提供对包括 Claude Opus 4.6 在内的所有 Claude models 的访问，其 usage limits 比 Pro 高出 20 倍。该计划能够处理涉及大型 projects 和复杂任务的 professional development，支持长时间 coding sessions 而不触发 limits，并能通过完整访问 Opus 4.6 来进行最前沿的 software engineering。

---

### Claude Code 是否需要 Pro 或 Max？

没有免费的 Claude Code 计划。你至少需要 Pro 订阅或 API credits 才能访问它。

Max 计划将 Claude desktop 和 mobile apps 以及 Claude Code 整合在一个订阅中，每节 session 的 usage 最高可达 Pro 的 20 倍。

---

### 总结表格

| Plan | Price | Usage | Claude Code | Opus Access |
|---|---|---|---|---|
| Free | $0 | Baseline | ❌ | ❌ |
| Pro | $20/mo | 5x Free | ✅ | ❌ |
| Max 5x | $100/mo | 5x Pro | ✅ | ✅ |
| Max 20x | $200/mo | 20x Pro | ✅ | ✅ (full) |

**结论：** Pro 是使用 Claude Code 的最低要求，适合大多数个人 developers。Max 则专为需要极高 usage、Opus model 访问权限或全天运行 agentic/multi-agent workflows 的 power users 设计。

**References:**

- [Claude Official Pricing Page](https://claude.com/pricing)
- [Claude Max Plan Details](https://claude.com/pricing/max)
- [Claude Code Pricing Breakdown – SSD Nodes](https://www.ssdnodes.com/blog/claude-code-pricing-in-2026-every-plan-explained-pro-max-api-teams/)
- [Claude Pricing 2026 – Finout](https://www.finout.io/blog/claude-pricing-in-2026-for-individuals-organizations-and-developers)
- [Claude Max Plan Explained – IntuitionLabs](https://intuitionlabs.ai/articles/claude-max-plan-pricing-usage-limits)
