---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnosis and Fixes for High CPU Usage
translated: false
type: note
---

Question: Explain the situation with high Apache CPU usage, Nextcloud dashboard loop, and Uptime-Kuma polling, and what the diagnosis and fixes mean.

Answer:

## What Happened (Simple)

Your server fan got loud because **Apache workers were stuck at 100% CPU**.
The investigation showed:

* Many `apache2` processes at **100% CPU**
* Running for **35–58 minutes** (not temporary)
* Memory usage normal → **not a memory leak**
* RAM mostly free → **CPU-bound issue**

Then the root cause was identified:

**Uptime-Kuma was repeatedly polling the Nextcloud dashboard endpoint:**

```
/apps/dashboard/
```

In **Nextcloud 33.0.0**, that dashboard loads a **PresetManager** that iterates through all apps/config.
Something in that path causes **very slow execution or infinite loop**.

So every health-check request:

```
Uptime-Kuma → /apps/dashboard/ → heavy loop → CPU 100%
```

Because Uptime-Kuma polls continuously, it **re-triggered the expensive code repeatedly**, stacking Apache workers.

Result:

* Workers pile up
* CPU spikes
* Load average climbs (11 → 9 → 3.6 after fix)
* Fan spins loudly

---

## Why CPU Dropped After Restart

When Apache restarted:

* Old stuck workers killed
* Queue cleared
* No more dashboard polling
* Load dropped quickly

That's why:

```
Load 11 → 3.68 in under 2 minutes
CPU idle 99%
Fan quiet
```

---

## Correct Fix (Important)

Don't use the dashboard as health endpoint.

### ❌ Bad (heavy UI page)

```
/apps/dashboard/
```

This loads:

* UI
* apps
* configs
* PresetManager
* loops

### ✅ Good (lightweight health endpoint)

```
/status.php
```

Returns:

```json
{"installed":true,"maintenance":false,"needsDbUpgrade":false}
```

Very fast, no UI, no loops.

So change Uptime-Kuma monitor to:

```
https://your-nextcloud/status.php
```

---

## The "Analysis" Section Explained

### 1. Why 12 workers at 100% CPU matters

Apache uses worker processes.
If 12 workers are stuck:

* All CPU cores busy
* New requests queue
* System load increases
* Fan spins

This is **worker exhaustion**.

---

### 2. The 3 possible causes listed

#### (1) DDoS / flood attack

Too many requests from internet.

Check with:

```
tail access.log
```

Look for repeated URLs/IPs.

---

#### (2) Runaway PHP script  ← THIS ONE

One endpoint looping or extremely slow.

Example:

```
/apps/dashboard/
```

Every request burns CPU.

---

#### (3) Slow backend

Workers waiting for:

* DB
* Redis
* upstream proxy

But CPU wouldn't be 100% usually — they'd be idle waiting.

So less likely.

---

## Diagnostic Commands Explained

### See what URLs are being hit

```
sudo tail -f /var/log/apache2/access.log
```

Shows requests in real-time.

---

### Find most frequent URLs

```
cut -d'"' -f2 | sort | uniq -c | sort -rn | head
```

Example output:

```
2000 GET /apps/dashboard/
50   GET /status.php
```

Then you know dashboard is the problem.

---

### Find attacking IPs

```
awk '{print $1}' access.log | sort | uniq -c | sort -rn
```

Shows:

```
5000 127.0.0.1
```

Means local monitor (Uptime-Kuma).

---

## Why This Caused Infinite CPU Loop

Because:

```
Uptime-Kuma (every 10s)
        ↓
GET /apps/dashboard/
        ↓
Nextcloud loads apps
        ↓
PresetManager iterates configs
        ↓
slow/infinite loop
        ↓
CPU 100%
        ↓
request not finished
        ↓
Uptime-Kuma sends another request
        ↓
more workers stuck
```

This is **feedback loop meltdown**.

---

## Final Fix Checklist

### 1. Change Uptime-Kuma URL

```
/apps/dashboard/
      ↓
/status.php
```

### 2. Update Nextcloud

You're on:

```
33.0.0
```

Upgrade to:

```
33.0.1+
```

Bug may already be fixed.

---

### 3. Optional: protect Apache workers

Limit max workers:

```
/etc/apache2/mods-enabled/mpm_prefork.conf
```

Example:

```
MaxRequestWorkers 20
```

Prevents runaway CPU.

---

## TL;DR

The fan noise came from:

```
Uptime-Kuma polling
        ↓
Nextcloud dashboard
        ↓
PresetManager loop
        ↓
Apache workers stuck
        ↓
CPU 100%
```

Fix:

```
Change monitor → /status.php
Update Nextcloud
```

This prevents the loop permanently.
