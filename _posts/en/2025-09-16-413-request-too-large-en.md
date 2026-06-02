---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-oss-120b
title: Resolving 413 Request Too Large Errors
translated: false
type: note
---

## What the error means

- **413 Request Too Large** is an HTTP status code indicating the server refused to process the request because the payload exceeds the allowed size. In the context of OpenAI’s inference service, the “payload” is the total number of tokens (input + output) sent in a single request. [1]

- **Tokens‑per‑minute (TPM) limit**: The `openai/gpt‑oss‑120b` model is configured with a maximum of **8,000 TPM** for the on‑demand service tier. The request you sent contained **13,701 tokens**, which is **5,701 tokens over the limit**. [1]

- **Why it happens**:
  1. **Large prompt** – the input text (including system instructions, user messages, and any appended data) may be very long.
  2. **High max‑tokens setting** – if the request asks the model to generate a long completion, the projected output token count is added to the input count.
  3. **Rapid successive calls** – if many requests are made in quick succession, the cumulative tokens in the current minute can exceed the TPM quota, even if each individual request is below the limit.

## How to resolve it

| Option | What to do | Effect |
|--------|------------|--------|
| **Trim the prompt** | Remove unnecessary text, use concise instructions, or compress data (e.g., summarize large blocks before sending). | Lowers the input token count. |
| **Reduce `max_tokens`** | Request a shorter completion (e.g., set `max_tokens` to 500 instead of 2000). | Decreases the projected output token count. |
| **Split the request** | Break a huge document into multiple smaller chunks and call the model sequentially, stitching results together afterwards. | Keeps each call under the TPM limit. |
| **Upgrade the tier** | Move to a higher‑capacity tier (e.g., Dev Tier) where the TPM limit is larger or unlimited. | Allows larger single‑request payloads without error. |
| **Throttle calls** | Add a short delay between requests or implement rate‑limiting to keep total tokens per minute ≤ 8,000. | Prevents cumulative TPM overflow. |

## Quick checklist before sending a request

1. **Count tokens** – use OpenAI’s tokenizer tool (or `tiktoken`) to estimate total tokens (prompt + max tokens).
2. **Stay ≤ 8,000 TPM** for the on‑demand tier.
3. **If near the limit**, consider one of the mitigation steps above.

By ensuring the request stays within the 8,000‑token‑per‑minute quota, the 413 “Request Too Large” error will be avoided. [1]

Citations:
[1] https://www.reddit.com/r/OpenAI/comments/1nbtl2p/wow_weve_been_burning_money_for_6_months/
