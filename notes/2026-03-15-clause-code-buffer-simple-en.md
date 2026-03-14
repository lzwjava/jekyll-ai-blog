---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Buffer Explained Simply
translated: false
type: note
---

Question: Why does the Claude Code autocompact buffer need so much space (33k tokens)?

Answer:

## Why the Autocompact Buffer Needs 33k Tokens

Looking at your `/context` output — you're on **claude-opus-4-6 with a 1M token window**, so the 33k buffer is actually only **3.3%** of your total window. That's actually quite small in your case! But here's why the buffer exists and why it's sized that way:

### What the Buffer Actually Does

The 33k buffer is not sitting idle — Claude uses it for the summarization process itself. When autocompaction triggers, Claude needs free space to:

1. **Read and analyze** the entire conversation history
2. **Generate a structured summary** of what happened, what files were changed, what's in progress
3. **Write the compressed result** back as new context

All of that reasoning and output needs room to happen. If the context is already 100% full, there's nowhere to work.

### Why 33k Specifically?

The buffer was recently reduced from 45k to 33k — an undocumented improvement giving ~12k more usable tokens. Compaction now triggers at ~83.5% usage, giving ~167k usable tokens on a 200K window (up from ~155K).

The engineers built in a completion buffer — enough free space not just for the compaction process itself, but to allow the current task to finish gracefully. The difference is: old behavior meant hitting 90% context mid-task, forcing a compact and losing context about what you were doing; new behavior means hitting 75% context with plenty of room for the current task, completing it successfully, then compacting with full understanding of what was accomplished.

### Your Case (1M Window) is Special

On a 1M window, the 33k fixed buffer is only 3.3%. On a 200K window, it's 16.5%. Using a fixed token count instead of a percentage keeps the calculation accurate across all context window sizes.

So with your 1M context window on `claude-opus-4-6`, the buffer is barely noticeable — you have **967k free** and the 33k buffer is a rounding error.

### Can You Disable It?

Yes — you can turn off autocompact using `/config`, which reclaims buffer tokens for immediate use. But without adequate buffer space, Claude Code experiences performance degradation as context fills. The buffer maintains working memory headroom, ensuring consistent performance throughout your session.

A feature request to make the buffer size configurable was filed on GitHub (Issue #15435), but it was closed as a duplicate — Anthropic has not exposed this as a user-configurable setting.

### TL;DR

| Reason | Explanation |
|---|---|
| **Space to summarize** | Compaction itself generates tokens — needs room to work |
| **Task completion runway** | Lets current task finish before resetting context |
| **Fixed at 33k** | Not a percentage — same across 200K and 1M windows |
| **Your 1M window** | 33k is only 3.3% — basically irrelevant for you |

References:

- [Claude Code Context Buffer: The 33K-45K Token Problem](https://claudefa.st/blog/guide/mechanics/context-buffer-management)
- [Feature request: Configurable autocompact buffer size · Issue #15435](https://github.com/anthropics/claude-code/issues/15435)
- [How Claude Code Got Better by Protecting More Context](https://hyperdev.matsuoka.com/p/how-claude-code-got-better-by-protecting)
- [Claude Code Auto-Compact: What Triggers It](https://www.morphllm.com/claude-code-auto-compact)