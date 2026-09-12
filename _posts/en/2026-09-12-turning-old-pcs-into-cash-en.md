---
audio: false
generated: true
image: false
lang: en
layout: post
title: Turning Old PCs into Cash
translated: false
type: note
---

Question: What can a ¥180–260 old PC actually do, and can you use it to make money?

Answer: **Yes. The trick is not the CPU power — it's using the machine as cheap infrastructure.** An i5-3470 + 8GB machine is weak for AI inference, but surprisingly useful for automation, hosting, scraping, monitoring, and small services.

### 💰 Things I'd actually consider monetizing

**1. Run small automation jobs**

```text
Customer
   ↓
Telegram / Web / API
   ↓
Your cheap PC
   ├── scraper
   ├── LLM API calls
   ├── data processing
   └── scheduled jobs
```

Examples:

* Price monitoring → sell alerts
* E-commerce inventory monitoring
* Website change monitoring
* Job/listing aggregation
* Automatic report generation
* Social/content monitoring
* Data collection + cleanup

The PC doesn't need to run the LLM. **Call an API for intelligence; use the ¥180 machine for everything around it.**

---

**2. Host small services**

Install:

```bash
Ubuntu
Docker
Caddy
Postgres
Redis
```

Then you can run:

* Discord/Telegram bots
* webhook endpoints
* small APIs
* internal dashboards
* cron workers
* databases
* monitoring
* personal VPN / network services

At ¥180 hardware cost, your infrastructure CAPEX is basically nothing.

---

**3. Build a "local worker" business**

This is particularly interesting.

Suppose you have 10 cheap PCs:

```text
                    ┌── worker 1
                    ├── worker 2
API → queue →───────┼── worker 3
                    ├── worker 4
                    └── worker N
```

Each worker can:

* fetch URLs
* process files
* run browser automation
* transcode media
* execute Python jobs
* run lightweight open-source models
* maintain persistent connections

You're effectively building a **tiny private compute cluster**.

The economics can be surprisingly good for workloads where CPU utilization is the bottleneck rather than GPU.

---

### 🕷️ 4. Web crawling / data products

This is probably one of the more realistic ways to turn cheap hardware into revenue.

For example:

```python
while True:
    urls = get_urls()

    for url in urls:
        html = fetch(url)
        data = extract(html)
        db.insert(data)

    time.sleep(60)
```

The value isn't the crawling itself.

It's:

```text
raw websites
     ↓
structured dataset
     ↓
historical data
     ↓
alerts / API / dashboard
     ↓
customers pay
```

Examples:

* competitor price history
* real-estate listings
* second-hand market prices
* supplier/product catalogs
* job listings
* game item prices
* domain/website monitoring

**Data aggregation is much more monetizable than "I have a server."**

---

### 🤖 5. AI agent worker

Given your agent work, this is probably the most interesting use.

Don't try:

```text
i5-3470
   ↓
run 70B model
```

😂

Instead:

```text
cheap PC
   ↓
agent runtime
   ├── browser
   ├── filesystem
   ├── shell
   ├── cron
   ├── queue
   └── API calls → powerful LLM
```

The cheap machine becomes a **persistent agent execution environment**.

For example:

```bash
docker run my-agent-worker
```

The agent can continuously:

```text
watch inbox
    ↓
classify task
    ↓
call LLM
    ↓
execute tools
    ↓
save result
    ↓
notify user
```

That's a much better use of ¥180 than trying to squeeze tokens/sec out of an ancient CPU.

---

### 🧪 6. Use it as a disposable sandbox

This has real value too.

You can throw random software at it:

```bash
docker run ...
git clone ...
npm install ...
pip install ...
```

If it gets destroyed:

```text
rm -rf machine
```

Who cares?

You can use the box for:

* CI runners
* untrusted code experiments
* reverse engineering
* testing Linux packages
* browser automation
* build jobs
* staging environments

Your expensive workstation stays clean.

---

### ⚡ But there is one important problem

**Electricity.**

A ¥180 computer isn't necessarily cheap if it consumes 70–100W continuously.

At 80W:

```text
0.08 kW × 24 × 365
≈ 701 kWh/year
```

At ¥0.60/kWh:

```text
≈ ¥421/year
```

So the economics are:

```text
hardware:       ¥180
electricity:    potentially ¥400+/year
```

The hardware is almost irrelevant.

**Your real goal is >¥50–100/month of value per machine.**

---

## What I would do with this exact machine

I'd pay the **¥180 without the GT705** and turn it into a Linux box.

Then:

```bash
# OS
Ubuntu Server / Debian

# infrastructure
docker
caddy
postgres
redis

# your stuff
agent-worker
crawler
cron
telegram-bot
monitoring
```

Then look for a workload where **one machine can produce a measurable business output**.

For example:

```text
¥180 PC
   ↓
crawl 10,000 listings/day
   ↓
normalize + deduplicate
   ↓
store historical prices
   ↓
alert customers
   ↓
¥99/month/customer
```

One customer already pays for the hardware many times over.

**Don't buy the PC first and then ask what it can mine. Find the profitable workload first, then buy 1/10/100 machines as needed.**

And **don't buy the GT705 for ¥80**. It doesn't meaningfully change this strategy.
