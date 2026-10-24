---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hottest Distributed Systems Projects 2026
translated: false
type: note
---

**Question:** What are the hot distributed systems projects right now?

**Answer:**

Here's a breakdown by category, based on community traction and 2026 trends:

---

### 🔥 Messaging & Streaming

- **Apache Kafka** (~32,800 ⭐) — Still the dominant event streaming platform. In 2026, the Apache Kafka community accepted KIP-1150 for Diskless Topics, moving diskless Kafka from a vendor experiment to a community-supported direction — a major architectural shift toward S3-backed object storage.

- **Apache Flink** — Real-time analytics is moving into the stream, and Flink is central to powering operational AI with real-time context in 2026.

- **NATS** (~19,951 ⭐) — For applications where latency is critical, NATS.io is one of the fastest pub-sub messaging systems available, and is gaining ground as a Kafka alternative, especially for edge computing workloads.

---

### 🗄️ Distributed Databases

- **TiKV** (Rust) — A distributed transactional key-value database originally created to complement TiDB, supporting ACID transactions and Spanner-style consistency.

- **CockroachDB** (Go) — A distributed fault-tolerant SQL database built on a transactional and strongly-consistent key-value store.

- **Apache Iceberg** — Iceberg continues to be the open table format of choice for building lakehouse architectures, with massive organic adoption in 2025–2026; its simplicity and community are its success factors.

---

### ⚙️ Workflow Orchestration

- **Temporal** (~20,736 ⭐) — A durable execution engine for long-running distributed workflows. The rise of durable execution engines like Temporal in event-driven architectures with Kafka is a recognized trend in 2026.

---

### 💾 Distributed Storage

- **SeaweedFS** — A distributed storage system for object storage (S3), file systems, and Iceberg tables, designed to handle billions of files with O(1) disk access and effortless horizontal scaling.

- **JuiceFS** — A distributed POSIX file system built on top of Redis and S3.

- **Apache Ozone** — A scalable, distributed object store designed for lakehouse workloads, AI/ML, and cloud-native applications, with S3-compatible APIs and a Hadoop-compatible filesystem.

---

### 🧠 Distributed Vector Databases (AI-driven boom)

- **Qdrant** & **Milvus** — Qdrant is a vector similarity search engine and vector database; Milvus is an open-source vector database built to power embedding similarity search and AI applications. Both are seeing explosive growth due to the AI/LLM wave.

---

### 🧩 Consensus & Primitives

- **etcd** — The backbone key-value store for Kubernetes, heavily relied upon for distributed consensus in production clusters.
- **Hashicorp Raft** — A well-regarded Golang implementation of the Raft consensus protocol, widely used as a building block.

---

**TL;DR hot picks for 2026:** Diskless Kafka, Apache Flink (for agentic AI pipelines), Temporal, NATS, Qdrant/Milvus, and Apache Iceberg are the ones generating the most buzz.

---

**References:**

- [libhunt.com – Top Distributed System Projects](https://www.libhunt.com/topic/distributed-systems)
- [kai-waehner.de – Data Streaming Trends Q3 2026](https://www.kai-waehner.de/?p=10518)
- [linkedin.com – Open Source Data Infra Projects to Watch in 2026](https://vn.linkedin.com/in/giang-vu-1403)
- [awesome-distributed-system-projects (GitHub)](https://github.com/roma-glushko/awesome-distributed-system-projects)
- [trendshift.io](https://trendshift.io)
