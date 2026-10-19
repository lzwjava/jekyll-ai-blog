---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVDA entry now at 2 shares minimum
translated: false
type: note
---

Done. NVDA entries now size at **2 shares minimum** instead of 1:

- **`bot/config.py`** — added `'min_quantity': 2` to the NVDA instrument entry.
- **`bot/engine.py`** — in `open_long()`, after the "size too small" check, quantity is bumped up to the instrument's `min_quantity` (defaults to 1, so all other instruments are unaffected). The `elif dry_run:` became `if dry_run:` since the new statement separates the two branches.

Verified: when the old sizing produced 1 share at NVDA's current price, it now results in 2; sizes already ≥ 2 stay unchanged, and the "size too small" skip still works. The bot will place the first 2-share NVDA buy on its next qualifying entry signal.
