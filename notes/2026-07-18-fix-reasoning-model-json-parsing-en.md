---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix reasoning model JSON parsing
translated: false
type: note
---

Fixed and pushed (`7afc39b`).

Two problems:
1. `max_tokens=100` was too small — `deepseek/deepseek-v4-flash` is a reasoning model, so it spent all 100 tokens on internal reasoning (finish_reason=length) and never produced visible output. Bumped to 2000.
2. `json.loads(response)` failed when the model wrapped JSON in markdown fences or reasoning text. Now uses regex to extract the `{...}` JSON object from the response.

Try `ww x unfollow` again — the `llm_error` cases should be gone.
