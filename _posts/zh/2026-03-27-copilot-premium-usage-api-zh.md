---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot Premium 请求用量与 API
translated: true
type: note
---

**Question:** 对于 GitHub Copilot 每月 300 次的 premium requests，我们是否可以安排在周一/周三/周五使用 premium，周二/周四使用 non-premium（计划每个 premium day 使用约 30 次）？此外，GitHub Copilot 是否提供查询当前 premium request 使用情况的 API？

---

**Answer:**

## Your Scheduling Math — Is It Sound?

你的逻辑在原理上是合理的。让我们分解一下：

- **300 premium requests / 月**
- **Premium days:** 周一、周三、周五 = 3 天/周 × ~4 周 = **每月 12 个 premium days**
- **300 ÷ 12 = 每个 premium day 25 次 requests** （不是 30 次——你正确使用了 3×4=12，但 300/12 = 25，而不是 30）

> 注意：有些月份可能略多于 4 周（例如有 5 个周一），所以会有所波动。为了稳妥起见，建议按每天 ~25 次进行预算。

这个策略本身很聪明——未使用的 requests 不会结转到下个月，因此有意识地分散使用可以帮助避免过早消耗完配额而导致数周无 premium 可用的情况。

在 non-premium days（周二/周四），你仍然可以使用 Copilot 内置的 base models（如 GPT-4.1 或 GPT-4o），这些不会消耗 premium requests，因此 workflow 依然可以保持高效。

---

## Does GitHub Copilot Have an API to Query Premium Usage?

**Yes and No — 取决于你的账户类型：**

### For Enterprise/Organization Admins ✅

GitHub 为 Copilot metrics 提供了 REST API endpoints，可通过 `https://api.github.com/orgs/ORG/copilot/metrics` 访问，需要具有 `manage_billing:copilot`、`read:org` 或 `read:enterprise` 权限的 PAT。

Enterprise 管理员、billing managers 以及授权用户可以通过 API 获取 Copilot metrics 报告，历史数据最长可追溯至当前日期起 1 年。

GitHub 还宣布：正在推出专门用于 premium request analytics 数据的 API endpoint，允许用户构建内部 dashboards，创建自定义 usage reports，并轻松跟踪各团队的支出。

### For Individual Users ❌ (Not Yet Officially Supported)

对于个人 GitHub Copilot 订阅者，目前没有官方支持的公开 API 来实时获取 premium request 使用情况。VS Code 可以在产品内显示使用情况，因为它与 GitHub 的内部 endpoints 通信，但这些 endpoints 并未公开记录，且不保证稳定性。官方支持的个人账户查看方式是通过 GitHub 网页端的 Settings → Billing → Copilot。

---

## Practical Ways to Monitor Usage Today

| Method | Who | How |
|---|---|---|
| GitHub Web UI | 所有人 | Settings → Billing → Copilot → Premium request analytics |
| Download CSV report | Enterprise 管理员 | Billing & Licensing → Usage → Export |
| REST API (`/orgs/ORG/copilot/metrics`) | Org/Enterprise 管理员 | 需要 PAT token |
| VS Code status bar | 个人用户 | 通过内部 endpoint 显示实时使用量 |
| 第三方工具 | 任何拥有 CSV 的人 | 类似 [github-copilot-usage-metrics-viewer](https://thomast1906.github.io/github-copilot-usage-metrics-viewer) 的工具可以可视化导出的 CSV |

另外请注意：你可以设置 budget alerts，在达到预算的 75%、90% 或 100% 时通知你，这是一种无需轮询 API 即可获取信息的轻量化方式。

---

## Summary

你的周一/周三/周五轮换策略对于控制预算节奏是可靠的。计算结果显示你每个 premium day 大约有 **25 次 premium requests**（不是 30 次——请再次核对）。在 non-premium days，退回到包含在内的 base models 可以保持工作流的延续。对于基于 API 的监控，Enterprise 管理员目前拥有完整的 REST API 访问权限；个人用户目前仍需依赖 GitHub UI 或 IDE 状态栏。

---

**References:**

- [GitHub Docs — Requests in GitHub Copilot](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)
- [GitHub Docs — Monitoring Copilot Usage and Entitlements](https://docs.github.com/copilot/how-tos/monitoring-your-copilot-usage-and-entitlements)
- [GitHub Docs — REST API Endpoints for Copilot Metrics](https://docs.github.com/en/rest/copilot/copilot-metrics)
- [GitHub Docs — REST API Endpoints for Copilot Usage Metrics (Enterprise)](https://docs.github.com/rest/copilot/copilot-usage-metrics)
- [Community Discussion — How to find premium request usage](https://github.com/orgs/community/discussions/157693)
- [Community Discussion — Supported endpoint for individual accounts](https://github.com/orgs/community/discussions/185848)
