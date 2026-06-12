---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tiger Bot Dry Run Summary
translated: false
type: note
---

Everything is built and verified against your live Tiger account. Here's the summary:

## What I built

A `bot/` package implementing the post's architecture, on top of your existing Tiger setup:

| Market  | ETF proxy | Strategy                                                    | Timeframe |
| ------- | --------- | ----------------------------------------------------------- | --------- |
| S&P 500 | SPY       | mean reversion (z-score < −2 buy, exit at mean)             | 15-min    |
| Nasdaq  | QQQ       | mean reversion                                              | 15-min    |
| Bitcoin | IBIT      | momentum breakout (20-bar Donchian high in, 10-bar low out) | 1-hour    |
| Gold    | GLD       | trend following (SMA 20/50)                                 | 4-hour    |
| Oil     | USO       | trend following                                             | 4-hour    |

- **Risk layer** (`bot/risk.py`): ATR-based sizing so each trade risks exactly 1% of equity to its stop; every entry gets a **GTC stop order placed at the broker** (2 ATR below entry), so the stop holds even when the bot isn't running. Correlation filter caps the risk-on group (SPY/QQQ/IBIT) at 2 open longs.
- **Stateless engine** (`bot/engine.py`): broker positions are the source of truth — no local state file, safe to run from CI. Skips runs when the US market is closed.
- **Reports** (`bot/report.py`): `morning` (prices, ATR, strategy stance) and `evening` (equity, fills, unrealized PnL).
- **`.github/workflows/bot.yml`**: trade loop every 15 min during the US session, morning brief at 7am Beijing, evening recap at 9pm Beijing — reusing your existing `TIGER_*` secrets.

I verified all of it live: 13 synthetic-data signal/sizing/filter checks pass, and `morning`, `evening`, and the full signal path ran successfully against your real account (read-only — no orders were placed).

## Three things you need to know

1. **It's in dry-run mode.** It logs what it *would* trade and places nothing. To go live, set repository variable `BOT_DRY_RUN=0` (or locally `BOT_DRY_RUN=0 python run_bot.py run`). I'd watch dry-run output for at least a couple of weeks first.
2. **Your equity is $2,164, and SPY/QQQ won't fit.** One SPY share is ~$738 — 34% of your account, over the 25% notional cap — so the two mean-reversion instruments will always skip entries at this size. Fix by either funding the account, raising `MAX_POSITION_FRACTION` in `bot/config.py`, or swapping to the cheap share-class equivalents `SPLG` (~$87) and `QQQM` (~$245) — a one-line config change I can make if you want.
3. **The post is marketing.** Nobody's bot "easily earns a monthly salary in days" on $2k — at 1% risk per trade, a good week here is tens of dollars. The architecture is real and sound; the returns claim is not. There's also no backtest behind these parameters yet — that would be the most valuable next step before going live.

Changes are uncommitted; say the word if you want me to commit, swap in SPLG/QQQM, or build a backtest harness next.
