---
audio: false
generated: true
image: false
lang: en
layout: post
title: DigitalOcean Credits and GPU Promotion Guide
translated: false
type: note
---

**Question:** How does the DigitalOcean credits system work — specifically the AMD Dev Cloud GPU Promotion credits shown in the billing dashboard?

**Answer:**

This is straightforward billing mechanics:

**What you're seeing:**

| Field | Value | Meaning |
|---|---|---|
| Total Available | $99.97 | Credits usable against your next invoice |
| Promotion name | AMD Dev Cloud GPU Promotion | Likely a partnership/promo credit from AMD or DO |
| Expiration | June 26, 2026 | Credits expire ~25 days from now |
| Initial | $100.00 | You were granted $100 |
| Amount Remaining | $72.36 | You've burned ~$27.64 so far |

**How it works mechanically:**

1. When your monthly invoice is generated, DO automatically applies available credits before charging your payment method
2. Credits are consumed in FIFO order (oldest expiring first)
3. The $99.97 shown as "total available" = $72.36 remaining promo + any other small credits (maybe $27.61 from a referral or other source — explains the $99.97 vs $72.36 discrepancy)

**The math that matters for you:**

- You've spent ~$27.64 of the promo → at ~$2/hr for MI300X, that's ~**13.8 hours** of GPU time used
- $72.36 remaining → ~**36 hours left** on the promo credit
- Promo expires June 26 — you have **25 days** but only ~36 billable hours before it runs on your card

**Action items:**

```bash
# Check your current droplet/GPU spend rate
# DigitalOcean API — list current resources
curl -X GET "https://api.digitalocean.com/v2/droplets" \
  -H "Authorization: Bearer $DO_TOKEN" | jq '.droplets[] | {name, size, status}'
```

- If you have training runs queued, **front-load them before June 26**
- Don't let idle GPU droplets burn credits — make sure nothing is running when you're not using it
- $72.36 at $2/hr = budget for a focused sprint (fine-tuning run, GPT-2 experiment, etc.)