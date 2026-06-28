---
audio: false
generated: true
image: false
lang: en
layout: post
title: Strategy vs. PDT Mismatch
translated: false
type: note
---

I've reviewed the GitHub Actions logs and the bot code. Here's the diagnosis.

## The Action itself is fine

Every run is **green/success**. The bot logs into Tiger, checks the market, and manages positions correctly. There's no crash and no error. So "it doesn't work" isn't a CI failure — it's the *trading behavior*.

## What actually happened to your "available assets"

Tracing the in-session runs on June 26:

| Time (UTC)        | Equity  | Available funds | Positions                                    |
| ----------------- | ------- | --------------- | -------------------------------------------- |
| 13:47 first entry | 2078.64 | **2012.87**     | NVDA only                                    |
| 14:43 onward      | ~2083   | **~1644**       | INTC + NVDA                                  |
| June 28 recap     | 2076.54 | —               | INTC 4@128.09 (−1.89), NVDA 1@198.60 (−5.89) |

So available funds dropped ~**$370** in one step — that's the bot **buying 4 INTC @ 127.345 (~$509 notional)** at 13:47. That drop is *expected*: deploying cash into a position reduces free cash. It's not a leak or a bug. Equity (net liquidation) is basically flat (~2078), just bleeding a few dollars from the two positions sitting at small unrealized losses during a weak tech tape (the LLM brief itself notes "tech sector losing ~5%").

## The real flaw: the strategy is structurally hamstrung by PDT

This is the thing worth fixing. Look at run `28253525557`:

```
INTC (mean_reversion, FIFTEEN_MINUTES): signal=exit, holding=True
  PDT guard: INTC was bought today, deferring exit to avoid a day trade (stop order still active)
```

- Your account is **~$2k, well under the $25k PDT threshold**, so you get ~3 day trades per rolling 5 days (`day trades remaining: 2`).
- But `AAPL`/`INTC` run **mean-reversion on 15-minute bars** — an *intraday* strategy that's supposed to buy a dip and sell back the same session.
- The PDT guard (`engine.py:84-88`, working as designed) **blocks that same-day exit**. So the bot opens an intraday position it is then *forbidden to close intraday*. When INTC's edge faded and it signaled EXIT, the bot couldn't act — it just held, and the only way out becomes the stop-loss or carrying it overnight.

That's the mismatch: **a fast intraday strategy running on an account that legally can't day-trade.** The bot mechanically "works," but the edge evaporates because it can't round-trip. Equity slowly bleeds as deferred losers ride down to their stops.

## What to do about it

The cleanest fixes, in order of impact:

1. **Match timeframes to a swing horizon.** Move `AAPL`/`INTC` mean-reversion off `FIFTEEN_MINUTES` to daily bars (`config.py:27-30`). Entries and exits then naturally span multiple days, so they're *not* day trades and the PDT guard never fires. This aligns the strategy with what the account is allowed to do.
2. **Or fund the account above $25k** to remove the PDT restriction entirely (then the 15-min strategy can actually exit when it wants).
3. **Or switch to a cash account** (no PDT rule, but you trade settled cash only — T+1 settlement limits churn instead).

My recommendation is **#1** — it's a config-only change, costs nothing, and makes the existing logic coherent. Want me to make that change (move the two mean-reversion names to daily bars)?

I haven't touched any code — this is review only. Let me know which direction you want.
