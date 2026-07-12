---
audio: false
generated: true
image: false
lang: en
layout: post
title: TRAE Work Unavailable in China
translated: false
type: note
---

Question: Why does TRAE Work show "Work Unavailable" for my region (Guangzhou/mainland China)?

Answer:

Two separate things are stacking up here, and it's worth knowing both since you'll run into the same pattern with other AI dev tools.

**1. TRAE has a hard domestic/international split**

ByteDance runs TRAE as two separate products under two separate entities:

- `trae.ai` — international version, targets overseas users, backed by GPT/Claude models
- `trae.com.cn` — domestic version for mainland China, uses DeepSeek-R1 and other domestic models

If you're hitting `trae.ai` (or its "TRAE Work" team product) from a mainland China IP, you get blocked/degraded — using the overseas version of Trae in China causes login and connectivity problems due to network congestion, and the fix most people use is routing through a VPN, or just switching to the domestic Trae.com.cn version which has a full Chinese interface. "TRAE Work" specifically is the newer B2B/team tier of the international product, so it's even more likely to be geofenced strictly by IP/billing region than the base IDE.

**2. Underlying model access is also getting squeezed**

Separate from ByteDance's own geofencing, there's a second-order problem: TRAE's overseas product is a downstream reseller of Anthropic and OpenAI models. Anthropic announced it would tighten access restrictions for entities more than 50% owned by companies headquartered in unsupported regions such as China, regardless of where the entity itself is located, and Trae — the ByteDance-built AI code editor for overseas users — is a known consumer of GPT and Claude models, which put users worried about losing Claude access. So even a fully "international" TRAE product sitting on ByteDance ownership is at risk of losing upstream model access independent of where you personally sit.

**What this means for your setup**

Since you're consulting internationally and building agent tooling anyway, I wouldn't lean on TRAE Work as critical infra — it sits at the intersection of two different regulatory fault lines (China outbound restriction + US model-provider inbound restriction), which is exactly the kind of dependency that can vanish overnight regardless of what you do right. If you want a ByteDance-model-quality coding agent with zero regional roulette, `trae.com.cn` (DeepSeek-R1 backed) is stable for you geographically. If you specifically want Claude/GPT-backed agentic coding, your own CLI agents (`ww`, `iclaw`, `zz`) hitting OpenRouter or direct API keys sidestep this whole class of problem — you already have the infra, no need to depend on a reseller's geofencing decisions.

References:

- [Supported countries and regions - TRAE Documentation](https://docs.trae.ai/ide/supported-countries-and-regions)
- [Why can't Trae work in China and how to fix it? - AI Sharing Circle](https://aisharenet.com/en/trae-guoneiweishenme/)
- [Tech war: Anthropic's Claude restrictions put overseas AI tools backed by China in limbo - SCMP](https://www.scmp.com/tech/tech-war/article/3324583/tech-war-anthropics-claude-restrictions-put-overseas-ai-tools-backed-china-limbo)
