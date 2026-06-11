---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Copilot Moves to Token Billing
translated: false
type: note
---

**Question:** Did GitHub Copilot change its pricing model to charge by tokens now?

**Answer:**

Yes — this just went live. All GitHub Copilot plans transitioned to usage-based billing on June 1, 2026. Instead of counting premium requests, every plan now includes a monthly allotment of GitHub AI Credits, and usage is calculated based on token consumption — input, output, and cached tokens — at the listed API rates for each model.

How the mechanics work:

- Each token is priced per the model used, and the total converts to AI Credits at 1 credit = $0.01 USD. Each paid plan includes a monthly credit allowance equal to its price — Pro at $10/month includes $10 in credits; Pro+ at $39/month includes $39 in credits, with overage purchasable on top.
- **What's still free:** Code completions and Next Edit Suggestions remain free under all plans. The billing change only affects credits consumed by chat, agentic features, agent mode, and code review. If autocomplete is your main use, nothing changes.
- **What's gone:** The ceiling. Previously heavy usage was bounded by the flat fee; now there's no ceiling unless you explicitly set a spending limit, and by default GitHub only notifies you when a limit is hit rather than stopping usage. The fallback model has also been removed.
- **Hidden second meter:** Copilot code review now runs on GitHub Actions, so reviewing a PR consumes both AI Credits and your included Actions minutes.
- **Annual plans:** Annual Pro/Pro+ subscribers stay on premium-request pricing until expiry, but model multipliers increased on June 1 for them; at expiration they drop to Copilot Free unless they upgrade to a monthly plan.

Model rates (per 1M tokens, examples): Claude Haiku 4.5 is cheapest at $1 input / $5 output; Claude Opus is most expensive at $5 input / $25 output; GPT-5.4 nano is $0.2 input / $1.25 output, GPT-5.5 is $5 input / $30 output.

The community reaction has been brutal: developers running agentic sessions project cost increases of 10x to 50x, and reports of bills jumping from $29 to $750/month are spreading across Reddit, X, and GitHub's own discussions. Worth noting the why: internal Microsoft documents reported by Ed Zitron showed Copilot's week-over-week running cost had nearly doubled since January 2026 — agentic workloads broke the flat-rate economics, same story as Cursor's repricing last year.

**Practical takeaway for you:** Given your ~1B tokens/month consumption profile, Copilot's $10–$39 included credits would evaporate in hours of agentic work. At these per-token rates you're effectively paying API prices plus a subscription wrapper — OpenRouter with deepseek-v4-flash/mimo-2.5-pro, or a Claude Code subscription with its own caps, will be dramatically cheaper for agentic loops. Copilot only stays rational if you use it purely for free autocomplete and route all chat/agent traffic through your own keys.

**References:**

- [GitHub Copilot is moving to usage-based billing — GitHub Blog](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)
- [GitHub Copilot Token Billing 2026: Full Cost Guide — DEV Community](https://dev.to/akaranjkar08/github-copilot-token-billing-2026-full-cost-guide-and-alternatives-3bcf)
- ['What a joke': Copilot's new token-based billing spurs consternation — TechCrunch](https://techcrunch.com/2026/05/30/what-a-joke-github-copilots-new-token-based-billing-spurs-consternation-among-devs/)
- [Community discussion #192948 — GitHub](https://github.com/orgs/community/discussions/192948)
