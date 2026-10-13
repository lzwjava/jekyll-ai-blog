---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean News Agent Run, Two Fixes
translated: false
type: note
---

Ran clean — exit 0, 19/19 feeds, all 4 sections LLM-edited.

```
news-agent · window=48h · top=40 · LLM: openrouter/deepseek/deepseek-v4.1-flash
19 sources -> 348 raw -> 40 articles -> 4 sections (4 LLM-edited)
```

**Section headlines from this run** (`output/digest.md`):

- **Labs & Product** — "Google DeepMind details Gemini 4 Argon; Higgsfield extends AI video to 10+ minutes" (5 items)
- **Research & Technical** — "Anthropic on self-replication and distillation; Python 3.15 ships" (10)
- **Community: YC & Hacker News** — "HN: Anthropic source control rework, LLM gateway launch, and AI crawler flood" (6)
- **Industry & AI News** — "Disney bids $20M for Character.AI tech; Pluto Security raises $42M" (10)

Fresh artifacts (timestamps 03:48):

```
output/index.html                HN-style feed page
output/digest.md                 markdown digest
output/digest.json               + dated aliases digest-2026-10-13.{md,json}, index-2026-10-13.html
output/feed.xml                  RSS 2.0
```

Two small fixes I made while running (currently **uncommitted**):

1. `news_agent/llm.py` — auto-detected provider/model is resolved back into settings, so the header now prints `openrouter/deepseek/deepseek-v4.1-flash` instead of `/default`, and `digest.json` records the real model.
2. `news_agent/render.py` — added the missing `output/digest.json` "latest" alias (md/html had one, json didn't).

Want me to commit and push those two?
