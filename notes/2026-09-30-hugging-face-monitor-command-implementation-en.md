---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hugging Face Monitor Command Implementation
translated: false
type: note
---

All done. Here's a summary of what was implemented:

## New Command: `ww monitor huggingface`

### Files created
- **`ww/monitor/__init__.py`** — package marker
- **`ww/monitor/huggingface.py`** — the monitoring module

### Files modified
- **`ww/main.py`** — added `monitor` group in help text, dispatch chain, and `all_groups` list
- **`~/.zsh/completions/_ww`** — added `monitor` to commands array, `monitor_cmds` array, subcmd dispatch, and `--now`/`--hours` flag completion

### How it works
1. **Fetches** top 10 trending models from `https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=10`
2. **Compares** against a cached snapshot at `~/.ww/monitor/hf_trending.json`
3. **Sends Telegram alert** if the top 10 changed (lists new entries, dropped entries, and positional shifts)
4. **Caches** the current top 10 as the new baseline for next run

### Flags
- `--now` — Force alert even if the top 10 is unchanged
- `--hours N` — Look back N hours (for cron use)

### Telegram config
Set these env vars in `.env`:
```
TELEGRAM_BOT_TOKEN=<your_bot_token>
TELEGRAM_CHAT_ID=<your_chat_id>
```
(Also accepts `TELEGRAM_HABIT_BOT_API_KEY` as fallback.)

### Cron job (included as comments in the module)
```cron
* * * * * cd /Users/lzwjava/projects/ww && uv run ww monitor huggingface >> /tmp/ww-monitor-hf.log 2>&1
```
Every 10 minutes (adjust as needed: `*/10 * * * *`).
