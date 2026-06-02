---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenAI Codex Usage Limits Explained
translated: false
type: note
---

**Question:** What does this Codex UI message mean — "剩余用量0%, 5小时, 1周, 0% 12:52AM 39% 7:10PM", and why does it show two different time windows (5 hours and 1 week)?

**Answer:**

Your friend is hitting **OpenAI Codex's usage limits** on a ChatGPT Plus subscription. Here's what each part means:

---

## The Two Rate Limit Windows

Codex (and ChatGPT Plus in general) enforces **two independent rolling windows** simultaneously:

| Label | Meaning |
|-------|---------|
| **5小时** (5 hours) | Short-term rate limit window — resets every ~5 hours |
| **1周** (1 week) | Long-term usage cap — resets weekly |

Both must be non-zero for you to use Codex. If **either** hits 0%, you're blocked until the respective window resets.

---

## Reading the Specific Values

```
剩余用量0%       ← current remaining = 0%, fully exhausted
5小时            ← short window resets in 5 hours (at 12:52 AM)
1周              ← weekly window at 39% remaining (resets at some point in the week)
0% 12:52AM      ← short-term bucket: 0% left, resets at 12:52 AM
39% 7:10PM      ← weekly bucket: 39% left, last checked/updated at 7:10 PM
```

So the **5-hour window is the bottleneck** right now — it's at 0%. The weekly budget still has 39% left, but it doesn't matter because the short window is empty.

---

## Why Two Windows?

This is a standard **token bucket / sliding window** rate limiting pattern:

- **Short window (5hr)** — prevents burst abuse, e.g. running 1000 agentic Codex tasks back-to-back in an hour
- **Long window (1 week)** — caps total monthly-ish consumption per subscription tier

Codex is particularly expensive to run (it's doing real code execution + LLM inference), so OpenAI applies tighter limits than regular ChatGPT.

---

## "Codex 太烧token" (Codex burns tokens fast)

Correct. Codex CLI/agent mode is expensive because:

1. **Agentic loops** — each task = multiple LLM calls (plan → tool use → observe → repeat)
2. **Long context** — it reads your whole codebase/files into context
3. **Code execution feedback** — stdout/stderr gets fed back into the next prompt

A single Codex session can easily burn 50k–200k tokens depending on task complexity. On Plus, the weekly allocation runs out fast if you use it seriously.

---

## Bottom Line

Your friend needs to wait ~5 hours for the short-term window to reset. After that, they'll have access again (with 39% of weekly budget remaining). If they hit 0% on the weekly window too, they'd need to wait until the weekly reset.

For heavy agentic use, **Plus limits are too tight** — Pro tier or API direct access (pay-per-token) is the practical path.
