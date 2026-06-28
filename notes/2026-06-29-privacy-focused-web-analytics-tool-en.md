---
audio: false
generated: true
image: false
lang: en
layout: post
title: Privacy-Focused Web Analytics Tool
translated: false
type: note
---

Question: What is Plausible Analytics (github.com/plausible/analytics)?

Answer:

Plausible is an open-source, privacy-focused web analytics tool — a lightweight Google Analytics alternative.

Core points:

- **Privacy-first**: No cookies, no persistent identifiers, GDPR/CCPA/PECR compliant by design. No personal data collected, so no cookie consent banner needed.
- **Lightweight script**: The tracking snippet is <1 KB — roughly 75x smaller than the GA bundle. Less page-weight, faster loads.
- **Single-page dashboard**: All key metrics (visitors, pageviews, sources, top pages, countries, devices) on one screen instead of GA's deep menu trees.
- **Self-hostable**: Apache 2.0 licensed core, ships a Docker Compose setup (Community Edition). You run it on your own box and own the data. There's also a paid managed cloud version that funds development.

Stack (relevant to you):
- **Backend**: Elixir / Phoenix
- **Data store**: ClickHouse (columnar OLAP — handles the event aggregation queries fast), PostgreSQL for app metadata
- **Frontend**: React + Tailwind

The ClickHouse + Elixir combo is the interesting architectural bit — events stream into ClickHouse, and the dashboard runs aggregation queries against the columnar store rather than scanning row-oriented tables. That's why it stays snappy at scale.

For your `lzwjava.github.io` blog/notes, self-hosted Plausible on your `192.168.1.36` workstation (or a small VPS) via Docker Compose would give you cookie-free traffic stats without GA's bloat or privacy baggage. The script just needs your domain whitelisted.

References:

- [plausible/analytics](https://github.com/plausible/analytics)
- [Plausible docs — self-hosting](https://plausible.io/docs/self-hosting)
