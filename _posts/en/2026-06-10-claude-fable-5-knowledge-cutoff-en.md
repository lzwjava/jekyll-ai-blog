---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Fable 5 Knowledge Cutoff
translated: false
type: note
---

Confirmed. Claude Fable 5 has a knowledge cutoff date of Jan 2026, matching what I told you. Anthropic's docs clarify the distinction: "reliable knowledge cutoff" is the date through which the model's knowledge is most extensive and reliable, while the training data cutoff is the broader date range of training data used — so I may have spotty awareness of some things slightly past January 2026, but January is the line I'd trust.

For context on this model specifically: Claude Fable 5 became generally available on the Claude API, AWS Bedrock, Vertex AI, and Microsoft Foundry on June 9, 2026 — yesterday — with a 1M token context window and 128K max output tokens.

So for anything between Feb 2026 and today (June 10, 2026), I'll search rather than rely on training data.

References:

- [Models overview — Claude API Docs](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Claude Fable 5 and Claude Mythos 5 — Anthropic](https://www.anthropic.com/news/claude-fable-5-mythos-5)
- [Initial impressions of Claude Fable 5 — Simon Willison](https://simonwillison.net/2026/Jun/9/claude-fable-5/)
