---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI API Proxy Channel Comparison Guide
translated: false
type: note
---

Question: What are the different AI model access channel groups shown in this service selection interface, and what do they mean?

Answer:

This appears to be a **third-party AI API proxy/aggregator platform** (likely a Chinese service reselling access to various AI models). The interface lists different "channels" or "groups" users can route their requests through, each with a **cost multiplier (倍率)**. Here is a breakdown of each group:

---

## Claude (Anthropic) Channels

| Group | Multiplier | Description |
|---|---|---|
| **Claude Max** | 1.3x | Best quality; uses Claude Max accounts |
| **Claude Max 备用 (Backup)** | 2.1x | Uses Max 20X accounts; costs spiked due to risk control, so temporarily higher rate |
| **AWS Bedrock** | 5x | Official Claude API via Amazon Web Services Bedrock — most stable but most expensive |
| **AWS Bedrock 低价 (Low Price)** | 2.6x | Same AWS Bedrock official channel, slightly less stable but cheaper |
| **CC-Azure** | 1.3x | Claude via Microsoft Azure cloud hosting |
| **CC-逆向渠道B (Reverse Channel B)** | 0.8x | Unofficial reverse-engineered proxy; supports Opus 4.6; quality comparable to Max |
| **CC-反重力逆向 (Anti-Gravity Reverse)** | 0.8x | Another unofficial reverse proxy channel |
| **kiro标准版 (Standard)** | 0.15x | Cheapest Claude option; does NOT support Opus model |
| **kiro企业版 (Enterprise)** | 0.4x | Supports Opus model; enterprise tier |
| **CC-TEST分组** | 0.15x | Test group — currently unavailable |
| **CC-其他逆向 (Other Reverse)** | 0.3x | Supports only Opus 4.5 and Haiku 4.5 — currently unavailable |

---

## OpenAI (GPT) Channels

| Group | Multiplier | Description |
|---|---|---|
| **Codex (Team)** | 0.3x | Uses GPT Team + regular account pool; lower priority than GPT Pro |
| **Codex (GPT Pro)** | 0.6x | Higher quality; supports all Codex models; GPT Pro account pool |

---

## Google Channels

| Group | Multiplier | Description |
|---|---|---|
| **gemini官方 (Gemini Official)** | 0.4x | Official Google Gemini API channel |

---

## Key Concepts Explained

**What is "倍率" (multiplier/rate)?**
This is a cost scaling factor relative to a base token price. A 5x rate means you pay 5× the base cost per token. A 0.15x rate means you pay only 15% of the base cost.

**What are "逆向渠道" (reverse channels)?**
These are **unofficial reverse-engineered proxies** — they intercept Claude's web interface traffic instead of using the official API. They are cheaper but:
- Less stable
- Potentially against Anthropic's Terms of Service
- May be blocked/rate-limited unpredictably (as seen with the "风控" risk control issue on the backup Max channel)

**What are "official channels" (AWS Bedrock, gemini官方, etc.)?**
These route through the **actual official enterprise APIs** of the respective providers, offering better stability, compliance, and reliability — but at a higher cost.

**Which channel is currently selected?**
The interface shows **Claude Max 备用 (Backup)** is currently selected (indicated by the checkmark ✓).