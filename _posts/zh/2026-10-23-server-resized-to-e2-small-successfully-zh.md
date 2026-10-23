---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 服务器已成功调整为e2-small
translated: true
type: note
---

已完成。服务器已调整大小、运行中并已验证。以下是完整摘要：

## ✅ e2-medium → e2-small — 完成

**已完成的操作**

1. **首先将外部 IP 提升为静态** (`live-server-ip`) — 它原本是临时的，所有 4 个域名都指向它，因此停止/启动会改变它。相同 IP `34.150.108.243`，DNS 未改动。（附加到运行中 VM 的静态 IP 是**免费**的。）
2. **停止 → 调整大小 → 启动** 虚拟机：现在为 `e2-small`，区域 asia-east2。
3. **重新启动整个服务栈** (`docker compose up -d`，位于 `/home/lzw/live-server/`) — app、web、database、redis、srs 全部运行中。
4. **添加了 2 GB 交换分区**（通过 `/etc/fstab` 持久化，swappiness 10）作为 OOM 保护 — RAM 减半至 2 GB，而这台机器运行 MySQL 8。
5. **为 app/web/database/redis 添加了 `restart: unless-stopped`** — 这次调整大小暴露出它们在重启后不会自动启动（只有 SRS 会）。已在 VM 上应用，并同步到你的本地 `docker-compose.yml`。

**验证**

- `https://funlive.io`、`www`、`web`、`api` → 从公网访问均返回 **200**
- MySQL 数据完好（`qulive`，87 MB，SELECT 1 正常）
- 容器全部 `Up`，所有 5 个容器的重启策略为 `unless-stopped`
- 当前内存：2 GB + 2 GB swap 中约使用 1 GB（之前为 4 GiB 中使用 1.5 GiB）

**成本影响（asia-east2 列表价 × 730 小时）**

| | e2-medium（之前） | e2-small（现在） |
| --- | --- | --- |
| vCPU (2 × $0.030519) | $44.56 | $44.56（封顶；按实际使用计费，约 17% 平均） |
| RAM (4→2 GB @ $0.004295) | $12.54 | **$6.27** |
| 自动 SUD 后（~30%） | ~$40 | **~$35–37** |
| 磁盘 + 快照 + GCS + 出站流量 | ~$4.4 | ~$4.4 |
| **预计总计** | **~$44–46/月** | **~$39–42/月** |

因此，直接节省约 **$4–8/月**，可能更多，因为 e2-small 是**共享核心**类型，按实际使用的 vCPU 秒计费（你的机器平均 CPU 使用率为 17%，所以 CPU 费用可能会低于配置的 2-vCPU 上限）。

**需要了解的取舍**

- **2 GB RAM**（之前为 4 GB）— 当前使用情况（~1 GB）下没问题，已添加 swap 作为后备。如果 MySQL/PHP 增长导致内存吃紧，请重新评估。
- **共享核心** — 你仍然可以突发到 2 vCPU，但持续高负载（例如 VM 上有大量并发观众/转码）的性能会比 e2-medium 的专用核心差。SRS 本身只是一个中继，因此这对流媒体影响不大。
- 还有一件事：VM 上部署的 `docker-compose.yml` 包含一个你的本地仓库副本没有的 `srs` 服务 — 仓库已与生产环境产生偏差。我只同步了重启策略的改动；下次处理仓库时请考虑合并其余更改。
