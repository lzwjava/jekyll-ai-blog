---
audio: false
generated: true
image: false
lang: en
layout: post
title: Forecasting with Accountability Loops
translated: false
type: note
---

Question: You set a calendar event a year ago as a future prediction/reminder, and now you're thinking you should build more habits like that — using calendar events to predict the future and check back on them. Is this a good system?

Answer:

Yes, and you're independently discovering something that serious forecasters do systematically. It has a name: **forecasting with accountability loops**.

---

## Why This Works

The core mechanism: **prediction → time capsule → review → calibration**.

Without the review step, your brain rewrites history ("I knew that would happen" = hindsight bias). The calendar event forces an honest audit.

Superforecasters (Tetlock's research, *Superforecasting*) do exactly this — write predictions with explicit probabilities, date them, review them, and track their **calibration score** over time. The review loop is what separates people who get better at predicting from people who just have opinions.

---

## What to Capture in Each Event

Don't just set a reminder. Write the full prediction at creation time:

```
Date: 2025-05-23
Prediction: Anthropic will cut Opus pricing by >30% within 12 months
Confidence: 75%
Reasoning: DeepSeek pressure, inference cost curves, API volume incentives
Review date: 2026-05-23
```

When you review, record:
- What actually happened
- Was your reasoning correct even if outcome was wrong?
- What would have changed your prediction?

---

## Suggested Categories for You

Given your trajectory:

**AI/Tech**
- Model capability jumps (GPT-5, Claude 4, Qwen 4 timeline)
- Price drops (your Anthropic prediction)
- Which labs survive/consolidate in 2 years

**Career**
- Where your income comes from in 12 months
- Whether you're still contracting or full-time AI role
- Token consumption rate (you're at 1.5B/yr now — what in 2026?)

**Personal projects**
- Which of your tools (ww, iclaw, zz, Hermes plugins) you're still using in 1 year
- Blog post count, notes count milestones

**Markets/macro**
- CNY/USD, China tech regulation, GPU export controls impact

---

## Simple System (Terminal-first for you)

Since you're already blog/GitHub-native:

```bash
# predictions.md in your blog repo
## 2025-05-23 | Confidence: 75%
**Prediction**: Anthropic cuts Opus price >30% by May 2026
**Review**: [fill in 2026-05-23]

## 2025-05-23 | Confidence: 60%
**Prediction**: Still using Hermes over Claude Code in 6 months
**Review**: [fill in 2025-11-23]
```

Calendar event = just the trigger to open `predictions.md` and fill in the Review field.

---

## The Real Compounding Value

After 2-3 years of this, you'll have:
1. A calibration score — do you actually know what you think you know?
2. A map of where your reasoning was systematically off
3. Intellectual honesty that's rare — most engineers have opinions, few have evidence about the quality of their opinions

You're already thinking in this direction. Formalizing it even slightly — just adding confidence % and written reasoning — makes it 10x more valuable than a bare calendar reminder.

References:
- [Superforecasting — Philip Tetlock](https://www.goodreads.com/book/show/23995360-superforecasting)
- [Calibration in forecasting — LessWrong](https://www.lesswrong.com/tag/calibration)
