---
audio: false
generated: true
image: false
lang: en
layout: post
title: SQLite Replaces TiDB Locally
translated: false
type: note
---

Question: For the mem9 project, is the TiDB dependency unnecessary — could SQLite handle the job instead?

Answer:

**Short answer: Yes, for personal/local use, SQLite can absolutely replace TiDB in mem9 — and the community has already done exactly this.**

---

## Why mem9 Uses TiDB

mem9 (mnemos) uses TiDB Cloud Starter as its backing store, with the architecture keeping agent plugins stateless — all state lives in the mnemo-server, backed by TiDB.

The key features mem9 relies on TiDB for are:
- **Hybrid vector + keyword (full-text) search** — needed for memory recall
- **Multi-tenant shared memory** — multiple agents or users sharing one pool
- **Cloud-persistent, cross-device access**

---

## Why TiDB Feels Like Overkill for Local Use

SQLite excels on the desktop; TiDB is built for the cloud and scale. For a local agent, a `.sqlite` file offers the right balance of simplicity and capability.

With extensions like FTS5 (Full-Text Search) and `sqlite-vec` (Vector Search), SQLite provides a functional RAG stack in a single binary — no server dependency, no ports, no background processes, and single-file portability making backups trivial.

So for **local single-user use**, SQLite with `sqlite-vec` can replicate exactly what mem9 uses TiDB for:

| Feature | TiDB | SQLite (with extensions) |
|---|---|---|
| Vector search | ✅ Native | ✅ via `sqlite-vec` |
| Full-text search | ✅ Native | ✅ via FTS5 |
| Multi-agent isolation | ✅ by `agent_id` | ✅ by `agent_id` column |
| Cloud/cross-device | ✅ | ❌ (local only) |
| Zero-ops / no Docker | ❌ (needs Docker or TiDB Cloud) | ✅ |

---

## The Community Workaround: Local TiDB as a SQLite Stand-in

There is a documented approach where two databases are maintained in TiDB — a control plane (`mnemos`) and a data plane (`mnemos_tenant`) — and the tenant can be pointed to a local TiDB instance via an SQL update, keeping all data on the local machine inside Docker containers with no data leaving the host.

This means even the "official" local workaround still runs TiDB in Docker, which is heavier than SQLite.

---

## Verdict

- **TiDB is justified** if you want: cloud sync, cross-device access, multi-user/team sharing, or production-scale deployments.
- **TiDB is unnecessary lock-in** if you only want: local single-machine memory for personal agent use.
- **SQLite is sufficient** for the local case. The repository's `repository/` layer is abstracted behind an interface, so swapping the TiDB SQL implementation for a SQLite one is architecturally clean and feasible. If you were to scale this "memory" concept to a multi-tenant SaaS platform serving thousands of agents, that's the moment to move from SQLite to a distributed SQL database like TiDB — but for a local agent, SQLite is the right tool.

If you're self-hosting mem9 for personal use, contributing a SQLite backend adapter to the `repository/` package would be a reasonable and welcome improvement to eliminate the TiDB dependency entirely.

References:

- [mem9 GitHub Repository](https://github.com/mem9-ai/mem9)
- [Keep Memory Local: Building a Private OpenClaw Memory Hub with mem9 + TiDB](https://addozhang.medium.com/keep-memory-local-building-a-private-openclaw-memory-hub-with-mem9-tidb-5b305345b40a)
- [Local-First RAG: Using SQLite for AI Agent Memory with OpenClaw](https://www.pingcap.com/blog/local-first-rag-using-sqlite-ai-agent-memory-openclaw/)
