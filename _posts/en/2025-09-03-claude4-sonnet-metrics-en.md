---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude 4 Sonnet Completion Metrics Explained
translated: false
type: note
---

Short version: it ended normally.
`finish_reason: "stop"` means the model reached a natural end of its reply (hit a stop sequence like the assistant-end token) and did **not** run into a length cap, error, or cancel.

Here’s what the rest of that record is telling you, in plain English:

* **Model & route**
  You called **anthropic/claude-4-sonnet-20250522** via **Google Vertex** (`provider_name: "Google"`). That’s why you see a `provider_responses` entry with status 200.

* **Timing / speed**

  * `latency: 2850` → \~2.85 s until the **first token** showed up.
  * `generation_time: 76365` → about **76.4 s** total to finish the reply.
  * With `tokens_completion: 2376`, that’s roughly **31 tokens/sec** throughput across the whole generation (2376 ÷ 76.4 ≈ 31.1).

* **Token counts (two sets)**

  * `tokens_prompt: 8446`, `tokens_completion: 2376` → your aggregator’s counts.
  * `native_tokens_prompt: 9007`, `native_tokens_completion: 2511` → the **provider’s** own tokenizer/accounting. These often differ due to different tokenizers, system wrappers, or hidden control tokens.
  * `native_tokens_reasoning: 0` → this run didn’t use a “reasoning tokens” meter (some providers expose this when a special reasoning mode is on).
  * `native_tokens_cached: 0` → no prompt caching hit.

* **Streaming & cancelation**

  * `streamed: true` → tokens were streamed to you.
  * `cancelled: false` → you didn’t interrupt it.

* **Why not “length”?**
  If it had hit the max token limit, you’d see `finish_reason: "length"`. You didn’t, so the model completed before any cap.

* **When did this happen?**
  `created_at: "2025-09-02T17:26:45.92824+00:00"` (UTC). In your timezone (Asia/Taipei, UTC+8) that’s **2025-09-03 01:26:45**.

* **Costs/usage fields**

  * `usage: 0.064686` → your system’s cost/usage metric (units depend on your billing layer).
  * Several `null` fields just mean your router didn’t record extra details (moderation latency, search results, etc.).

* **Misc.**

  * `finish_reason: "stop"` (again) is the key: normal stop via stop token.
  * `origin: ""`, `app_id: null` → no specific app tag.
  * `is_byok: false` → not a bring-your-own-key call.

If you want, paste a second example where you saw `length` or `cancelled`, and I’ll contrast them line-by-line (no tables).
