---
audio: false
generated: true
image: false
lang: en
layout: post
title: Google Calendar slot length and timezone
translated: false
type: note
---

Question: For Google Calendar appointment scheduling links (like the one you set up), can I shorten the slot to e.g. 30 min so I get two per day, and does the booking page auto-convert to each visitor's local timezone?

Answer:

Yes on both, with one nuance.

**Slot length / multiple slots per day.** In the appointment schedule editor, "Appointment duration" controls slot length. Set it to 30 min and define an availability window — the system auto-generates back-to-back slots inside that window. If you want exactly *two* 30-min slots per day (not four), don't just set duration to 30 with an 11:00–12:00 window — that yields two slots, which is what you want. But if you want them spaced out (e.g. one at 11:00, one at 15:00), add two separate availability windows for the same day. You can also set "Buffer time" between appointments and a per-day "Maximum bookings per day" cap (set it to 2) to hard-limit it regardless of window size.

So for your 11–12 case: duration 30 min + window 11:00–12:00 → exactly two slots (11:00, 11:30). Clean.

**Timezone.** Yes — the public booking page auto-detects the visitor's browser timezone and displays slots in their local time. There's a timezone selector at the top of the booking page they can override. You define availability in *your* calendar's timezone; Google handles the conversion per-visitor. This is the part that makes it nice for talking to someone like Reni on a Google team if they're in a different zone — neither of you does mental math.

One caveat worth knowing: the auto-detection is browser-based, so if a visitor's system clock/timezone is misconfigured (VPN, traveling), they may see the wrong local time until they manually pick their zone from the selector. Rare, but it happens.

Practical setup for your case: 30-min duration, "Maximum bookings per day" = 2, add a buffer if you don't want them adjacent, and optionally cap total bookings or set a booking window (e.g. "can't book less than 4 hours out") so people don't grab a slot 5 minutes before.

References:

- [Create an appointment schedule in Google Calendar](https://support.google.com/calendar/answer/10729749)
