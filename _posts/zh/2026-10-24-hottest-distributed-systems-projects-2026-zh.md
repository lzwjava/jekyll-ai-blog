---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2026年最热门的分布式系统项目
translated: true
type: note
---

**问题：** 目前热门的 distributed systems 项目有哪些？

**回答：**

以下是按类别分类的细分，基于 community traction 和 2026 trends：

---

### 🔥 Messaging & Streaming

- **Apache Kafka** (~32,800 ⭐) — 仍然是主导的 event streaming platform。在2026年，Apache Kafka 社区接受了关于 Diskless Topics 的 KIP-1150，将 diskless Kafka 从 vendor experiment 转变为 community-supported direction —— 这是一个朝向 S3-backed object storage 的主要架构转变。

- **Apache Flink** — Real-time analytics 正在进入 stream，而 Flink 在2026年对于通过 real-time context 驱动 operational AI 至关重要。

- **NATS** (~19,951 ⭐) — 对于 latency 关键的应用，NATS.io 是最快的 pub-sub messaging systems 之一，并逐渐成为 Kafka 的替代选择，特别是在 edge computing workloads 中。

---

### 🗄️ Distributed Databases

- **TiKV** (Rust) — 一个 distributed transactional key-value database，最初创建以补充 TiDB，支持 ACID transactions 和 Spanner-style consistency。

- **CockroachDB** (Go) — 一个 distributed fault-tolerant SQL database，构建在 transactional and strongly-consistent key-value store 之上。

- **Apache Iceberg** — Iceberg 持续是构建 lakehouse architectures 的 open table format 的首选，在2025–2026年间被大量 organic adoption；其 simplicity 和 community 是其成功因素。

---

### ⚙️ Workflow Orchestration

- **Temporal** (~20,736 ⭐) — 一个用于 long-running distributed workflows 的 durable execution engine。2026年，类似 Temporal 的 durable execution engines 在 event-driven architectures 与 Kafka 中的兴起是一个公认的趋势。

---

### 💾 Distributed Storage

- **SeaweedFS** — 一个用于 object storage (S3)、file systems 和 Iceberg tables 的 distributed storage system，设计用于处理 billions of files，具有 O(1) disk access 并且水平扩展 effortless。

- **JuiceFS** — 一个 built on top of Redis 和 S3 的 distributed POSIX file system。

- **Apache Ozone** — 一个 scalable, distributed object store，设计用于 lakehouse workloads、AI/ML 和 cloud-native applications，具有 S3-compatible APIs 和 Hadoop-compatible filesystem。

---

### 🧠 Distributed Vector Databases (AI-driven boom)

- **Qdrant** & **Milvus** — Qdrant 是一个 vector similarity search engine 和 vector database；Milvus 是一个 open-source vector database，构建用于 power embedding similarity search 和 AI applications。两者由于 AI/LLM 浪潮而经历 explosive growth。

---

### 🧩 Consensus & Primitives

- **etcd** — Kubernetes 的 backbone key-value store，在生产 cluster 中高度依赖 distributed consensus。
- **Hashicorp Raft** — 一个广受好评的 Golang 实现的 Raft consensus protocol，广泛用作 building block。

---

**TL;DR 2026年热门选择：** Diskless Kafka、Apache Flink (用于 agentic AI pipelines)、Temporal、NATS、Qdrant/Milvus 和 Apache Iceberg 是最受关注的。

---

**References:**
- [libhunt.com – Top Distributed System Projects](https://www.libhunt.com/topic/distributed-systems)
- [kai-waehner.de – Data Streaming Trends Q3 2026](https://www.kai-waehner.de/?p=10518)
- [linkedin.com – Open Source Data Infra Projects to Watch in 2026](https://vn.linkedin.com/in/giang-vu-1403)
- [awesome-distributed-system-projects (GitHub)](https://github.com/roma-glushko/awesome-distributed-system-projects)
- [trendshift.io](https://trendshift.io)