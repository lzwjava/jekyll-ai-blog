---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code 订阅与 API 选项
translated: true
type: note
---

Question: 使用 Claude Code CLI (npm tool) 的两种主要方式是什么 —— 是通过 Claude Pro/Max 订阅，还是通过 API access (包括官方 Anthropic API 和 AWS Bedrock)？

Answer:

你的理解基本正确。Claude Code (npm CLI tool) 支持 **三种计费/访问模式**，可以如你所述归纳为两大类：

---

## Category 1: Claude Subscription Plans (Pro / Max)

通过 Pro 和 Max 计划，你可以通过一个统一的订阅同时使用 web 端、桌面端、移动端 App 的 Claude **以及** 终端里的 Claude Code。

工作原理：你使用现有的 Claude 订阅通过浏览器登录来对 Claude Code 进行身份验证。无论 Claude Code 使用量多少，费用都是固定的月费，且使用额度与你的 web 端 claude.ai 使用量 **共享**。

Claude Code 可用的订阅层级：

- **Claude Pro** — $20/月，适度的 usage limits
- **Claude Max** — $100–$200/月，显著更高的 usage limits (Pro 的 5x–20x)

为了将使用严格保持在 Pro 或 Max 计划的配额内，你可以使用 `/status` 命令监控剩余配额。

---

## Category 2: API Access (Pay-as-you-go)

此类别有两个子选项：

### 2a. Anthropic's Direct API

当你在系统中设置 `ANTHROPIC_API_KEY` 环境变量时，Claude Code 会自动通过 API 计费路由请求，而不是使用你的订阅配额。价格按 token 计算 —— Sonnet 4.5 在标准 context 下的费用为每百万 input/output tokens $3.00/$15.00。

API 在使用透明度方面表现出色，提供详细的 token 追踪和成本明细。API 额度是专用的，不会占用你的 web 端使用配额。

### 2b. AWS Bedrock API

你可以在 Amazon Bedrock 上运行 Claude Code，利用 IAM 治理和统一计费将代码保留在 AWS 环境中。它涵盖了 AWS 认证选项（包括最新的 Bedrock API keys）、配置、model 选择以及在 Bedrock 上进行 agentic coding 的成本优化。

要启用它，需设置环境变量：

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
```

Bedrock 采用按量计费 (pay-as-you-go) —— 无席位费，无合同。你直接向 AWS 支付每 token 的价格。没有单独的 Anthropic 账单。

Bedrock 的主要优势包括：

- 统一计费：Claude Code 的使用情况将与 EC2、S3 等其他服务一起出现在你的 AWS 账单中。无需单独的供应商关系或支付方式。
- 集中访问控制：开发人员使用现有的 AWS IAM 或 IAM Identity Center (SSO) 进行身份验证，而无需管理单独的 API keys。

---

## Summary Table

| Method | Billing | Best For |
| --- | --- | --- |
| **Claude Pro** ($20/mo) | Fixed monthly | 轻度/日常个人使用 |
| **Claude Max** ($100–200/mo) | Fixed monthly | 重度日常开发 |
| **Anthropic API** | Pay-per-token | 可变的业务量，大 context 需求 |
| **AWS Bedrock** | Pay-per-token via AWS | 企业、合规性、AWS ecosystem |

一些开发人员使用混合方法：将订阅作为基础，但在特定的高 context-window 项目时切换到 API。

References:

- [Using Claude Code with your Pro or Max plan – Claude Help Center](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
- [Claude Code on Amazon Bedrock – Official Docs](https://code.claude.com/docs/en/amazon-bedrock)
- [Claude Code API vs Subscription – Usagebar Blog](https://usagebar.com/blog/claude-code-api-vs-subscription)
- [Claude, Claude API, and Claude Code: What's the Difference? – 16x Engineer](https://eval.16x.engineer/blog/claude-vs-claude-api-vs-claude-code)
- [Why and How to Run Claude Code with Amazon Bedrock – Medium](https://ndeplace.medium.com/why-and-how-to-run-claude-code-with-amazon-bedrock-28979c92098b)
