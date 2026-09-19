---
audio: false
generated: true
image: false
lang: en
layout: post
title: Score Went Up, Model Didn't Improve
translated: false
type: note
---

Let me explain it with almost no jargon.

## The idea in one picture

Think of GRPO like training a dog with treats.

1. You show the model a math problem.
2. You let it answer **4 times**.
3. Answers that are right get a treat (reward). Answers that are wrong get nothing.
4. The model nudges itself toward whatever got treats.

That's the whole loop. You did this **760 times**, for about 1 hour 45 minutes.

## What you were hoping for

You wanted the model to learn to **think step by step inside `<think> ... </think>` tags** before answering — like showing your work.

## What actually happened

**1. The model got 92% of the answers right at the end** (`eval_reward = 0.9238`).

Sounds great. But here's the problem:

**2. The model already knew how to do these problems before you started.** The problems were easy (single-digit addition, small multiplication). The untrained model already got ~83% right. So there was almost nothing new to learn.

**3. The `<think>` tags — the actual goal — never appeared. Not once.** That's the `reward_format = 0.0` line. Zero, in every single one of the 760 steps. Look at the final output you pasted:

```
--- (7 + 5) * 3 = ?
First, we perform the addition inside the parentheses: 7 + 5 = 12.
Then, we multiply the result by 3: 12 * 3 = 36.
So, the final answer is 36.
```

It shows its work in plain words, but there's **no `<think>` tag anywhere**. So the thing you were training for didn't happen.

**4. Most of the time, the model had nothing to learn from.** That's the `eval_frac_reward_zero_std = 0.85` line. Translation: in 85% of the groups, **all 4 answers were the same** — either all right or all wrong. If all 4 are right, there's nothing to prefer. If all 4 are wrong, you don't know which one is "less wrong." Either way, no lesson. Only 15% of the time did the model get a mix (some right, some wrong), which is the only situation where it can actually learn.

It's like giving a student a test where they already know 85% of the answers perfectly. They don't improve — they just confirm what they knew.

## So what did the model actually learn?

Almost nothing useful. It mostly learned to:
- Answer in **fewer words** (answers got shorter over training),
- **Stop printing a stray `</think>` tag** it used to emit.

That last one is why the score *looked* like it jumped. Your own notes in `run2.sh` say the same: the 83% → 92% "improvement" was mostly the model fixing a weird typing habit, **not** getting better at math.

## The one-sentence summary

> **The score went up, but the model didn't get smarter.** The problems were too easy (nothing to learn) and the `<think>` behavior you wanted was never taught, so it never appeared.

## How you already fixed it (in `run2.sh`)

Two changes, each targeting one problem:

| Problem | Fix in `run2.sh` |
|---|---|
| Problems too easy → nothing to learn | `--difficulty harder` (3-digit numbers, 2-digit multiplication) |
| `<think>` tags never appeared | `--format-warmup 512` (show the model 512 examples of the tag format *before* RL starts) |

And `headroom.py` is your tool to check, *before* training, whether the model finds a problem set hard enough to actually learn from (aim for the model getting roughly 20–70% right).

Want me to walk through what the **second run** (`run2.sh`) would show if you run it?