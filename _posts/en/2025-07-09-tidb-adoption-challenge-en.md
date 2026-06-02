---
audio: false
generated: true
lang: en
layout: post
title: TiDB's Niche in Distributed Database Adoption
translated: false
type: note
---

You're absolutely right about this being a significant adoption challenge for TiDB and similar distributed databases. This is actually a classic "chicken and egg" problem in the database world.

The migration cost barrier is real and substantial. Companies that start with MySQL or PostgreSQL often build their entire application architecture, ORM configurations, query patterns, and operational processes around these databases. Even though TiDB aims for MySQL compatibility, there are still subtle differences, performance characteristics to relearn, and new operational complexity to master.

The sharding path you mentioned is often seen as the "incremental" solution - companies can continue using familiar technology while scaling horizontally. Many engineering teams prefer this because:

- They keep their existing expertise and tooling
- Migration can be done gradually, table by table
- They maintain more control over data distribution
- Costs are more predictable

However, this creates a narrow adoption window for TiDB. Companies typically consider it when:

- They're already at massive scale where sharding becomes operationally complex
- They're building new systems from scratch (greenfield projects)
- They're hitting fundamental limitations of their sharded MySQL setup
- They have specific requirements like strong consistency across regions

This positioning does make TiDB somewhat niche compared to traditional databases. It's competing more with other distributed systems like CockroachDB, Spanner, or even NoSQL solutions rather than trying to replace every MySQL installation.

The sweet spot seems to be companies that know they'll need distributed scale from the beginning, or those where the operational overhead of managing sharded MySQL has become a significant burden.
