---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 闲鱼机器人监控指南
translated: true
type: note
---

**问题：** 如何构建一个监控闲鱼二手市场的机器人？

**回答：**

主要有两种方法——使用现成的爬虫服务（最简单）或构建自己的 Python 机器人（最具控制力）。以下是完整说明：

---

## 方法 1：使用 Apify 爬虫（无需代码 / 低代码）

Apify 上的 **Xianyu / Goofish Listings Scraper** 可让您收集结构化的列表数据，用于价格研究和趋势监控。它支持匿名首页信息流抓取（无需登录）以及使用淘宝会话 Cookie 进行带身份验证的关键词搜索。

导出的数据包括：`itemId`、`title`、`price`（人民币）、`area`、`sellerName`、`wantCount`、`publishedAt`、`categoryName` 等。

您可以在 Apify 上安排定时运行，并通过 Webhook 将结果发送到 Telegram、Google Sheets 或 Slack——无需编写代码。

---

## 方法 2：构建自己的 Python 机器人

这是最灵活的方法。以下是完整的架构：

### 步骤 1 — 选择数据源

| 方法 | 优点 | 缺点 |
|---|---|---|
| Apify Actor API | 可靠、持续维护 | 约 $2/1,000 条列表 |
| 直接 HTTP 抓取 | 免费 | 需要淘宝登录 Cookie、容易失效 |
| Selenium / 浏览器自动化 | 处理 JavaScript | 速度慢、有验证码风险 |

闲鱼不提供官方 API，因此爬虫的工作方式是以买家身份打开列表页面，并让页面自行执行其签名的 API 握手。

### 步骤 2 — 核心机器人结构（Python）

```python
import requests
import sqlite3
import time
from apify_client import ApifyClient

# --- 配置 ---
APIFY_TOKEN = "your_token"
TELEGRAM_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"
KEYWORDS = ["iPhone 15", "Nintendo Switch"]
CHECK_INTERVAL = 300  # 秒

# --- 用于跟踪已见列表的数据库 ---
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
                        f"❤️ {item.get('wantCount', 0)} 想要\n"
                        f"🔗 {item['url']}"
                    )
                    send_telegram(msg)
        time.sleep(CHECK_INTERVAL)

monitor()
```

### 步骤 3 — 添加价格过滤器

```python
# 仅当价格低于阈值时提醒
MAX_PRICE = {"iPhone 15": 4000, "Nintendo Switch": 1500}

if item["price"] <= MAX_PRICE.get(kw, float("inf")):
    send_telegram(msg)
```

### 步骤 4 — 处理身份验证（用于关键词搜索）

为避免登录提示，您可以使用保存到 JSON 文件中的淘宝/闲鱼会话 Cookie，如果会话过期，机器人可以通过 Telegram 请求二维码登录。

### 步骤 5 — 部署与定时调度

一个可靠的生产架构使用 **调度器**（cron 或 APScheduler）→ **爬虫**（带代理）→ **数据库**（SQLite 或 PostgreSQL）→ **警报引擎**（Telegram/电子邮件）。

---

## 方法 3：使用现有的开源机器人

**Goofish Watcher** 是一个开源的 Discord 机器人，可监控闲鱼上的列表并发送 DM 提醒。功能包括可配置的关键词搜索、包含/排除过滤器、价格范围过滤、基于 AI 的列表验证、去重以及灵活的扫描间隔（60/180/360 分钟）。

```bash
# 使用 Docker 快速开始
git clone https://github.com/Microck/goofish-watcher
docker compose up -d
```

---

## 汇总表

| 方法 | 所需技能 | 成本 | 最适合 |
|---|---|---|---|
| Apify + Zapier/Make | 无需 | 约 $2/1k 条 | 快速设置 |
| 自定义 Python 机器人 | 中级 | 免费（+代理） | 完全控制 |
| goofish-watcher（开源） | 基础 Docker | 免费 | Discord 用户 |

---

**参考资料：**
- [Xianyu / Goofish Listings Scraper – Apify](https://apify.com/piotrv1001/xianyu-goofish-listings-scraper)
- [Goofish Xianyu Search Scraper – Apify](https://apify.com/fetch_cat/goofish-xianyu-search-scraper)
- [Goofish Scraper (per-item) – Apify](https://apify.com/gio21/goofish-scraper)
- [goofish-watcher – GitHub (Discord bot)](https://github.com/Microck/goofish-watcher)
- [XYSpy – Archived Telegram Xianyu Monitor](https://github.com/Microck/XYSpy)
- [Price Monitoring System Guide 2026 – DEV Community](https://dev.to/agenthustler/how-to-build-a-price-monitoring-system-with-python-in-2026-complete-guide-5d32)