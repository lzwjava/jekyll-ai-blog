---
audio: false
generated: true
image: false
lang: en
layout: post
title: MiMo Token Plan Credits and Pricing
translated: false
type: note
---

**Question:** What does the Xiaomi MiMo Token Plan subscription page say? (Full breakdown of Credits, pricing, and model consumption ratios.)

**Answer:**

The actual doc is much more detailed than my previous answer. Here's the real picture:

---

## 1 Credit ≠ 1 Token

Credits are deducted per token, but each model consumes a different number of Credits per token. The exact table is:

| Model | Input (cache hit) | Input (cache miss) | Output |
|---|---|---|---|
| mimo-v2.5-pro | 2.5 Credits/token | 300 Credits/token | 600 Credits/token |
| mimo-v2.5 | 2 Credits/token | 100 Credits/token | 200 Credits/token |
| mimo-v2-pro | 140 Credits/token | 700 Credits/token | 2100 Credits/token |
| mimo-v2-omni | 56 Credits/token | 280 Credits/token | 1400 Credits/token |
| TTS series | free (limited time) | free | free |

So **1 Credit ≠ 1 token** — it's the opposite: **1 token costs hundreds of Credits** for uncached input, or just a few Credits if it's a cache hit. Credits are a fine-grained internal accounting unit, not a 1:1 token alias.

---

## Plan Pricing & Credit Quotas

**Monthly plans:**

| Plan | Price | Monthly Credits |
|---|---|---|
| Lite | $6/mo, ¥39/mo | 4.1B Credits |
| Standard | $16/mo, ¥99/mo | 11B Credits |
| Pro | $50/mo, ¥329/mo | 38B Credits |
| Max | $100/mo, ¥659/mo | 82B Credits |

---

## Practical Example

If you subscribe to Lite (4.1B Credits) and use 10M uncached input tokens on mimo-v2.5-pro, that costs 3,000M Credits (10M × 300), leaving 1,100M Credits — equivalent to roughly 5.5M uncached input tokens on mimo-v2.5 (at 200 Credits/output token).

---

## Key Notes

- **Night discount:** 0.8× consumption multiplier during off-peak hours (Beijing time 00:00–08:00).
- **Quota exhausted:** Service stops; it won't fall back to your balance or bonus credits.
- **Token Plan API keys** use `tp-xxxxx` format, distinct from regular pay-as-you-go `sk-xxxxx` keys.
- **Anthropic-compatible endpoint** available: e.g. `https://token-plan-sgp.xiaomimimo.com/anthropic` — so you can point Claude Code directly at MiMo.

**Important restriction:** Token Plan quota can only be used inside coding tools (OpenClaw, OpenCode, Claude Code, etc.). Using the API key for automation scripts or custom app backends outside coding scenarios is considered a violation and can result in suspension.

---

**References:**

- [MiMo Token Plan Subscription Docs (zh-CN)](https://platform.xiaomimimo.com/docs/zh-CN/price/tokenplan/subscription)
