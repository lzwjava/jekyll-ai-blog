---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alarm Tiers by Consequence and Irreversibility
translated: false
type: note
---

Question: Should reminders be split into distinct escalation tiers (no-alert markdown todo → light phone notification → loud alarm) because different information needs different processing effort, and does this match my experience that most soft alarms get dismissed without consequence while a "meat is burning" alarm needs to be unmissable, even though existing alarms have labels I don't read when busy?

Answer:

Yes, and the reasoning is correct — but the bug you found is more precise than "3 tiers." It's this:

**Your tiers are sorted by importance. They should be sorted by (cost of missing) × (irreversibility).**

A forgotten todo costs you nothing physical — you just do it later. Burnt meat costs you: ruined food, a scorched pan, potentially a kitchen fire, smoke damage. These are not the same category of event and shouldn't share an escalation ladder just because both are "reminders."

**Why labels fail under load**

This is a known failure mode in human attention, not a discipline problem: under active cognitive load, low-salience channels get filtered before they reach conscious processing (the same mechanism as the cocktail-party effect). A label requires you to *read* it, which requires you to *stop and look*, which is exactly the resource that's unavailable when you're mid-task. So any system that relies on "the alarm says what it's for" will fail precisely when it matters most, because reading is the bottleneck, not the sound.

**Fix: separate by sensory channel, not by label**

The signal that says "this one is different" has to be pre-attentive — recognizable without reading anything. Concretely:

```
Tier 0 — Log (markdown/notion/whatever)     → no notification, reviewed on your schedule
Tier 1 — Soft (Google Tasks push)            → glance-able, dismissible, no cost if ignored
Tier 2 — Loud, reserved-channel alarm        → used ONLY for physically irreversible events
```

The key constraint on Tier 2: **it must never be used for anything else.** The moment you use your "meat is burning" alarm sound/device for a meeting reminder, you've destroyed its signal value — now it's just another thing you tune out. Reserve one channel exclusively for consequence-carrying physical events (stove, oven, laundry that will mildew, something charging that shouldn't overheat), and its rarity becomes the alert.

**Practical implementation (AI-native, cheap)**

Use [ntfy.sh](https://ntfy.sh) (self-hostable, has an app, supports priority + custom sound) and split by topic, not label:

```python
import requests

def notify(channel: str, message: str, priority: str = "default"):
    requests.post(
        f"https://ntfy.sh/{channel}",
        data=message.encode("utf-8"),
        headers={
            "Priority": priority,       # "min"/"low"/"default"/"high"/"urgent"
            "Tags": "warning" if priority == "urgent" else "memo",
        },
    )

# Tier 1 — soft
notify("zhiwei-todo", "Reply to client email", priority="default")

# Tier 2 — reserved, never mixed with anything else
notify("zhiwei-kitchen-critical", "Meat has been on for 20 min — check now", priority="urgent")
```

Subscribe to `zhiwei-kitchen-critical` on a *separate device* (an old phone left in the kitchen, or a $10 smart plug + buzzer via Home Assistant) set to max volume, no vibrate-only, no silent mode override. Physically decouple it from your main phone, since your main phone is already saturated with notifications you've trained yourself to ignore.

If you want to go further toward your agentic direction: a small agent watching a stove-top temperature sensor or a timer you start via voice ("start meat timer") could auto-escalate — retry with increasing volume/frequency if not acknowledged within N seconds, similar to a PagerDuty escalation policy. That's a natural weekend project and fits directly into your "AI-native tooling" thread — the underlying pattern (bounded number of severity classes, each with a hardware-distinct channel, escalation-on-no-ack) is the same one distributed systems use for on-call alerting, just physically instantiated in your kitchen.
