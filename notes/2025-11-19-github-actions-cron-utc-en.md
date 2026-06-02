---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GitHub Actions Cron Uses UTC Time
translated: false
type: note
---

**GitHub Actions scheduled workflows (using the `on: schedule:` trigger with cron syntax) always interpret the cron times in UTC (Coordinated Universal Time).**

There is no built-in support for specifying a different timezone directly in the workflow YAML. If you want a job to run at a specific local time (e.g., 9:00 AM PST), you must convert that to the equivalent UTC time and write the cron expression accordingly.

### Key points from official documentation:
- Scheduled workflows use POSIX cron syntax and run at specific **UTC times**.
- Example: `cron: '0 5 * * *'` runs daily at 5:00 AM UTC (not your local time).

This has been consistent for years and remains the case as of late 2025 — no native timezone parameter exists for the `schedule` event (unlike some other GitHub features like Dependabot).

[Events that trigger workflows - GitHub Docs](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
[Workflow syntax for GitHub Actions - GitHub Docs](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#on-schedule)
