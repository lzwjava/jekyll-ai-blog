---
audio: false
generated: true
image: false
lang: en
layout: post
title: Real User vs Test Log
translated: false
type: note
---

2 lines logged, but only **1 is a real user**:

| # | Prompt | Source |
|---|---|---|
| 1 | `What risk factors are disclosed in 10-K filings?` | My test |
| 2 | `What legal proceedings and litigation matters are mentioned in Amazon's SEC filing?` | **Real user** — 05:51 UTC, clicked the 3rd sample button |

That's it so far. Only one person tried it after the restart. The Amazon question matches the sample button text exactly, so someone opened the page and clicked the third suggestion. They got 200 tokens of output in 1.3 seconds — reasonable latency.

No free-form typing from users yet. Probably need to wait a bit more for the WeChat group traffic to hit the new server.
