---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Scaling PostgreSQL for ChatGPT's Users
translated: false
type: note
---

**Question:** What does the OpenAI blog post at https://openai.com/index/scaling-postgresql/ say?

**Answer:**

The blog post, titled **"Scaling PostgreSQL to power 800 million ChatGPT users"**, was published by OpenAI on January 22, 2026. It describes how OpenAI has scaled a single unsharded PostgreSQL database (running on Azure PostgreSQL Flexible Server) to handle massive global traffic for ChatGPT and their API, supporting 800 million users and millions of queries per second (QPS), mostly read-heavy.

### Key points from the article:

- **Scale achieved**
  PostgreSQL load increased >10× in the past year.
  They run **one primary instance** (for all writes) + **nearly 50 read replicas** spread across multiple regions.
  This setup delivers millions of QPS, low double-digit millisecond p99 latencies, near-zero replication lag, and five-nines availability.
  Only **one SEV-0 incident** in the last 12 months (caused by a 10× write surge during the ChatGPT ImageGen launch with 100 million new users).

- **Core architecture decisions**
  - No sharding of PostgreSQL itself (to avoid rewriting hundreds of application endpoints).
  - Write-heavy workloads are migrated to sharded systems like Azure Cosmos DB.
  - New services default to sharded databases from the start.
  - All remaining PostgreSQL usage is read-heavy; no new tables are added to it.

- **Main techniques used to scale and stabilize the system**
  - **Read offloading** → almost all reads go to replicas; critical reads protected from hitting the primary.
  - **Connection pooling** with PgBouncer (reduced average connection time from 50 ms to 5 ms).
  - **Aggressive caching** with cache locking/leasing to prevent thundering-herd cache-miss storms hitting the database.
  - **Multi-layer rate limiting** (application, proxy, pooler, query, ORM) and blocking of expensive query patterns.
  - **Workload isolation** — separate instances for high- vs low-priority traffic.
  - **Query & schema discipline** — avoid expensive joins, multi-table operations, full-table rewrites; enforce strict timeouts (e.g., 5 seconds for schema changes).
  - **High availability** — primary runs in HA mode with hot standby; multiple replicas per region with capacity headroom.
  - **Cascading replication** (in testing) to scale beyond ~50 replicas without overloading the primary via WAL streaming.

- **Biggest challenges mentioned**
  - Write spikes (cache misses, feature launches, backfills) overwhelming the single primary.
  - MVCC-related issues under heavy writes (bloat, autovacuum pressure, read/write amplification).
  - Connection exhaustion and idle connection storms.
  - WAL streaming CPU/network overhead limiting how many replicas can be added.
  - Noisy neighbors and risky schema changes.

- **Takeaway & future direction**
  OpenAI shows that PostgreSQL can reliably handle much larger read-heavy workloads than commonly believed — without sharding — when combined with careful engineering (replicas, caching, rate limiting, workload migration).
  They plan to keep migrating remaining write-heavy parts away from PostgreSQL and enable cascading replication in production.

In short, the post is an engineering deep-dive showing that a classic single-primary + many-replicas PostgreSQL architecture, when aggressively optimized, can support planetary-scale AI products like ChatGPT.

**References:**

- [Scaling PostgreSQL to power 800 million ChatGPT users](https://openai.com/index/scaling-postgresql/)
