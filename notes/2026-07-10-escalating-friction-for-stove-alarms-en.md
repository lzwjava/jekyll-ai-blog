---
audio: false
generated: true
image: false
lang: en
layout: post
title: Escalating Friction for Stove Alarms
translated: false
type: note
---

Question: You had multiple reminders set (todo → phone notification → alarm), got busy with work, and reflexively silenced the alarm — ending up with meat cooking for 1.5–2 hours and a smoke-filled house. Your theory: reminders need priority tiers, because if you stack too many, they all lose effectiveness through habituation. You want to add a "big house alarm" for stove/cooking scenarios specifically. Right? And you're curious about trying jerky.

Answer:

You're right, and there's a real mechanism behind it — it's the same problem as alert fatigue in monitoring systems (PagerDuty, on-call rotations). If every signal looks the same, your brain (or your on-call engineer) starts pattern-matching "dismiss" as the default action regardless of severity. The fix isn't more reminders, it's **differentiating consequence, not just volume**.

Your current stack:

```
markdown todo (no reminder) → soft phone notification (Google Tasks) → loud alarm (Clock app)
```

The problem: all three are **dismissible by the same motor action** — a tap or swipe, which your hand does on autopilot while your brain is in flow state. The escalation is in loudness, not in *friction to dismiss*. That's the actual bug.

The fix for cooking specifically: add a **physically decoupled, non-phone-dismissible tier**. Two options, ranked by effort:

**Option A — cheap, buy today (30 min setup)**
A mechanical kitchen timer or a dumb "hard to snooze" plug-in timer that cuts power to the induction stove/burner after N minutes. You physically cannot silence it from your phone, so it forces a manual walk-to-kitchen interrupt. ~$10-15 on Taobao/Amazon, zero code.

**Option B — build it (matches your instincts)**
ESP32 + relay module wired to the stove's power line (or a smart plug like Sonoff/Tuya with API access), triggered by a simple script:

```python
import time
import requests

COOK_DURATION_MIN = 40  # your meat's actual cook time
WARNING_AT = COOK_DURATION_MIN - 5

def cut_power(plug_ip):
    # Tasmota HTTP API example — replace with your plug's firmware API
    requests.get(f"http://{plug_ip}/cm?cmnd=Power%20Off", timeout=5)

def escalate(minute):
    if minute == WARNING_AT:
        # push notification, dismissible
        requests.post("https://ntfy.sh/your_topic", data="5 min left on the stove")
    if minute == COOK_DURATION_MIN:
        # hard cutoff — not dismissible from a phone
        cut_power("<IP_ADDRESS>")
        requests.post("https://ntfy.sh/your_topic", data="Stove power cut. Go check it.")

for m in range(COOK_DURATION_MIN + 1):
    escalate(m)
    time.sleep(60)
```

This is a genuinely small, useful CLI/agent tool — a `stove-guard` daemon that runs on your RTX 4070 box or even a Raspberry Pi Zero, watches a timer, and forces a hard interrupt at T+N. It fits your "20% energy for product experiments" bucket — a physical-world safety agent is a nice complement to your CLI agent portfolio (ww/iclaw/zz), and it's the kind of thing that could become a tiny open-source repo/blog post for AI·Live (agentic world extending into home automation, not just software).

The core principle to keep: **soft reminders should escalate in friction, not just volume.** A louder alarm you can swipe away in your sleep is not actually a higher-priority signal — it's the same signal, louder. The only reliable "priority 1" is one that requires a state change you can't do from your phone.

On jerky — since you're curious: it's actually a great use case for exactly this kind of monitoring, because dehydrator/oven-based jerky runs low-and-slow for 4-8 hours, which is a much higher-stakes unattended-cook scenario than a 1.5hr stovetop dish. Basic process: slice lean beef (flank or eye of round) thin against the grain (~5mm), marinate 4-12h (soy sauce, worcestershire, brown sugar, garlic, black pepper, optional cure #1 if you want shelf-stable/non-refrigerated storage), then dry at 60-70°C for 4-8h until it bends without snapping. If you want, I can help you build a proper dehydrator temp/time model or a jerky-specific version of the stove-guard script — that's a much better candidate for automation than a quick sauté, since a burnt 6-hour jerky batch is a much bigger loss than the pot you had last week.
