---
audio: false
generated: true
image: false
lang: en
layout: post
title: Margin Trading Reality Check
translated: false
type: note
---

Here's your actual position — and it surfaces something important: **you're trading on margin already.**

|                               |                |
| ----------------------------- | -------------- |
| Net liquidation (your equity) | $2,164.68      |
| Positions value               | $3,867.20      |
| **Cash**                      | **−$1,703.05** |
| Available funds               | $674.79        |

Your AMD (2 shares, +$15.73) and NVDA (14 shares, +$34.78) together are worth $3,867 against $2,165 of equity — you've borrowed ~$1,703 from Tiger and are paying margin interest on it (typically 5–8%/yr, roughly $8–12/month at this size).

**Do you need to sell?** You don't *have* to — but here's the honest assessment:

1. **The bot doesn't require it to function.** You have $675 available, enough for its first one or two entries (~$300–550 each). But after that, new buys would dig deeper into margin debt.
2. **The bot currently sizes off net liquidation and doesn't check available funds** — so in live mode it could push your margin loan toward $3,000+ if several signals fire. That's a real gap I'd want to fix before you go live: add an available-funds check so it never increases margin debt. Say the word and I'll add it.
3. **The cleanest setup**: selling ~9 NVDA shares (~$1,850) would clear the negative cash, keep your AMD and 5 NVDA shares, stop the interest charges, and give the bot ~$1,800 of real cash to work with. Selling everything is only necessary if you want the bot to be the whole strategy.

My recommendation: decide how much of this account is "bot capital" vs. "your NVDA/AMD conviction trades," because right now they'd share one margin pool and amplify each other's risk. If you tell me which way you want to go, I can add the available-funds guard (and optionally a hard "never borrow" rule) before you flip to live.
