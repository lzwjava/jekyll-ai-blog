---
audio: false
generated: true
image: false
lang: en
layout: post
title: Daily mean-reversion config update
translated: false
type: note
---

Committed and pushed.

- **Commit:** `ec948f7` on `main`
- **Pushed** to `origin/main` (`e521e46..ec948f7`)

The next scheduled run (the every-15-min trade loop during US session, `2,17,32,47 13-20 * * 1-5` UTC) will pick up the new config: AAPL/INTC on daily bars and the three new names (AVGO, GOOGL, PDD). Since these are all daily mean-reversion now, they'll trade as swing positions and won't trip the PDT guard.

You can watch the first run that uses it with `gh run list` once the market's open, or trigger one manually via the workflow's `workflow_dispatch` (`run` job).
