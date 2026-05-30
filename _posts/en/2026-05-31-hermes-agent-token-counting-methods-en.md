---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Token Counting Methods
translated: false
type: note
---

Good question. Since you're using MiMo via the Anthropic-compatible endpoint with Claude Code / agent tooling, the token counts come back in the API response's `usage` field — same as standard Anthropic API.**Question:** In Hermes Agent, how do you see input and output token counts?

**Answer:**

Several ways, from built-in to DIY:

---

## 1. Built-in: `/analytics` page

Hermes has an Analytics page at `/analytics` that displays a Daily Token Usage chart with input and output token counts. Navigate there in the Hermes web UI. Note: there's a known bug where input is reported far smaller than output — input/output counts may appear swapped or undercounted in the insights report.

---

## 2. Session files: `~/.hermes/sessions/`

Hermes stores request dumps in `~/.hermes/sessions/`. You can inspect them directly:

```bash
# List sessions
ls ~/.hermes/sessions/

# Grep for token usage across all sessions
grep -r "input_tokens\|output_tokens" ~/.hermes/sessions/ | tail -50

# Pretty-print a specific session
cat ~/.hermes/sessions/<session_id>.json | python3 -m json.tool | grep -A5 "usage"
```

The `usage` object in each API response follows the standard Anthropic shape:
```json
{
  "input_tokens": 14200,
  "output_tokens": 843,
  "cache_read_input_tokens": 11500,
  "cache_creation_input_tokens": 0
}
```

---

## 3. What the token counts actually mean for MiMo Credits

Given the MiMo pricing table from the doc, you can calculate Credit burn yourself. For `mimo-v2.5`:

```python
def credits_used(input_tokens, output_tokens, cache_hit_tokens=0):
    cache_miss = input_tokens - cache_hit_tokens
    credits = (
        cache_hit_tokens   * 2      +   # 2 Credits/token cache hit
        cache_miss         * 100    +   # 100 Credits/token cache miss
        output_tokens      * 200        # 200 Credits/token output
    )
    return credits

# Example: typical Hermes call
print(credits_used(14000, 800, cache_hit_tokens=11500))
# cache hit: 11500*2=23000, miss: 2500*100=250000, out: 800*200=160000
# Total: 433,000 Credits per call
```

With Lite plan (4.1B Credits), that's ~9,470 calls before quota exhausted. Fits the "~200 medium-complex tasks" estimate from the official docs (each task = multiple calls).

---

## 4. Reality check on Hermes overhead

A typical Hermes API call's input is dominated by: tool definitions (~8K tokens), system prompt (~2–3K tokens), SOUL/MEMORY/USER.md (~1–5K tokens), and skills if loaded (~0–2K tokens). For a brand-new chat with no skills active, the input cost is roughly 12K–14K tokens before you've sent your first message.

So for MiMo Credit math: assume ~13K input tokens mostly as cache miss on the first call, then mostly cache hits on subsequent turns within the same session.

---

**References:**

- [Hermes Issue #1091 — Token visibility in CLI](https://github.com/NousResearch/hermes-agent/issues/1091)
- [Hermes Issue #4379 — Token overhead analysis](https://github.com/NousResearch/hermes-agent/issues/4379)
- [Hermes Issue #18615 — Input/output counts swapped bug](https://github.com/NousResearch/hermes-agent/issues/18615)
- [Cut your Hermes token bill — LumaDock](https://lumadock.com/tutorials/cut-hermes-token-costs)