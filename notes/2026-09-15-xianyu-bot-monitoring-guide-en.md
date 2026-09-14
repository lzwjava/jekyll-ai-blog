---
audio: false
generated: true
image: false
lang: en
layout: post
title: Xianyu Bot Monitoring Guide
translated: false
type: note
---

**Question:** How do I build a bot to monitor the Xianyu (闲鱼) second-hand market?

**Answer:**

There are two main approaches — using a ready-made scraper service (easiest) or building your own Python bot (most control). Here's the full picture:

---

## Approach 1: Use Apify Scrapers (No-Code / Low-Code)

The **Xianyu / Goofish Listings Scraper** on Apify lets you collect structured listing data for price research and trend monitoring. It supports anonymous home-feed scraping (no login needed) and authenticated keyword search with a Taobao session cookie.

The data exported includes: `itemId`, `title`, `price` (CNY), `area`, `sellerName`, `wantCount`, `publishedAt`, `categoryName`, and more.

You can schedule runs on Apify and pipe results to Telegram, Google Sheets, or Slack via webhooks — no coding required.

---

## Approach 2: Build Your Own Python Bot

This is the most flexible approach. Here's the full architecture:

### Step 1 — Choose Your Data Source

| Method | Pros | Cons |
| --- | --- | --- |
| Apify Actor API | Reliable, maintained | Costs ~$2/1,000 listings |
| Direct HTTP scraping | Free | Requires Taobao login cookies, prone to breaking |
| Selenium / browser automation | Handles JS | Slow, captcha risk |

Xianyu doesn't expose an official API, so scrapers work by opening listing pages exactly as a buyer would and letting the page perform its own signed API handshake.

### Step 2 — Core Bot Structure (Python)

```python
import requests
import sqlite3
import time
from apify_client import ApifyClient

# --- Config ---
APIFY_TOKEN = "your_token"
TELEGRAM_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"
KEYWORDS = ["iPhone 15", "Nintendo Switch"]
CHECK_INTERVAL = 300  # seconds

# --- DB to track seen listings ---
conn = sqlite3.connect("xianyu.db")
conn.execute("CREATE TABLE IF NOT EXISTS seen (item_id TEXT PRIMARY KEY)")

def fetch_listings(keyword):
    client = ApifyClient(APIFY_TOKEN)
    run = client.actor("fetch_cat/goofish-xianyu-search-scraper").call(
        run_input={"keyword": keyword, "maxItems": 50}
    )
    return client.dataset(run["defaultDatasetId"]).iterate_items()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})

def is_new(item_id):
    cur = conn.execute("SELECT 1 FROM seen WHERE item_id=?", (item_id,))
    return cur.fetchone() is None

def mark_seen(item_id):
    conn.execute("INSERT OR IGNORE INTO seen VALUES (?)", (item_id,))
    conn.commit()

def monitor():
    while True:
        for kw in KEYWORDS:
            for item in fetch_listings(kw):
                iid = item["itemId"]
                if is_new(iid):
                    mark_seen(iid)
                    msg = (
                        f"🛒 <b>{item['title']}</b>\n"
                        f"💰 ¥{item['price']} | 📍 {item['area']}\n"
                        f"❤️ {item.get('wantCount', 0)} wants\n"
                        f"🔗 {item['url']}"
                    )
                    send_telegram(msg)
        time.sleep(CHECK_INTERVAL)

monitor()
```

### Step 3 — Add Price Filters

```python
# Only alert if price is below your threshold
MAX_PRICE = {"iPhone 15": 4000, "Nintendo Switch": 1500}

if item["price"] <= MAX_PRICE.get(kw, float("inf")):
    send_telegram(msg)
```

### Step 4 — Handle Auth (for keyword search)

To avoid login prompts, you can use cookies from a Taobao/Xianyu session saved to a JSON file, and the bot can request a QR code login via Telegram if the session expires.

### Step 5 — Deploy & Schedule

A solid production architecture uses a **scheduler** (cron or APScheduler) → **scraper** (with proxies) → **database** (SQLite or PostgreSQL) → **alerting engine** (Telegram/email).

---

## Approach 3: Use an Existing Open-Source Bot

**Goofish Watcher** is an open-source Discord bot that monitors Xianyu for listings and sends DM alerts. Features include configurable keyword search, include/exclude filters, price range filtering, AI-based listing verification, deduplication, and flexible scan intervals (60/180/360 minutes).

```bash
# Quick start with Docker
git clone https://github.com/Microck/goofish-watcher
docker compose up -d
```

---

## Summary Table

| Approach | Skill Required | Cost | Best For |
| --- | --- | --- | --- |
| Apify + Zapier/Make | None | ~$2/1k items | Quick setup |
| Custom Python bot | Intermediate | Free (+ proxy) | Full control |
| goofish-watcher (OSS) | Basic Docker | Free | Discord users |

---

**References:**

- [Xianyu / Goofish Listings Scraper – Apify](https://apify.com/piotrv1001/xianyu-goofish-listings-scraper)
- [Goofish Xianyu Search Scraper – Apify](https://apify.com/fetch_cat/goofish-xianyu-search-scraper)
- [Goofish Scraper (per-item) – Apify](https://apify.com/gio21/goofish-scraper)
- [goofish-watcher – GitHub (Discord bot)](https://github.com/Microck/goofish-watcher)
- [XYSpy – Archived Telegram Xianyu Monitor](https://github.com/Microck/XYSpy)
- [Price Monitoring System Guide 2026 – DEV Community](https://dev.to/agenthustler/how-to-build-a-price-monitoring-system-with-python-in-2026-complete-guide-5d32)
