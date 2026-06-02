---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Barely Good Principle for Prompting
translated: false
type: note
---

Question: How does the "doing things barely" principle apply to writing prompts for LLMs and using tools like Claude Code — finding the sweet spot between too little context and too much?

Answer:

## The "Barely Good" Principle for LLM Prompting

This is a sharp extension of the philosophy. With LLMs, the same calibration challenge exists — but the dynamics are unique because **LLMs already carry enormous world knowledge**. You are not teaching them from scratch; you are *steering* something already highly capable.

---

## The Two Failure Modes

| Too Little | Barely Good | Too Much |
|---|---|---|
| LLM doesn't know the goal | Clear intent + key constraints | Over-specified, rigid, wastes tokens |
| Wrong assumptions made | Correct assumptions guided | No room for LLM's own judgment |
| Output misses the point | Output hits the target well | LLM becomes a dumb executor |
| Agent wanders or loops | Agent moves with purpose | Agent is micromanaged into failure |

---

## Why LLMs Need Less Than You Think

LLMs like Claude have already internalized:
- Coding best practices, design patterns, languages
- Writing styles, formats, genres
- Domain knowledge across medicine, law, science, engineering
- Reasoning frameworks and step-by-step problem solving

So when you write a prompt, you are **not filling an empty vessel** — you are **giving a direction to an expert**. A good manager doesn't explain to a senior engineer what a for-loop is. They say: *"Build a rate limiter for the API, Redis-backed, 100 req/min per user."* That's it.

---

## Applying This to Claude Code

Claude Code is an agentic coding tool. The "barely enough" prompt principle here means:

**Tell it:**
- What the goal is
- Key constraints or non-obvious context
- What "done" looks like (if not obvious)

**Don't tell it:**
- How to write every function
- Which libraries exist (it knows)
- Step-by-step instructions for standard tasks
- Everything you already know about the codebase it can read itself

**Example — Too Much:**
> "Please open the file users.py, look at the User class, add a method called get_full_name that concatenates first_name and last_name with a space between them, make sure to add a docstring, use f-strings, and return a string."

**Example — Too Little:**
> "Fix users."

**Example — Barely Good:**
> "Add a `get_full_name` method to the User model in users.py."

Claude Code reads the file, understands the existing style, writes idiomatic code, adds a docstring if that's the pattern — all without being told.

---

## The Art of the Barely Good Prompt

The skill is knowing **what to omit** — and that requires understanding:

1. **What the LLM already knows** — standard patterns, common libraries, language idioms. Don't explain these.
2. **What is unique to your situation** — your business logic, your architecture decisions, non-obvious constraints. Always include these.
3. **What the goal looks like** — a brief statement of success criteria. One sentence often suffices.
4. **What to avoid** — one or two negative constraints if there's a real risk of wrong direction ("don't modify the schema").

---

## The Deeper Insight

Just like with eyeglasses and air conditioning — the principle demands **you know the domain well** to apply it. A beginner can't write barely-good prompts because they don't know what the LLM already handles. They over-specify out of anxiety, or under-specify out of laziness.

Mastery shows as **conciseness with precision** — few words, right words, correct assumptions about what the model will infer correctly.

> Writing a barely good prompt is itself a skill that proves understanding — of the task, of the LLM's capabilities, and of where the gap between them actually lies.

This is exactly why experienced engineers write shorter prompts than beginners, and get better results.

References:

- [https://lzwjava.github.io/vision-tips-en](https://lzwjava.github.io/vision-tips-en)
- [https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
