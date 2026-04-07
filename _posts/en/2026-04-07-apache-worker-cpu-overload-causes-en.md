---
audio: false
generated: true
image: false
lang: en
layout: post
title: Apache Worker CPU Overload Causes
translated: false
type: note
---

Looking at your `top` output, here's what's happening:

## Analysis

**12+ Apache2 workers all at 100% CPU** — this is the root cause of your fan noise.

Key observations:
- Processes have been running for **35-58+ minutes** at sustained 100% CPU — not a burst
- All are `www-data` (web server workers), not `root` (not startup/config)
- Memory per process is normal (~61-71 MB RES), so it's **not a memory leak**
- System RAM is fine (28 GB free), swap barely used

## Likely Causes (in order of probability)

1. **DDoS / flood attack** — someone hammering your server with requests
2. **Runaway PHP/CGI script** — an endpoint with an infinite loop or very expensive computation
3. **Slow resource exhaustion** — requests waiting on a slow backend (DB, upstream proxy), causing worker pileup

## Diagnose Now

Check what requests are actively being served:
```bash
# See open connections and what URLs are being hit
sudo apachectl status          # or /server-status if mod_status enabled
# OR
sudo cat /proc/$(pgrep -f apache2 | head -1)/net/tcp

# Check access log for flood patterns
sudo tail -f /var/log/apache2/access.log | cut -d'"' -f2 | sort | uniq -c | sort -rn | head -20

# Check which IPs are hammering you
sudo awk '{print $1}' /var/log/apache2/access.log | sort | uniq -c | sort -rn | head -20
```

Check if it's a PHP script looping:
```bash
# See what each worker is actually executing
sudo ls -la /proc/$(pgrep -f apache2 | head -1)/fd | grep php

# strace a worker briefly
sudo strace -p $(pgrep -f apache2 | head -1) -c -e trace=all &
sleep 3 && sudo kill %1
```

## Quick Mitigation

If it's a DDoS:
```bash
# Block top offending IPs
sudo ufw deny from <attacker-ip>
# or with mod_evasive / fail2ban if installed
```

If it's a runaway script — identify the URL from access logs and either block the route or fix the script.

What does `sudo tail -100 /var/log/apache2/access.log` show? That'll narrow it down quickly.