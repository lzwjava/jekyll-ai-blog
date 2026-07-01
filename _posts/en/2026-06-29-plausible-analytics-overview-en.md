---
audio: false
generated: true
image: false
lang: en
layout: post
title: Plausible Analytics Overview
translated: false
type: note
---

Question: Give me an intro to Plausible Analytics (github.com/plausible/analytics).

Answer:

Plausible is an open-source, privacy-first, lightweight web analytics tool — positioned as a Google Analytics alternative. Let me hit the parts that actually matter to you.

**The pitch**

- **Privacy-first**: no cookies, no persistent identifiers, GDPR/CCPA/PECR compliant out of the box. No cookie banner needed because it stores nothing on the visitor's device.
- **Lightweight**: the tracking script is <1 KB (vs. Google Analytics' ~45 KB+). Big selling point for page-speed-sensitive sites.
- **Self-hostable** (AGPLv3) or use their paid managed cloud. The repo is the actual product, not a stripped community edition.

**Stack — this is the interesting bit for you**

- **Backend: Elixir / Phoenix.** This is a real-world, production Elixir codebase at scale — worth reading if you're curious about the BEAM/OTP concurrency model. They lean on Phoenix LiveView for the dashboard (server-rendered reactive UI, minimal JS).
- **Analytics store: ClickHouse.** This is the part most relevant to your interests. All event data goes into ClickHouse, a columnar OLAP database built for fast aggregations over billions of rows. Postgres holds app/config/user data; ClickHouse holds the firehose. Studying how they model events, partition by time, and write aggregation queries is a solid lesson in OLAP schema design.
- **Frontend**: React for the dashboard widgets, Tailwind.

**Architecture mental model**

```
tracker.js (<1KB) ──POST──> /api/event (Phoenix)
                                  │
                    ┌─────────────┴─────────────┐
                Postgres                    ClickHouse
            (users, sites,            (pageviews, events —
             config, billing)          columnar, append-only)
                                            │
                                    Phoenix LiveView dashboard
                                    (aggregation queries on read)
```

The core trick: ingestion is a thin append path; all the heavy lifting is push-down aggregation queries against ClickHouse at dashboard-render time, rather than precomputing rollups everywhere.

**Self-host quickstart** (Docker Compose is the supported path):

```bash
git clone https://github.com/plausible/community-edition plausible-ce
cd plausible-ce
# generate SECRET_KEY_BASE
openssl rand -base64 48
# edit plausible-conf.env: BASE_URL, SECRET_KEY_BASE, etc.
docker compose up -d
```

Note: the self-hosted distribution lives in a separate repo (`plausible/community-edition`) which pins the main `plausible/analytics` image plus Postgres + ClickHouse services. The main repo is the source.

**Why it's worth a look for you specifically**

1. Production Elixir + ClickHouse is a clean reference architecture for any high-write, read-aggregate system — directly transferable if you ever build an LLM-usage/telemetry analytics layer (you're consuming ~3B tokens in total; you'd want exactly this shape of store for per-request event analytics).
2. The ClickHouse event schema and query patterns are a compact, real lesson in OLAP design.
3. The privacy/no-cookie counting approach (how they dedupe unique visitors without persistent IDs — a daily-rotating salted hash of IP + user-agent + domain) is a neat constraint-driven design.

I'd skim `lib/plausible/` (Elixir core) and the ClickHouse migrations first — that's where the substance is.

I should note I'm answering from general knowledge of the project rather than a fresh read of the current repo state; if you want, I can pull the live README and current schema/migrations to verify specifics like the exact CE setup steps and ClickHouse table definitions.

References:

- [plausible/analytics](https://github.com/plausible/analytics)
- [plausible/community-edition](https://github.com/plausible/community-edition)
