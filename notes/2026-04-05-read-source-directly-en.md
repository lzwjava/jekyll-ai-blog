---
audio: false
generated: true
image: false
lang: en
layout: post
title: Read Source Directly
translated: false
type: note
---

Question: Is it better to just clone the OpenClaw source code and read it directly, without needing Claude Code?

Answer:

Yes — and that's actually the **simplest, most direct approach**. You don't need Claude Code at all for this.

## Why Direct Source Reading Works Fine Here

You already know:

- ✅ Webhook signature verification works
- ✅ Nextcloud is sending webhooks
- ✅ OpenClaw receives them
- ✅ The drop reason is `(no mention)`

So you just need to **find that string in the source** and trace the logic around it.

## Just Do This

```bash
git clone https://github.com/openclaw/... openclaw
cd openclaw

# Find the exact drop condition
grep -r "no mention" .
grep -r "drop" . --include="*.php"
grep -r "mention" . --include="*.php"
```

That's it. `grep` will pinpoint the exact file and line. Then you read 20–50 lines of surrounding code and you know exactly what condition the bot requires.

## Claude Code Is Overkill Here

Claude Code is valuable when:

- The codebase is huge and unfamiliar
- You need to trace across many files
- You want AI to **explain** complex logic

But for your case — one specific drop condition with a known log message — **grep + reading the relevant function** is faster and more direct than spinning up Claude Code.

## Summary

| Approach | When useful |
|---|---|
| `grep` + read source directly | ✅ Your situation right now |
| Claude Code | Large unfamiliar codebase, complex multi-file tracing |
| Web search / docs | Initial setup, not runtime logic |

You're right. Clone it, grep it, read it. Done.
