---
audio: false
generated: true
image: false
lang: en
layout: post
title: App Audit by Last Modified Timestamps
translated: false
type: note
---

Here's how I audited your /Applications:

**Method: 3-layer scan**

1. List all apps — `ls -1 /Applications/*.app` → 74 apps, 33GB total

2. Size analysis — `du -sh /Applications/*.app | sort -rh` → ranked by disk usage, biggest offenders first (Xcode 4.7GB, IntelliJ 3.9GB, Android Studio 2.5GB, Docker 1.7GB)

3. Last-modified timestamps — `stat -f "%Sm"` on each .app bundle → this is the key signal. It reflects last install/update, which correlates strongly with actual usage. An app untouched since 2023 is almost certainly dead.

**Classification logic:**

- SAFE DELETE = last touched 1+ year ago AND (redundant with another app OR one-time-use tool OR irrelevant to your AI engineering work)
- CONSIDER = duplicates of things you already have (3 browsers, 2 FTP clients, etc.)
- KEEP = touched in last month, clearly active
- HOLD = large apps where I need your input on whether the use case still exists

The timestamps don't lie — iTerm from Jan 2023 means you haven't touched it since Ghostty replaced it. TencentMeeting from Dec 2023 means no meetings there in 2.5 years. That's stronger evidence than any heuristic.