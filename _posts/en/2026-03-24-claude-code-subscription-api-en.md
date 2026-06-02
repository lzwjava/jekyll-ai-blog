---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Subscription and API Options
translated: false
type: note
---

Question: What are the two main ways to use the Claude Code CLI (npm tool) — through a Claude Pro/Max subscription and through API access (including the official Anthropic API and AWS Bedrock)?

Answer:

You are essentially correct. Claude Code (the npm CLI tool) supports **three billing/access modes**, which can be grouped into two broad categories as you described:

---

## Category 1: Claude Subscription Plans (Pro / Max)

With Pro and Max plans, you have access to both Claude on the web, desktop, and mobile apps **and** Claude Code in your terminal with one unified subscription.

How it works: you use your existing Claude subscription to authenticate Claude Code through browser login. The cost is a fixed monthly fee regardless of Claude Code usage, and usage limits are **shared** with your web claude.ai usage.

Available subscription tiers for Claude Code:

- **Claude Pro** — $20/month, moderate usage limits
- **Claude Max** — $100–$200/month, significantly higher usage limits (5x–20x Pro)

To maintain usage strictly within your Pro or Max plan allocation, you can monitor your remaining allocation using the `/status` command.

---

## Category 2: API Access (Pay-as-you-go)

This category has two sub-options:

### 2a. Anthropic's Direct API

When you set an `ANTHROPIC_API_KEY` environment variable on your system, Claude Code automatically routes requests through API billing instead of your subscription allocation. Pricing is per-token — Sonnet 4.5 costs $3.00/$15.00 per million input/output tokens for standard context.

The API excels in usage transparency, providing detailed token tracking and cost breakdowns. API limits are dedicated and don't compete with your web usage quota.

### 2b. AWS Bedrock API

You can run Claude Code with Amazon Bedrock to keep your code within your AWS environment with IAM governance and unified billing. It covers AWS authentication options including the new Bedrock API keys, configuration, model selection, and cost optimization for agentic coding on Bedrock.

To enable it, you set environment variables:

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
```

Bedrock is pay-as-you-go — no seats, no contracts. You pay a single per-token price to AWS. There is no separate Anthropic bill.

Key benefits of Bedrock include:
- Unified billing: Claude Code usage appears in your AWS bill alongside EC2, S3, and other services. No separate vendor relationships or payment methods needed.
- Centralized access control: developers authenticate using your existing AWS IAM or IAM Identity Center (SSO) instead of managing separate API keys.

---

## Summary Table

| Method | Billing | Best For |
|---|---|---|
| **Claude Pro** ($20/mo) | Fixed monthly | Light/daily personal use |
| **Claude Max** ($100–200/mo) | Fixed monthly | Heavy daily development |
| **Anthropic API** | Pay-per-token | Variable workloads, large context needs |
| **AWS Bedrock** | Pay-per-token via AWS | Enterprise, compliance, AWS ecosystem |

Some developers use a hybrid approach: subscriptions as their baseline and switching to API for specific high-context-window projects.

References:

- [Using Claude Code with your Pro or Max plan – Claude Help Center](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
- [Claude Code on Amazon Bedrock – Official Docs](https://code.claude.com/docs/en/amazon-bedrock)
- [Claude Code API vs Subscription – Usagebar Blog](https://usagebar.com/blog/claude-code-api-vs-subscription)
- [Claude, Claude API, and Claude Code: What's the Difference? – 16x Engineer](https://eval.16x.engineer/blog/claude-vs-claude-api-vs-claude-code)
- [Why and How to Run Claude Code with Amazon Bedrock – Medium](https://ndeplace.medium.com/why-and-how-to-run-claude-code-with-amazon-bedrock-28979c92098b)
