---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 服务器健康与容器状态报告
translated: true
type: note
---

## 🖥️ 服务器健康概览

**负载 / CPU**
- 负载：**0.50**（此前为 11 —— 风扇问题已解决 ✅）
- CPU：**99% 空闲**，已使用 6GB / 62GB 内存，剩余 56GB
- **交换分区**：107MB / 2GB —— 健康

---

## 📊 磁盘 — ⚠️ 已使用 84%（剩余 142GB）

| 类别 | 大小 |
|---|---|
| 总计 | 916GB |
| 已使用 | 728GB |
| 可用 | 142GB |

**问题：** 尚未达到临界点，但对于运行 Docker 的根分区而言，84% 的使用率已偏高。  
**可回收空间：**
- 22.9GB 未使用镜像（62% 的镜像可回收）
- 220MB 已停止容器的可写层
- 73MB 构建缓存

**建议：** 运行 `docker system prune -a` 清理旧镜像版本，或至少运行 `docker image prune -a`。

---

## 🐳 所有容器均正常运行（19/19）

| 容器 | CPU | 内存 | 状态 |
|---|---|---|---|
| nextcloud-app-1 | 0% | 206MB | ✅ 健康 |
| nextcloud-db-1 | 0% | 67MB | ✅ 健康 |
| nextcloud-redis-1 | 1% | 7MB | ✅ 健康 |
| live-server-app-1 | 0% | 21MB | ✅ 运行中 |
| live-server-web-1 | 0% | 22MB | ✅ 运行中 |
| live-server-database-1 | 0.1% | 183MB | ✅ 运行中 |
| live-server-redis-1 | 1% | 5MB | ✅ 运行中 |
| immich_server | 0.3% | 485MB | ✅ 健康 |
| immich_postgres | 0% | 147MB | ✅ 健康 |
| immich_machine_learning | 0.2% | 251MB | ✅ 健康 |
| immich_redis | 0.5% | 16MB | ✅ 健康 |
| LibreChat | 0% | 240MB | ✅ 运行中 |
| gitea | 0.2% | **980MB** | ⚠️ 内存偏高 |
| chat-mongodb | 0.8% | 151MB | ✅ 运行中 |
| chat-meilisearch | 0.6% | 133MB | ✅ 运行中 |
| rag_api | 0.2% | 141MB | ✅ 运行中 |
| vectordb | 0% | 43MB | ✅ 运行中 |
| searxng | 0% | 133MB | ✅ 运行中 |
| uptime-kuma | 2% | 162MB | ✅ 健康 |

---

## 🔴 发现的非关键问题

### 1. **Gitea —— 内存占用偏高（980MB）**
Gitea 使用了近 1GB 内存，是所有容器中最高的。这不常见——可能是正在执行 git gc 或重建索引。请检查内存占用是暂时偏高还是持续增长。

### 2. **SearXNG —— wikidata 引擎初始化失败**
```
ERROR: wikidata (init failed)
```
这是一个第三方引擎初始化失败，SearXNG 的其他引擎仍可正常工作，但你可以在设置中禁用 wikidata 引擎。

### 3. **LibreChat —— Meilisearch 配置缺失**
```
[indexSync] error Meilisearch configuration is missing
```
Meilisearch 服务正在运行（chat-meilisearch 容器已启动），但 LibreChat 的索引器未能正确连接。可能需要重新配置 LibreChat 环境变量中的 Meilisearch URL。

### 4. **llama 接口 /health → 404**
`GET http://localhost:8081/api/v1/health` 返回 404 —— jellyfin（端口 8096）工作正常。llama/Ollama 健康检查接口的路径可能不同。

### 5. **Nextcloud 33.0.2** ✅
已从 33.0.0 升级。Uptime-Kuma 现轮询 `/status.php` 而非 `/apps/dashboard/`。负载正常。

---

## 📋 快速待办事项

| 优先级 | 任务 | 命令 |
|---|---|---|
| 中 | 清理 22.9GB 未使用镜像 | `docker system prune -a` |
| 低 | 监控 Gitea 内存（980MB） | `docker stats gitea` |
| 低 | 修复 LibreChat Meilisearch 同步 | 检查 LibreChat 的 `MEILISEARCH_` 环境变量 |
| 低 | 在 SearXNG 中禁用 wikidata | 在 SearXNG 设置界面中操作 |
| 信息 | Nextcloud 数据库备份 | `/home/lzw/backup-nextcloud-db-20260407_165943.sql` |

希望我处理其中任一事项吗？