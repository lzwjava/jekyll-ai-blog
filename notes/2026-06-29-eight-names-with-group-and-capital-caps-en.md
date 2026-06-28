---
audio: false
generated: true
image: false
lang: en
layout: post
title: Eight Names with Group and Capital Caps
translated: false
type: note
---

The instrument list now has 8 names:

| Symbol | Name         | Strategy          | Period     | Group     |
| ------ | ------------ | ----------------- | ---------- | --------- |
| AAPL   | Apple        | mean_reversion    | DAY        | risk_on   |
| INTC   | Intel        | mean_reversion    | DAY        | risk_on   |
| AVGO   | Broadcom     | mean_reversion    | DAY        | risk_on   |
| GOOGL  | Alphabet     | mean_reversion    | DAY        | risk_on   |
| PDD    | PDD Holdings | mean_reversion    | DAY        | china     |
| NVDA   | Nvidia       | momentum_breakout | ONE_HOUR   | risk_on   |
| GLD    | Gold         | trend_following   | FOUR_HOURS | commodity |
| USO    | Crude Oil    | trend_following   | FOUR_HOURS | commodity |

Two things worth flagging:

1. **Group cap interaction.** `risk_on` now holds 5 names (AAPL, INTC, AVGO, GOOGL, NVDA) but `MAX_GROUP_POSITIONS = 2`, so the bot will hold **at most 2 risk_on positions at once** — the correlation filter will skip the rest. That's by design (avoids piling into correlated big-tech), but with 5 candidates competing for 2 slots, any individual name trades less often. PDD in its own `china` group gets a dedicated slot. If you'd rather give big-tech more room, bump `MAX_GROUP_POSITIONS` to 3.

2. **Capital.** On a ~$2k account, `entry_quantity` is also capped by free cash (`AVAILABLE_FUNDS_BUFFER`), so realistically only a couple of these can be funded at a time anyway — the group cap rarely becomes the binding constraint.

Both edits (daily timeframes + 3 new symbols) are still **uncommitted**. Want me to commit them together, and push so the next scheduled run picks them up?
