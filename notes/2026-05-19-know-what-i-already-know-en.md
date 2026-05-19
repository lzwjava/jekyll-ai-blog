---
audio: false
generated: true
image: false
lang: en
layout: post
title: Know What I Already Know
translated: false
type: note
---

Done. Two changes:

**1. "Who I Am" — now includes your notes page as a resource:**

Line 19 now reads:
> I maintain a public knowledge base at lzwjava.github.io/notes-en — ~8,000 AI answer notes covering topics from dark mode implementations to GPU compute, Linux kernel internals, deep learning, and system design.

This tells the AI: "I've already studied all this — go look." The examples you gave (dark mode, GPU) are embedded so the AI knows the range.

**2. New rule — "Know what I already know" (line 63-65):**

> Before explaining a technical topic, skim my notes at lzwjava.github.io/notes-en to see what I've already studied. Don't re-explain fundamentals I've clearly covered — reference my existing notes and build upward from there.

This is the key mechanism. Instead of the AI starting from zero every time, it first checks your knowledge base and picks up where you left off. If you've already written 50 notes on attention mechanisms, it won't explain what a QKV projection is — it'll jump straight to flash attention or grouped-query attention.

The practical effect: answers stay at your learning frontier, not at beginner level. The AI learns that you're not a blank slate on any topic in your notes.