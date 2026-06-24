---
audio: false
generated: true
image: false
lang: en
layout: post
title: Meituan Home Services System Analysis
translated: false
type: note
---

**Question:** After finishing a customer call with 美团家政 (Meituan Home Services), what are your thoughts on the system — especially around weekend demand surges, EV motorcycle battery issues, and worker availability?

**Answer:**

This is a logistics/ops problem, and it's actually a great domain to study for an AI startup later. Let me break down what you observed:

---

## What's happening here (systems view)

**Supply-demand mismatch on weekends:**
- Saturday/Sunday = 爆单 (order surge)
- 阿姨 (cleaners) are finite, and the good ones get booked out fast
- Meituan's matching algorithm probably doesn't do dynamic pricing or surge staffing well enough

**EV motorcycle battery = hidden constraint:**
- The worker couldn't come because her motorcycle ran out of charge
- She was coming from a far previous order
- Battery range → geographic radius → order assignment radius
- Meituan's dispatch likely treats workers as "available" without modeling battery state + distance realistically

This is essentially the same problem as **Uber's ETA model failing to account for driver state** — except instead of fuel/time, it's charge + distance from previous job.

---

## The actual failure modes

| Problem | Root cause | What good systems do |
|---|---|---|
| Weekend 爆单, not enough workers | No surge capacity planning | Dynamic pricing + pre-scheduling incentives |
| 阿姨 battery dead | Dispatch ignores EV state | Battery-aware routing (like Tesla fleet dispatch) |
| 前一单 too far away | No geographic clustering of orders | Cluster nearby jobs per worker per day |

---

## AI startup angle (your context)

If you ever build in this space — home services / O2O logistics — the real moat is:

1. **Worker state modeling** — battery level, fatigue, current location, not just "available/unavailable"
2. **Predictive surge staffing** — ML on historical order data to pre-position workers before weekends
3. **Dynamic re-routing** when a worker drops (like your 阿姨 did today)

Meituan has the data but moves slowly on infra. A vertical AI scheduler for home services is a real gap.

---

**Short-term practical:** For your own household, book 阿姨 early in the week for weekends, and confirm the day before — ask explicitly if she has reliable transport.
