---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Discovery Command Summary
translated: false
type: note
---

All 4 surfaces updated and tested. Here's the summary:

**Command: `ww network discover`**

```
ww network discover              # Quick: ARP table + MAC OUI vendor lookup
ww network discover -r           # + reverse DNS hostnames
ww network discover -p           # + port probe + device type guessing
ww network discover -r -p        # Full discovery
ww network discover -s 10.0.0.0/24  # Custom subnet
```

**What it does:**
1. Gets local IP via UDP socket trick (no traffic sent)
2. Parses `arp -an` table (numeric, no DNS timeout)
3. Enriches with MAC OUI → vendor name (Apple, Xiaomi, TP-Link, Espressif, etc.)
4. `-r`: reverse DNS hostname resolution
5. `-p`: probes 8 common ports (SSH, HTTP, mDNS, VNC, AirPlay, iPhoneSync) → guesses device type
6. Filters out multicast/broadcast, sorts by IP
7. Prints aligned table

**Files changed:**
- `/Users/lzwjava/projects/ww/ww/network/discover.py` — new module
- `/Users/lzwjava/projects/ww/ww/main.py` — dispatch + help text (3 locations)
- `/Users/lzwjava/projects/ww/README.md` — command table row
- `/Users/lzwjava/projects/ww/completions/_ww` — zsh completion entry