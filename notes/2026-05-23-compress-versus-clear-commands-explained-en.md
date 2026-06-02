---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compress versus Clear Commands Explained
translated: false
type: note
---

Yes, that's the right mental model:

- `/compress` — summarizes the conversation into a condensed form, preserving key context. Use when the next task builds on what was discussed (same project, related debugging, continuation of work). You keep the "what happened so far" without burning context window on verbose tool outputs.

- `/clear` — wipes the conversation entirely. Use when switching to something completely unrelated. Fresh start, no baggage.

The practical difference matters because `/compress` injects the summary as a system message so the model still "remembers" decisions, file paths, errors found, etc. `/clear` means the model knows nothing about prior turns.

One nuance: `/compress` isn't free — it still costs tokens (the summary itself). If the conversation is short or the next task is truly unrelated, `/clear` is cheaper and cleaner. `/compress` shines when you've had a long multi-step session and want to continue without losing the thread.
