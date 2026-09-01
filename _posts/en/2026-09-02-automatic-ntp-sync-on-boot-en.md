---
audio: false
generated: true
image: false
lang: en
layout: post
title: Automatic NTP Sync on Boot
translated: false
type: note
---

Fixed. Here's the summary:

- Installed `systemd-timesyncd`
- Enabled it to start automatically on boot
- Activated NTP sync

Current status:
- `NTP service: active`
- `System clock synchronized: yes`
- `RTC time` was also updated to the correct synced time

From now on, every time the system boots it will automatically contact NTP servers and correct the clock, even though the hardware RTC is unreliable.