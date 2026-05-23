---
audio: false
generated: true
image: false
lang: en
layout: post
title: No API for DMIT Traffic Stats
translated: false
type: note
---

**Question:** Does DMIT.io have an API to programmatically query server traffic/bandwidth usage (for a CN2 VPN server)?

**Answer:**

Short answer: **No public/official API.** DMIT doesn't expose a documented customer-facing API for querying traffic stats. Here's the full picture and your practical workarounds:

---

## What DMIT Actually Uses Underneath

DMIT runs a custom management panel built on **WHMCS** with **SolusVM** for VPS control. Both of these have APIs, but DMIT hasn't exposed them publicly to customers.

- **WHMCS** has an API at `/includes/api.php`, but it's an admin-only API — customers don't get credentials for it.
- **SolusVM** has a client API, but it's also gated — you'd need DMIT to enable it for your account.

---

## Your Real Options

### Option 1: Scrape the DMIT Client Area (quickest hack)

Log into `https://www.dmit.io/clientarea.php`, look at the service page for your VPS — it shows bandwidth used/remaining. You can automate scraping this with `requests` + `BeautifulSoup`:

```python
import requests
from bs4 import BeautifulSoup

SESSION_COOKIE = "YOUR_WHMCS_SESSION_COOKIE"

s = requests.Session()
s.cookies.set("WHMCSUser", SESSION_COOKIE, domain="www.dmit.io")

r = s.get("https://www.dmit.io/clientarea.php?action=productdetails&id=YOUR_SERVICE_ID")
soup = BeautifulSoup(r.text, "html.parser")

# Inspect the HTML to find the bandwidth element — usually something like:
bw = soup.find("div", {"class": "traffic-usage"})  # adjust selector
print(bw.text if bw else "Selector needs adjustment")
```

To get your session cookie: open DevTools → Network → any request to dmit.io → copy the `Cookie` header. Use `id=` from the URL when you click your service in the client area.

---

### Option 2: Monitor Traffic Directly on the VPS (most reliable)

Since you control the VPS, just measure from the server side. No API needed.

```bash
# Install vnstat for persistent monthly tracking
apt install vnstat
vnstat -i eth0 --json   # outputs JSON with daily/monthly stats
```

Or a one-liner to get current month's usage:
```bash
vnstat -m --json | python3 -c "
import json,sys
d=json.load(sys.stdin)
m=d['interfaces'][0]['traffic']['month']
print(f\"RX: {m[-1]['rx']/1e9:.2f} GB, TX: {m[-1]['tx']/1e9:.2f} GB\")
"
```

Set up a cron job + push to a webhook/Telegram bot if you want alerts when you're near quota.

---

### Option 3: SolusVM Client API (if DMIT enables it for you)

SolusVM has a client-facing API. Email DMIT support and ask if they expose the SolusVM API key for your VPS. If they do:

```python
import requests

# SolusVM client API endpoint (DMIT's SolusVM host — ask them for it)
SOLUSVM_URL = "https://vpsmanage.dmit.io/api.php"
KEY = "your_api_key"
HASH = "your_api_hash"

params = {
    "key": KEY,
    "hash": HASH,
    "action": "info",
    "status": "true",
    "bw": "true",      # bandwidth info
    "ipaddr": "true",
}
r = requests.get(SOLUSVM_URL, params=params)
print(r.text)  # XML response with <bw> field
```

The `bw` field in the SolusVM API response gives used/free/total bandwidth. This is the cleanest solution if they grant access.

---

### Option 4: Ask DMIT Support Directly

Their support is responsive and CN-friendly. Just ask: *"Can I get SolusVM API credentials for my VPS?"* Some DMIT plans expose this, some don't.

---

## TL;DR

| Method | Reliability | Effort |
|--------|------------|--------|
| `vnstat` on VPS | ✅ Best | 5 min |
| Scrape client area | ⚠️ Fragile | 30 min |
| SolusVM API (if enabled) | ✅ Clean | Ask support |
| Official DMIT API | ❌ Doesn't exist | — |

For your use case (monitoring CN2 VPN traffic quota), **`vnstat` on the server + a cron job pushing to Telegram** is the most reliable path and takes 10 minutes to set up.