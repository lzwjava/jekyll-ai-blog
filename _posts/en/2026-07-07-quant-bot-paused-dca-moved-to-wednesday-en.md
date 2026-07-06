---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quant Bot Paused, DCA Moved to Wednesday
translated: false
type: note
---

Done. Here's what changed:

**Stopped the quant bot's strategy loop** — the `.github/workflows/bot.yml` is still in the repo (kept intact, not deleted) but it won't run anymore unless explicitly triggered. The old schedule ran every 15 min during US market hours. The workflow file stays as a record of your quant strategies.

**Moved DCA to Wednesday** — the `.github/workflows/main.yml` schedule changed from:
- `35 14 * * 4` (every **Thursday** 14:35 UTC / 10:35 PM Beijing)
- → `35 14 * * 3` (every **Wednesday** 14:35 UTC / 10:35 PM Beijing)

**invest.py untouched** — still buys 1 share NVDA market order via Tiger Brokers. No code changed.

**All quant code preserved** — `bot/` directory (config, engine, strategies, indicators, risk, broker, news, report), `run_bot.py`, GitHub Actions workflow — everything stays. You can re-enable it later by updating the bot.yml `on.schedule` if needed.

Pushed to `main`. The next DCA will fire this Wednesday at 22:35 Beijing time.
