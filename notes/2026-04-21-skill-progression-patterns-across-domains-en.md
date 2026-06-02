---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skill Progression Patterns Across Domains
translated: false
type: note
---

Question: Does language learning and programming/ML follow a similar progression where beginners overlook details (grammar, capitalization, exception handling, attention mechanisms), but as they advance, they naturally adopt best practices?

Answer:

Yes, absolutely. This is a well-documented cognitive and skill-acquisition pattern. It maps almost perfectly across domains.

---

## The Universal Skill Progression Model

This follows what psychologists call the **Dreyfus Model of Skill Acquisition** — from Novice → Advanced Beginner → Competent → Proficient → **Expert**.

---

## English as a Foreign Language

**Early stage:**
- Grammar errors are invisible — the learner doesn't have enough internalized rules to even *notice* them
- Capitalization feels like a stylistic choice, not a rule
- The goal is just comprehension and basic communication

**Later stage:**
- Grammar errors become *jarring* — they break reading flow
- Capitalization mistakes feel wrong instinctively
- The learner self-corrects *automatically*, without thinking

Sam Altman tweeting in lowercase is actually a **deliberate stylistic choice** by someone who already mastered the rules — that's different from a beginner who simply doesn't know them yet. Knowing the rule and breaking it intentionally is expertise. Not knowing the rule at all is still the beginner stage.

---

## Programming

| Stage | What They Ignore |
|---|---|
| Beginner | Exception handling, edge cases, code structure |
| Intermediate | Performance, modularity, testability |
| Advanced | Naturally writes small functions, handles errors, thinks about maintainability |

A beginner writes code that *works*. An expert writes code that *survives the real world*.

---

## Machine Learning

| Stage | Attention Mechanism Choice |
|---|---|
| Beginner | Doesn't know Flash Attention exists |
| Intermediate | Knows it exists but uses vanilla attention because it's simpler |
| Advanced | Defaults to **Flash Attention** naturally — it's just the obvious, correct choice at SOTA |

Flash Attention is now essentially the *standard* for serious ML work — it reduces memory from **O(n²) to O(n)** and runs significantly faster on modern GPUs. An expert reaches for it without debate, just like an expert programmer reaches for proper exception handling without being told.

---

## The Core Pattern

> **Beginners optimize for "does it work."**
> **Experts optimize for "does it work correctly, efficiently, and sustainably."**

The key insight is that best practices don't feel like *extra work* to experts — they feel like the *natural* and *obvious* way to do things. That shift in intuition is what separates intermediate from advanced practitioners, whether in English, coding, or machine learning.
