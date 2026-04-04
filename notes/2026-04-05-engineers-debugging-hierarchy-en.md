---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Engineer's Debugging Hierarchy
translated: false
type: note
---

Question: Is the debugging process for complex technical problems analogous to how a human engineer thinks — trying from memory first, then searching, then running commands, and finally going to the source code as a last resort?

Answer:

Yes — you've described it **perfectly**. This is exactly the mental model of an experienced engineer.

## The Engineer's Debugging Hierarchy

| Stage | Human Engineer | Claude / Claude Code |
|---|---|---|
| 1st | Use existing knowledge / experience | Training knowledge |
| 2nd | Google / Stack Overflow / docs | Web search |
| 3rd | Run commands, test, observe output | bash / tool calls |
| 4th | Clone repo, read actual source code | Read source directly |

Each stage is only triggered **when the previous one fails**. A good engineer doesn't jump to reading source code for every problem — that's expensive and slow. But they also know **when to stop guessing** and go to ground truth.

## Why This Order Makes Sense

- **Memory/experience first** — fastest, zero cost
- **Search second** — cheap, covers 80% of common problems
- **Run commands third** — validates assumptions with real evidence
- **Source code last** — slow to read, but **never wrong**

## Your Exact Case Followed This Pattern

1. ✅ Tried config knowledge (bot setup, Docker networking)
2. ✅ Searched docs / community help
3. ✅ Ran test requests, observed webhook behavior
4. ✅ Now ready to read OpenClaw source — **because all else pointed here**

## The Key Insight

> Source code is the **ground truth** — but you only go there when you've **exhausted faster paths**.

A junior engineer goes to source code too early (wastes time) or never goes (stays stuck). A senior engineer knows **exactly when** the right moment is — and you've reached that moment.

That's good engineering instinct.