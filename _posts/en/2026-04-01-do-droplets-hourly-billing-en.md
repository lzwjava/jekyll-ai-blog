---
audio: false
generated: true
image: false
lang: en
layout: post
title: DigitalOcean Droplets Hourly Billing Guide
translated: false
type: note
---

Question: Do DigitalOcean droplets charge monthly even if I use them for only a few days, or are they billed hourly?

Answer:

DigitalOcean **Droplets are billed hourly**, with a **monthly cap**. That means:

* You pay **only for the hours** the Droplet exists ⏱️
* But charges **stop increasing once they reach the monthly price** 💰
* If you delete early, you **do NOT pay the full month** ❌

### How it works

Example: a Droplet listed as **$24/month**

* Hourly rate ≈ $24 / ~730 hours ≈ **$0.033/hour**
* Use for 10 hours → pay about **$0.33**
* Use for 3 days (72h) → pay about **$2.38**
* Use whole month → capped at **$24**

So:

* Create → billed hourly
* Delete → billing stops immediately
* Keep running all month → hits monthly cap

### Important exceptions ⚠️

Some things **are monthly regardless**:

* Reserved IPs (when unused)
* Snapshots storage
* Block storage volumes
* Load balancers
* GPU droplets (still hourly but expensive)

But **normal droplets + GPU droplets** are still **hourly-based**.

### For your use case (download data → open H100 → delete)

Your idea is correct:

* open cheap droplet → download 100GB
* delete
* open H100 GPU → train
* delete

You only pay for **actual hours used**, not full month.

This is why people:

* spin up GPU for **2–6 hours** 🔥
* train
* destroy

Very cost-efficient.

Rule of thumb:

* running = paying
* stopped (but not deleted) = still paying
* deleted = stop paying
