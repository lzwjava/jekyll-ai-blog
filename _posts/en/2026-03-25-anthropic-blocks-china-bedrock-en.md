---
audio: false
generated: true
image: false
lang: en
layout: post
title: Anthropic Blocks Chinese Users on Bedrock
translated: false
type: note
---

Question: Are Anthropic models (Claude) banning Chinese users even on AWS Bedrock?

Answer:

Yes — **Anthropic restrictions also apply when using models through AWS Bedrock**, not just the direct API. This is why you see errors like:

> “Access to Anthropic models is not allowed from unsupported countries…”

### 1. Anthropic explicitly blocks China (even via AWS Bedrock)

Anthropic’s policy **prohibits access from China**, and AWS Bedrock customers must follow Anthropic’s end-user license terms.
An AWS spokesperson confirmed that Claude access is **not allowed in China via Bedrock or Anthropic API**. ([Voice of America][1])

This means:

* Direct Claude API → blocked
* Claude via AWS Bedrock → still blocked
* Claude via cloud resellers → still subject to restriction

### 2. They expanded restrictions further (not just IP location)

In 2025 policy updates, Anthropic **blocked Chinese-controlled companies globally**, even if hosted outside China. ([CRN Asia][2])

So restrictions can trigger by:

* IP location (China)
* billing account country
* company ownership (Chinese entity)
* suspicious routing/proxy

### 3. "Unsupported regions" list excludes China

Anthropic only enables Claude in specific countries; unsupported regions violate ToS and may be blocked. ([Anthropic][3])

This is why you get:

```
ValidationException: Access to Anthropic models is not allowed...
```

### 4. Why even Bedrock cannot bypass

Because Bedrock is only a **hosting layer**. The model provider (Anthropic) still enforces:

* export controls
* national security rules
* ToS country restrictions

AWS explicitly states **third-party model restrictions still apply**. ([Amazon Web Services, Inc.][4])

---

### 5. Practical implications

Typical behavior:

| Scenario                        | Result                    |
| ------------------------------- | ------------------------- |
| China IP + Bedrock              | ❌ blocked                 |
| Chinese AWS account             | ❌ often blocked           |
| Chinese company using US region | ❌ may still blocked       |
| US/EU AWS account               | ✅ works                   |
| Proxy/VPN                       | ⚠️ sometimes works, risky |

---

### 6. This is getting stricter in 2025–2026

Anthropic:

* blocked Chinese-linked firms
* tightened unsupported-region enforcement
* willing to lose revenue for compliance/security reasons ([www.ndtv.com][5])

So yes — **they are actively tightening access**.

---

### TL;DR

Yes.
Even on AWS Bedrock, **Anthropic blocks Chinese users**.
Bedrock does not bypass Anthropic regional restrictions.

---

If you're trying to use Claude via:

* Bedrock
* OpenRouter
* Cursor / Claude Code
* API

Tell me which one — I can explain which setups still work and which fail.

[1]: https://www.voanews.com/a/chinese-entities-turn-to-amazon-cloud-rivals-to-access-us-chips-ai/7754150.html?utm_source=chatgpt.com "Chinese entities turn to Amazon cloud, rivals to access US ..."
[2]: https://www.crnasia.com/news/2025/artificial-intelligence/anthropic-tightens-ai-access-rules?utm_source=chatgpt.com "Anthropic tightens AI access rules, targeting Chinese- ..."
[3]: https://www.anthropic.com/supported-countries?utm_source=chatgpt.com "Supported countries & regions"
[4]: https://aws.amazon.com/legal/bedrock/third-party-models/?utm_source=chatgpt.com "Serverless Third-Party Models on Amazon Bedrock - AWS"
[5]: https://www.ndtv.com/world-news/anthropic-blocks-ai-model-claude-access-for-firms-linked-to-chinese-communist-party-11143362?utm_source=chatgpt.com "Anthropic Blocks AI Access For Firms Linked To Chinese ..."