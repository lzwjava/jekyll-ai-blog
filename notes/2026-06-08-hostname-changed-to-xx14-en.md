---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hostname Changed to xx14
translated: false
type: note
---

Here's a summary of what you changed and what it affects:

## Hostname Change Summary

### What was done
```
OLD:  xiaoxin-XiaoXin-14-IAH8
NEW:  xx14
```

Two files were modified:
- `/etc/hostname` — via `hostnamectl set-hostname xx14`
- `/etc/hosts` — replaced old hostname with `xx14` so local resolution still works

### What this affects
- Your terminal prompt: now shows `xiaoxin@xx14` instead of `xiaoxin@xiaoxin-XiaoXin-14-IAH8`
- `hostname` command returns `xx14`
- Any network services that advertise the hostname (SSH, mDNS/Bonjour, Samba) will now use `xx14`
- SSH known_hosts entries pointing to the old name may need updating if you connect to this machine from other devices

### What does NOT change
- Your username (still `xiaoxin`)
- Your home directory (`/home/xiaoxin`)
- WiFi/network connectivity
- Hardware identification (MAC, serial, etc.)

### Good to know
- The change is permanent — survives reboots
- If you ever need to revert: `sudo hostnamectl set-hostname xiaoxin-XiaoXin-14-IAH8`
- Open a new terminal tab/shell to see the updated prompt (current sessions keep the old one)