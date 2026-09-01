---
audio: false
generated: true
image: false
lang: en
layout: post
title: timedatectl set-time ignored by NTP
translated: false
type: note
---

Question: `timedatectl set-time` succeeds or appears to run, but the clock immediately stays at the old time.

Answer: Most likely **NTP is still controlling the clock**, or the system's time service is resetting it.

Run this first:

```bash
timedatectl
```

Look for:

```text
NTP service: ...
System clock synchronized: ...
```

### Quick fix: turn NTP off, then set the time

```bash
sudo timedatectl set-ntp false
sudo timedatectl set-time '2026-09-02 03:12:00'
date
```

If `set-ntp false` says NTP isn't supported, check what time-sync service is running:

```bash
systemctl list-units --type=service | grep -E 'ntp|chrony|timesync'
```

Also:

```bash
ps aux | grep -E 'ntpd|chronyd|timesyncd'
```

### If you just want the correct time right now

You can bypass `timedatectl`:

```bash
sudo date -s '2026-09-02 03:12:00'
```

Then:

```bash
date
```

If **even `date -s` immediately jumps back**, something is actively synchronizing/resetting the clock.

One important point: if you only changed the timezone with:

```bash
sudo timedatectl set-timezone Asia/Shanghai
```

the **displayed time should change by the timezone offset**, but the underlying Unix timestamp does not change. That's different from setting the actual clock.

Paste the output of:

```bash
timedatectl
systemctl list-units --type=service | grep -E 'ntp|chrony|timesync'
```

and I can pinpoint what's overriding it.
