---
audio: false
generated: true
image: false
lang: en
layout: post
title: 7-Day Sleep Clock Reset Protocol
translated: false
type: note
---

Question: **How do I execute a 7-day sleep-clock reset?**

Answer:

Yes. I’d treat this like an **experiment**, not a vague “sleep better” goal.

The most important variable is **wake time**. Pick one time you can realistically maintain long-term.

### 7-day protocol

Assuming a target of **08:00 wake / ~00:00 sleep**:

| Time            | Action                                    |
| --------------- | ----------------------------------------- |
| **08:00**       | Get out of bed immediately                |
| **08:05–08:30** | Outdoor daylight + light walking          |
| **Morning**     | Coffee is fine; avoid using caffeine late |
| **Daytime**     | Normal work/exercise; don't stay in bed   |
| **14:00–15:00** | If necessary, ≤20 min nap                 |
| **22:30**       | Start reducing stimulation/light          |
| **23:00**       | Stop serious engineering/LLM work         |
| **23:00–00:00** | Shower, walk, read, simple activities     |
| **00:00**       | Bed                                       |
| **08:00**       | Repeat                                    |

### Days 1–2: establish the anchor

Don't worry if you can't sleep at midnight.

If you currently sleep at 03:00, you might initially get:

```text
03:00 → sleep
08:00 → wake
```

You'll be tired. **That's intentional.**

Don't "fix" the tiredness with a 3-hour afternoon nap.

### Days 3–4: sleep pressure starts doing the work

Because you've accumulated some sleep pressure, you should start becoming sleepy earlier.

If you're sleepy at 23:30:

```text
23:30 → bed
```

Don't stay awake until midnight merely to obey the schedule.

The rule is:

> **Fixed wake time, flexible bedtime within reason.**

### Days 5–7: stabilize

You should start seeing something like:

```text
Day       Sleep       Wake
--------------------------------
1         02:30       08:00
2         02:00       08:00
3         01:30       08:00
4         01:00       08:00
5         00:30       08:00
6         00:15       08:00
7         00:00       08:00
```

That's just an example. **Don't force this exact progression.**

---

## The three rules I'd make non-negotiable

### 1. Wake time > bedtime

If you only remember one thing:

```text
WAKE = fixed
SLEEP = follows sleepiness
```

Your wake time is the strongest daily anchor.

### 2. Morning light

Within roughly the first hour after waking, go outside.

Even better:

```text
08:00 wake
08:05 outside
08:05–08:30 walk
08:30 breakfast
```

Don't replace outdoor daylight with your monitor.

### 3. Protect the last hour

For someone doing intense AI/engineering work, this is probably particularly valuable.

At 23:00:

```text
NO:
  debugging CUDA
  reading papers
  benchmarking models
  "just one more experiment"

YES:
  shower
  walk
  boring book
  stretching
  preparing tomorrow's TODO
```

Before shutting down, dump unfinished thoughts:

```text
tomorrow.md

- investigate why kernel X is slower
- read paper Y section 4
- run benchmark Z
```

This gives your brain permission to stop.

---

## One trick that works surprisingly well

**Never negotiate with yourself while lying in bed.**

If you're awake and thinking:

> "Should I get up? Maybe check GitHub? Maybe watch one video?"

Don't.

Your bed becomes associated with:

```text
bed → sleep
```

rather than:

```text
bed → phone → YouTube → Reddit → GitHub → thinking → sleep
```

If you're unable to sleep for a while and becoming frustrated, get up, keep the light low, and do something boring. Return when sleepy.

---

## Track only 4 numbers

Don't turn this into another engineering project.

Every morning record:

```text
date
sleep_time
wake_time
energy_1_to_5
```

For example:

```text
Sep 10   01:40   08:00   2
Sep 11   01:15   08:00   3
Sep 12   00:50   08:00   4
...
```

After 7 days, look at the trend rather than judging individual nights.

### And don't sacrifice sleep for the reset

If you are severely sleep-deprived, don't deliberately keep yourself awake just to hit the schedule. Safety comes first—especially driving or doing anything requiring sustained attention.

If your sleep remains very irregular despite a consistent schedule, or you regularly can't sleep until very late even when exhausted, that's worth discussing with a clinician; delayed sleep-wake phase disorder is one possibility.

**My preferred experiment for you:** choose a wake time you can maintain **7 days/week**, get outside immediately after waking, eliminate long naps, and create a hard **"no new technical problems"** cutoff 60–90 minutes before bed. Do that for 7 days before changing anything else.
