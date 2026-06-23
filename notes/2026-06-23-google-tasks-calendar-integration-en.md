---
audio: false
generated: true
image: false
lang: en
layout: post
title: Google Tasks Calendar Integration
translated: false
type: note
---

Yes, Google Tasks and Google Calendar are natively integrated. Tasks you create in the Google Tasks app (or the Tasks widget on iOS) show up in Google Calendar as green checkmark items — they appear on the due date you set, and you can see them inline with your calendar events on your Pixel.

A few things worth knowing about the integration:

- Tasks appear in Calendar only if they have a due date set. No due date = invisible in Calendar.
- They show at the top of the day (all-day section), not as timed blocks, unless you also set a specific time.
- Completing a task in Calendar marks it done in Tasks and vice versa — bidirectional sync.
- The green color is distinct from calendar event colors, which makes it easy to visually separate "things to do" from "meetings/events."

On Pixel with the default Google Calendar app this looks especially clean because Google's Material You theming gives tasks that consistent green checkmark style across the day view.

If you're building any automation around this — Google Tasks has a REST API (`tasks.googleapis.com`) and so does Calendar. You could programmatically create tasks with due dates via the API from your CLI agents (`ww`, `zz`, etc.) and they'll show up in Calendar automatically. Worth considering if you want to pipe reminders or TODOs from your agent workflows into your daily view.
