---
audio: false
generated: true
image: false
lang: en
layout: post
title: PDT Guard Live With Deferred Trades
translated: false
type: note
---

Pushed as `2e6c90d`. The PDT guard is live, built on Tiger's own `day_trades_remaining` counter (currently 3 for your account):

- **Selling**: the bot never closes a position the same US-Eastern day it bought it. A same-day exit signal gets logged as deferred and re-checked the next day — meanwhile the protective stop stays at the broker, because eating a PDT day-trade is better than eating an unprotected loss.
- **Buying**: each position opened today has a stop that could fire before the close, and that fill would count as a day trade. So a new entry is only allowed when `day_trades_remaining` is strictly greater than the number of still-held positions bought today — there's always a reserved slot for every live same-day stop, including the new one's.

Verified with five scenario tests (fresh day, multiple same-day stops, no spare slot, exhausted counter, already-sold-today) plus a live API check.

One honest trade-off to be aware of: deferring same-day exits slightly changes the 15-minute mean-reversion behavior — when AAPL or INTC snaps back to the mean within hours (the usual case), the bot now holds overnight and sells the next day instead of capturing the revert immediately. With 3 day trades per 5 days as the budget, that's the price of staying under the PDT radar. Everything takes effect at the next live tick, Monday 21:32 Beijing.
