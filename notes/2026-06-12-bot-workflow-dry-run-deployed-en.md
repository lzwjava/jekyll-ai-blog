---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bot workflow dry-run deployed
translated: false
type: note
---

Committed as `eac1e05` and pushed to `main`. 13 files, 575 insertions.

One thing to be aware of: the `bot.yml` workflow is now live on GitHub, so the trade loop will start running on its schedule (every 15 min during the US session, plus the 7am/9pm Beijing reports). It's safe — the `BOT_DRY_RUN` repository variable isn't set, so it defaults to dry-run and will only log signals to the Actions log. When you're ready to go live, set the repo variable `BOT_DRY_RUN=0` under Settings → Secrets and variables → Actions → Variables.
