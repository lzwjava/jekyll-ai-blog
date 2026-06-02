---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SQLite 在本地取代 TiDB
translated: true
type: note
---

问题：对于 mem9 项目，TiDB 依赖是否多余——SQLite 能否胜任这项工作？

回答：

**简短回答：是的，对于个人/本地使用，SQLite 完全可以替换 mem9 中的 TiDB —— 社区已经这样做了。**

---

## 为什么 mem9 使用 TiDB

mem9（mnemos）使用 TiDB Cloud Starter 作为其后端存储，架构保持 agent 插件无状态——所有状态都存在于 mnemo-server 中，由 TiDB 支持。

mem9 依赖 TiDB 的关键特性包括：
- **Hybrid vector + keyword (full-text) search** —— 用于 memory recall
- **Multi-tenant shared memory** —— 多个 agents 或用户共享一个池
- **Cloud-persistent, cross-device access**

---

## 为什么 TiDB 对于本地使用来说显得多余

SQLite 在桌面环境中表现出色；TiDB 是为云端和规模化构建的。对于本地 agent，一个 `.sqlite` 文件提供了简单性和功能性的最佳平衡。

使用 FTS5（Full-Text Search）和 `sqlite-vec`（Vector Search）等扩展，SQLite 在单个二进制文件中提供功能完整的 RAG 栈——无需服务器依赖、无需端口、无需后台进程，并且单文件可移植性使备份变得简单。

因此，对于**本地单用户使用**，带 `sqlite-vec` 的 SQLite 可以完全复制 mem9 使用 TiDB 所做的一切：

| 特性 | TiDB | SQLite (with extensions) |
|---|---|---|
| Vector search | ✅ 原生 | ✅ 通过 `sqlite-vec` |
| Full-text search | ✅ 原生 | ✅ 通过 FTS5 |
| Multi-agent isolation | ✅ 通过 `agent_id` | ✅ 通过 `agent_id` 列 |
| Cloud/cross-device | ✅ | ❌（仅本地） |
| Zero-ops / no Docker | ❌（需要 Docker 或 TiDB Cloud） | ✅ |

---

## 社区变通方案：本地 TiDB 作为 SQLite 的替代

有一种记录在案的方法，在 TiDB 中维护两个数据库——控制平面（`mnemos`）和数据平面（`mnemos_tenant`）——通过 SQL 更新可以将 tenant 指向本地 TiDB 实例，所有数据保存在本地机器的 Docker 容器中，数据不会离开主机。

这意味着即使是“官方”本地变通方案仍然在 Docker 中运行 TiDB，比 SQLite 更重。

---

## 结论

- 如果您需要 cloud sync、跨设备访问、多用户/团队共享，或生产规模部署，则**TiDB 是合理的**。
- 如果您只想要本地单机 memory 用于个人 agent 使用，则**TiDB 是多余的锁定**。
- **SQLite 对于本地情况已足够**。repository 的 `repository/` 层抽象在接口后面，因此将 TiDB SQL 实现替换为 SQLite 实现是架构上干净且可行的。如果您要将这个“memory”概念扩展到服务数千个 agents 的多租户 SaaS 平台，那就是从 SQLite 迁移到像 TiDB 这样的分布式 SQL 数据库的时刻——但对于本地 agent，SQLite 是正确的工具。

如果您为个人使用自托管 mem9，为 `repository/` 包贡献一个 SQLite 后端适配器将是一个合理且受欢迎的改进，完全消除 TiDB 依赖。

参考文献：

- [mem9 GitHub 仓库](https://github.com/mem9-ai/mem9)
- [Keep Memory Local: 使用 mem9 + TiDB 构建私有 OpenClaw Memory Hub](https://addozhang.medium.com/keep-memory-local-building-a-private-openclaw-memory-hub-with-mem9-tidb-5b305345b40a)
- [Local-First RAG: 使用 SQLite 为 OpenClaw 的 AI Agent Memory](https://www.pingcap.com/blog/local-first-rag-using-sqlite-ai-agent-memory-openclaw/)
