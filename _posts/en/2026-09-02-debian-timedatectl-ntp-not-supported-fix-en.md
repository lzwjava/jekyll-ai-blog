---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debian timedatectl NTP not supported fix
translated: false
type: note
---

Question: Debian says `timedatectl set-ntp true` is not supported.

Answer: That's usually because **no NTP synchronization service is installed/running**. `timedatectl` itself doesn't necessarily provide NTP.

First check:

```bash
timedatectl
```

and:

```bash
systemctl status systemd-timesyncd
```

### If `systemd-timesyncd` exists

Try:

```bash
sudo systemctl enable --now systemd-timesyncd
sudo timedatectl set-ntp true
```

Then:

```bash
timedatectl
```

### If `systemd-timesyncd` is not installed

Since your Debian installation currently seems to have limited APT repositories, you can simply **set the clock manually** for now:

```bash
sudo timedatectl set-timezone Asia/Shanghai
sudo timedatectl set-time '2026-09-02 03:12:00'
```

Check:

```bash
date
timedatectl
```

Once you fix your APT repository configuration, install an NTP client. I would use `chrony`:

```bash
sudo apt update
sudo apt install chrony
sudo systemctl enable --now chrony
```

Then:

```bash
chronyc tracking
```

You should eventually see a valid `Reference ID` and a small `System time` offset.

**Given your current situation, I'd fix APT first.** Once `apt install openssh-server` works, installing `chrony` will also work.
