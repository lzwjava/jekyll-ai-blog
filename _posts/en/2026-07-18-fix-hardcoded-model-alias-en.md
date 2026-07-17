---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix hardcoded model alias
translated: false
type: note
---

Fixed and pushed (`b515650`).

The error: `x_bulk_unfollow.py` hardcoded `model="gemini-flash"` — that's just an alias, not a valid OpenRouter model ID. OpenRouter expects the full slug like `google/gemini-2.5-flash`. Changed it to `model=None`, which makes `call_openrouter_api_with_messages` fall back to your `MODEL` env var (`deepseek/deepseek-v4-flash`). Run `ww x unfollow` again and it should work.
