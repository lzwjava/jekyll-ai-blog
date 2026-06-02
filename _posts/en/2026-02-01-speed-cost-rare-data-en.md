---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Balancing Speed Cost for Rare Data
translated: false
type: note
---

"Nearline" refers to a storage tier or access method that falls between **online** (immediately accessible) and **offline** (archived, requiring manual retrieval) storage.

**Key characteristics:**

- **Access speed**: Slower than online storage but faster than offline archives
- **Cost**: Cheaper than high-performance online storage but more expensive than cold/archival storage
- **Use case**: Data that's accessed infrequently (maybe once a month or quarter) but needs to be retrievable within seconds to minutes when needed

**Common examples:**

- Cloud storage tiers like Google Cloud's "Nearline Storage" or AWS's "Infrequent Access" tiers
- Tape libraries with robotic retrieval systems
- Secondary disk arrays for backup data

The term comes from distinguishing between data that's "online" (instantly available on primary storage) versus "nearline" (quickly retrievable but not instantly accessible) versus "offline" (requires physical intervention like loading a tape).
