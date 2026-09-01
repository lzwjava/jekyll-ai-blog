---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting Debian System Clock
translated: false
type: note
---

Question: How to set the system clock on Debian 13.

Answer:

### Check current time

```bash
date
timedatectl
```

### Recommended: set the timezone

If you want **China time**:

```bash
sudo timedatectl set-timezone Asia/Shanghai
```

Check:

```bash
timedatectl
```

You should see:

```text
Time zone: Asia/Shanghai (CST, +0800)
```

### If the actual clock is wrong

Enable NTP time synchronization:

```bash
sudo timedatectl set-ntp true
```

Then:

```bash
timedatectl
```

Look for:

```text
System clock synchronized: yes
NTP service: active
```

This is preferable to manually setting the clock.

### Manually set it

If there is no network/NTP available:

```bash
sudo timedatectl set-time '2026-09-02 03:15:00'
```

Then verify:

```bash
date
```

**For your Debian Live installation, I'd do:**

```bash
sudo timedatectl set-timezone Asia/Shanghai
sudo timedatectl set-ntp true
timedatectl
```

If you're dual-booting **Windows + Debian**, there is one additional clock issue worth knowing: Linux normally treats the hardware RTC as UTC while Windows commonly treats it as local time.
