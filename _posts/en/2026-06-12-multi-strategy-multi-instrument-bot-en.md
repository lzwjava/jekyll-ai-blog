---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Strategy Multi-Instrument Bot
translated: false
type: note
---

The bot is running three strategies across five instruments (all live as of tonight, configured in `bot/config.py`):

| Instrument        | Strategy          | Timeframe | Rules                                                                                                                      |
| ----------------- | ----------------- | --------- | -------------------------------------------------------------------------------------------------------------------------- |
| SPLG (S&P 500)    | Mean reversion    | 15-min    | Buy when price closes 2+ std devs below its 20-bar average (z-score ≤ −2); sell when it reverts to the mean (z ≥ 0)        |
| QQQM (Nasdaq 100) | Mean reversion    | 15-min    | Same z-score rules                                                                                                         |
| IBIT (Bitcoin)    | Momentum breakout | 1-hour    | Buy when price breaks above the prior 20-bar high (Donchian); sell when it breaks below the prior 10-bar low               |
| GLD (Gold)        | Trend following   | 4-hour    | Buy when the 20-bar SMA is above the 50-bar SMA and price is above the slow SMA; sell when the fast SMA crosses back under |
| USO (Oil)         | Trend following   | 4-hour    | Same SMA crossover rules                                                                                                   |

The logic behind the mix: indices chop around a mean intraday so you fade their overextensions; bitcoin trends hard so you ride breakouts instead of fading them; commodities move in slower waves so a 4-hour SMA crossover filters out intraday noise.

On top of all three sits one shared risk layer:

- **Sizing**: each entry risks 1% of equity to its stop, where the stop is 2 ATR (14-bar) below entry — so quieter instruments get bigger size, volatile ones smaller.
- **Hard stop**: every entry immediately gets a GTC stop order at the broker, so the 1% cap holds even if the bot isn't running.
- **Correlation filter**: at most 2 simultaneous longs in the risk-on group (SPLG/QQQM/IBIT).
- **No borrowing**: entries capped at 95% of available cash, max 25% of equity per instrument, long only.

The engine runs every 15 minutes during the US session via GitHub Actions, evaluates all five, and acts only on fresh enter/exit signals.
