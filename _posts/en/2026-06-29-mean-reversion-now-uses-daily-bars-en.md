---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mean reversion now uses daily bars
translated: false
type: note
---

Done. The change:

```python
{'symbol': 'AAPL', ... 'strategy': 'mean_reversion', 'period': BarPeriod.DAY, ...}
{'symbol': 'INTC', ... 'strategy': 'mean_reversion', 'period': BarPeriod.DAY, ...}
```

**What this changes in behavior:**

- Both names now evaluate mean-reversion on **daily bars** instead of 15-minute bars. The z-score window (`ZSCORE_WINDOW=20`) now spans 20 *days* of history rather than 20 fifteen-minute candles, and `BARS_LIMIT=120` gives 120 days — plenty.
- An entry and its exit now naturally land on **different calendar days**, so they no longer count as day trades. The PDT guard (`engine.py:84-88`) stops firing on these names, and the bot can actually act on EXIT signals instead of deferring them.
- The every-15-min cron is unchanged and harmless — daily bars just update once per session, but the bot still re-checks positions/stops on each run.

**No other code needed touching** — `engine.py`, `risk.py`, and `strategies.py` all read the period from the instrument config, so they pick this up automatically. `NVDA` (1h momentum), `GLD`/`USO` (4h trend) are untouched.

This is a config-only edit on a tiny strategy table — low risk. I haven't committed it. Want me to commit (and optionally push so the next scheduled run uses it)?
