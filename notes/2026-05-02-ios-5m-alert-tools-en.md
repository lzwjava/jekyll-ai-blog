---
audio: false
generated: true
image: false
lang: en
layout: post
title: iOS Tools for Repeating Five-Minute Alerts
translated: false
type: note
---

Question: What tools on iOS can help set a repeating notification every 5 minutes (e.g., to check on a baby) without the hassle of manually setting alarms each time?

Answer:

You’re right that using the default **Clock app** repeatedly is annoying for this use case. There are better, more “systematic” solutions on iOS depending on how automated and flexible you want it.

---

## 1. Best Built-in Option: **Reminders**

This is the simplest native solution most people overlook.

### How to set it:

* Open Reminders → create a new reminder like “Check baby”
* Tap **Details**
* Enable:

  * **Date & Time**
  * Set time to now
  * Turn on **Repeat → Custom → Every 5 minutes**

⚠️ Limitation:

* iOS does NOT natively support repeating every 5 minutes directly in UI
* You can only choose things like daily/hourly (hourly works but not 5 min granularity)

👉 So this alone won’t fully solve your problem.

---

## 2. Best Native Automation: **Shortcuts**

This is the most powerful built-in method.

### Idea:

Create a **looping reminder system** using automation.

### Approach:

1. Open Shortcuts → Automation
2. Create **Personal Automation**
3. Choose:

   * “Time of Day” → set once (e.g., start working time)
4. Add actions:

   * Show Notification (“Check baby”)
   * Wait 300 seconds (5 minutes)
   * Repeat (use loop via multiple waits or recursive shortcut)

⚠️ Reality check:

* iOS **does not allow true infinite loops in background**
* Shortcuts will eventually stop or require confirmation

👉 So it works, but not perfectly reliable for long sessions.

---

## 3. Practical & Reliable: **Timer (Repeat Manually)**

Using **Clock → Timer** is actually underrated:

### Trick:

* Set timer to **5 minutes**
* When it rings → quickly tap **Repeat**

Pros:

* Very reliable
* Works in background
* Loud alert

Cons:

* Requires tapping every time (but only 1 tap)

👉 Honestly, many parents use this because it’s stable.

---

## 4. Best Solution Overall: Third-Party Interval Timer Apps

This is what you actually want.

### Examples:

* **MultiTimer**
* **Interval Timer**

### Why they are better:

* True **repeat every 5 minutes**
* Runs reliably in background
* No manual reset needed
* Can vibrate instead of loud alarm (less disruptive)

👉 This is the closest to a “professional solution”.

---

## 5. Creative Alternative: Apple Watch (if you have one)

Using **Apple Watch**:

* Set a repeating timer or use interval apps
* You get **haptic tap on wrist**
* Less disruptive than phone alarms

---

## Recommendation (based on your situation)

Since you:

* Are working on laptop
* Need low-friction reminders
* Don’t want repeated manual setup

👉 Best setup:

1. Install **MultiTimer**
2. Set:

   * Interval = 5 minutes
   * Repeat = infinite
   * Alert = vibration or soft sound

This gives you:

* Automation (no thinking)
* Reliability (no iOS limitation issues)
* Low parenting cognitive load

---

## Small but important note

A strict 5-minute check is useful, but:

* If your child is very young, **audio/video monitor** may be safer than relying only on timers
* Timer = backup, not primary safety system

---

If you want, I can design a **perfect Shortcuts automation workaround** (with near-infinite loop behavior) — but it’s a bit hacky.
