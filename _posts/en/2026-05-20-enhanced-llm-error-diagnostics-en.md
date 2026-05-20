---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enhanced LLM error diagnostics
translated: false
type: note
---

All good. Here's a summary of what was changed and why:

## Changes made

### `ww/llm/openrouter_client.py` — LLM client layer

**Problem:** When `call_openrouter_api_with_messages` got an empty content response (HTTP 200 but `message.content` is `None` or `""`), it just returned the falsy value silently. When it got a non-200 response, the error message only showed the status code and raw response body — no context about model, proxy, or tokens.

**Fix:** Added two improvements:

1. **`_check_proxy()`** — new helper that checks proxy env vars and tests TCP connectivity to the proxy host:port. Returns a human-readable string like `"HTTP_PROXY=http://127.0.0.1:7890 (port 7890 reachable)"` or `"UNREACHABLE: ..."`.

2. **Empty content detection** — after a successful HTTP 200, parses the JSON body and checks if `content` is falsy. If so, raises an exception with: model name, `max_tokens`, `finish_reason`, HTTP status, proxy status, and full response body (first 1000 chars). This covers the case that hit you — when the model returns `content: null`.

3. **Enhanced HTTP error** — now includes model, max_tokens, proxy status alongside the status code and response body.

### `ww/note/create_note_utils.py` — caller layer

**Problem:** `_call_llm_or_exit` swallowed all detail. The old code:
```python
result = call_openrouter_api(prompt, max_tokens=max_tokens)
if not result:
    print("Failed to generate title with max 6 words. Exit.")
    sys.exit(1)
```
No model name, no prompt preview, no exception details.

**Fix:** Wrapped in a try/except that prints:
- `[error] LLM call failed. Model: <model>, max_tokens: <N>`
- `[error] Prompt (first 300 chars): <prompt preview>`
- `[error] Exception: <full details>`
- Full traceback

And for the empty-result path (which shouldn't happen anymore since the LLM client now raises on empty content):
- `[error] LLM returned empty result. Model: <model>, max_tokens: <N>`
- `[error] Prompt (first 300 chars): <prompt preview>`

---

Now if `ww note` fails on title generation again, you'll see the **model name**, the **prompt** it sent, the **HTTP status**, the **finish_reason** from the API, and your **proxy connectivity** status — everything needed to diagnose what went wrong.