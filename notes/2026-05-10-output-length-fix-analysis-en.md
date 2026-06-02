---
audio: false
generated: true
image: false
lang: en
layout: post
title: Output Length Fix Analysis
translated: false
type: note
---

Here's a full review of my fix.

---

## Root Cause Analysis

The error: the LLM returned 1518 characters instead of a 6-word title. Two things broke:

1. The model ignored the instruction "respond with only the title" and produced a full essay with analysis and bullet points.
2. The code treated this as a fatal error -- `raise ValueError` with no retry.

Why did the model ramble? Two compounding factors:

- **No `max_tokens` cap.** The API call in `generate_title` went through `_call_llm_or_exit` -> `call_openrouter_api` with `max_tokens=None`. The model had no hard constraint on output length. Some models (especially weaker or "chatty" ones) treat "respond with only X" as a suggestion, not a rule.
- **Prompt structure was suboptimal.** The old prompt was one long sentence: *"Generate a very short title in English (maximum six words, do not have single quote) for the following text and respond with only the title: {content}"*. This is an imperative instruction embedded in the same text block as the content. Many models handle this poorly -- they see the content, get "inspired", and start generating analysis before they remember the instruction.

---

## My Fix Steps

### Step 1: Cap `max_tokens` on the API call (the hard guard)

**File:** `create_note_utils.py`
**Change:** Pass `max_tokens=60` through `_call_llm_or_exit` to `call_openrouter_api`.

**Why:** This is the most reliable fix. Even if the model tries to ramble, the API will cut off output after ~60 tokens. For a 6-word title, 60 tokens is generous (6 words = ~8-10 tokens). The token limit is enforced at the API level -- no model can bypass it. It's a safety net that works regardless of model behavior.

**What I had to change:** `_call_llm_or_exit` didn't accept a `max_tokens` parameter. I added `max_tokens=None` as an optional param and forwarded it to `call_openrouter_api`. This keeps backward compatibility -- all other callers that don't pass `max_tokens` still get `None` (unlimited).

### Step 2: Add retry logic (resilience)

**File:** `create_note_utils.py`
**Change:** Wrap the title generation in a retry loop (3 attempts). If the title is >= 100 chars, print a warning and retry. Only raise `ValueError` after 3 failures.

**Why:** The old code had a "fail fast" approach -- one bad LLM response and the whole `ww note` command crashes. LLM output is non-deterministic. A retry is cheap (one more API call, ~$0.001) and often succeeds because the model produces different output each time. The warning message also gives the user visibility that something odd happened.

**Design choice:** I chose 3 retries. Too few (1) is what we already had. Too many (10) would silently waste time/money on a genuinely broken prompt. 3 is the standard retry count for transient failures.

### Step 3: Strengthen the prompt (the soft guard)

**File:** `create_note_from_clipboard.py`
**Change:** Rewrote the prompt from:
```
Generate a very short title in English (maximum six words, do not have single quote)
for the following text and respond with only the title: {content}
```
To:
```
Give a short English title (at most 6 words, no quotes, no explanation) for:
{content}

Title:
```

**Why two things changed here:**

1. **"no explanation" is explicit.** The old prompt said "respond with only the title" but didn't say why the model might want to add extra text. Some models interpret "respond with only X" as a formatting preference, not a prohibition. "no explanation" is more direct about what NOT to do.

2. **Trailing `\n\nTitle:` priming.** This is the bigger change. By ending the prompt with `Title:`, I'm using completion-style priming. The model sees a partially completed response and naturally continues with just the title text. This works far better than imperative instructions for most models -- it exploits how next-token prediction works. The model doesn't need to "decide" to follow an instruction; it just completes the pattern.

---

## What I Did NOT Fix (and why)

- **No system message.** The `call_openrouter_api` function only supports a single user message (no `system` role). Adding system message support would require changing the client interface, which is a bigger refactor than needed. The `max_tokens` + prompt fix is sufficient.

- **No similar fix for `generate_short_title`.** That function uses a different prompt and is less likely to ramble (it's generating a 4-word filename slug from an existing title, not from raw content). If it becomes a problem, the same pattern applies.

- **No model-specific workarounds.** The fix is model-agnostic. Whatever model is configured via the `MODEL` env var, `max_tokens=60` and the primed prompt will work.

---

## Assessment of the Fix

**Strengths:**
- Defense in depth: prompt (soft) + max_tokens (hard) + retry (resilience)
- Backward compatible: `_call_llm_or_exit` defaults `max_tokens=None`
- Minimal code change: ~15 lines touched total

**Remaining risk:**
- If the model outputs 60 tokens of garbage that happens to be < 100 chars, the retry loop won't catch it (the char check passes but the title is nonsense). This is low probability and would need a semantic check, which is overengineering for this use case.
