---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Picks One per Ten Profiles
translated: false
type: note
---

Pushed (`7029c8a`).

New approach:

- Gathers 10 profiles at a time (scrolling as needed)
- Sends all 10 intros to the LLM in one call
- LLM picks exactly 1 to unfollow from each batch
- 1-in-10 ratio distributes unfollows conservatively

The LLM prompt now asks for `{"index": <1-10>, "reason": "..."}` — it compares all 10 profiles relative to each other and picks the single least valuable one. This avoids unfollowing someone who might be useful just because they looked borderline in isolation.
