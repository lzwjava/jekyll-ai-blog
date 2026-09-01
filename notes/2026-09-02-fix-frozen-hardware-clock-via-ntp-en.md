---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix frozen hardware clock via NTP
translated: false
type: note
---

The root cause is clear:

- **RTC (hardware clock) is dead/frozen** at `2011-08-04`.
- **No NTP sync client is installed** (`systemd-timesyncd` / `chrony` / `ntp` are all missing).
- So on every boot the system starts from the broken hardware clock and never corrects itself.

Run these commands to fix it:

```bash
sudo apt update
sudo apt install -y systemd-timesyncd
sudo systemctl enable --now systemd-timesyncd
sudo timedatectl set-ntp true
```

Then verify:

```bash
timedatectl status
```

You should see `NTP service: active` and eventually `System clock synchronized: yes`.

If your VM/ machine has no working RTC battery at all, you can also add a one-shot sync at boot so it corrects quickly even before network managers settle:

```bash
sudo systemctl edit systemd-timesyncd.service --force --full
```

And ensure it contains `After=network-online.target`, but the defaults usually work.

Copy-paste the install commands above and let me know the `timedatectl status` output.
