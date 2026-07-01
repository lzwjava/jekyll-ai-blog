---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copilot Premium Request Usage and API
translated: false
type: note
---

**Question:** For GitHub Copilot's 300 monthly premium requests, can we schedule premium usage on Mon/Wed/Fri and non-premium on Tue/Thu (giving ~30 requests per premium day), and does GitHub Copilot provide an API to query current premium request usage?

---

**Answer:**

## Your Scheduling Math — Is It Sound?

Your logic is reasonable in principle. Let's break it down:

- **300 premium requests / month**
- **Premium days:** Mon, Wed, Fri = 3 days/week × ~4 weeks = **12 premium days/month**
- **300 ÷ 12 = 25 requests per premium day** (not 30 — you used 3×4=12 correctly, but 300/12 = 25, not 30)

> Note: Some months have slightly more than 4 weeks (e.g. 5 Mondays), so it varies a bit. Budget ~25 to be safe.

The strategy itself is smart — unused requests do not carry over to the following month, so spacing out usage deliberately can help avoid burning through your quota early and then sitting idle for weeks.

On non-premium days (Tue/Thu), you can still use Copilot with one of the included base models (like GPT-4.1 or GPT-4o) without consuming premium requests, so the workflow still remains productive.

---

## Does GitHub Copilot Have an API to Query Premium Usage?

**Yes and No — it depends on your account type:**

### For Enterprise/Organization Admins ✅

GitHub provides REST API endpoints for Copilot metrics, accessible via `https://api.github.com/orgs/ORG/copilot/metrics`, requiring a PAT with `manage_billing:copilot`, `read:org`, or `read:enterprise` scopes.

Enterprise owners, billing managers, and authorized users can retrieve Copilot metrics reports via API, with historical data accessible for up to 1 year from the current date.

GitHub also announced: a dedicated API endpoint for premium request analytics data is being shipped, allowing users to build internal dashboards, create custom usage reports, and easily track expenses across teams.

### For Individual Users ❌ (Not Yet Officially Supported)

For individual GitHub Copilot subscribers, there is no supported public API to pull premium request usage in real time. VS Code can show usage in-product because it talks to GitHub's internal endpoints, but those aren't documented or guaranteed to be stable. The officially supported way for individual accounts is through the GitHub web UI under Settings → Billing → Copilot.

---

## Practical Ways to Monitor Usage Today

| Method | Who | How |
| --- | --- | --- |
| GitHub Web UI | Anyone | Settings → Billing → Copilot → Premium request analytics |
| Download CSV report | Enterprise admins | Billing & Licensing → Usage → Export |
| REST API (`/orgs/ORG/copilot/metrics`) | Org/Enterprise admins | Requires PAT token |
| VS Code status bar | Individual users | Shows real-time usage via internal endpoint |
| Third-party tool | Anyone with CSV | Tools like [github-copilot-usage-metrics-viewer](https://thomast1906.github.io/github-copilot-usage-metrics-viewer) visualize the exported CSV |

Also note: you can set budget alerts that notify you when you reach 75%, 90%, or 100% of your budget, which is a lightweight way to stay informed without polling an API.

---

## Summary

Your Mon/Wed/Fri rotation strategy is solid for budget pacing. The math gives you ~**25 premium requests per premium day** (not 30 — double-check). On non-premium days, falling back to included base models keeps the workflow going. For API-based monitoring, enterprise admins have full REST API access today; individual users currently rely on the GitHub UI or IDE status bar.

---

**References:**

- [GitHub Docs — Requests in GitHub Copilot](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)
- [GitHub Docs — Monitoring Copilot Usage and Entitlements](https://docs.github.com/copilot/how-tos/monitoring-your-copilot-usage-and-entitlements)
- [GitHub Docs — REST API Endpoints for Copilot Metrics](https://docs.github.com/en/rest/copilot/copilot-metrics)
- [GitHub Docs — REST API Endpoints for Copilot Usage Metrics (Enterprise)](https://docs.github.com/rest/copilot/copilot-usage-metrics)
- [Community Discussion — How to find premium request usage](https://github.com/orgs/community/discussions/157693)
- [Community Discussion — Supported endpoint for individual accounts](https://github.com/orgs/community/discussions/185848)
