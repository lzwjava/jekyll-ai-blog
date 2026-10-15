---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 带死端口的健康在线服务器
translated: true
type: note
---

它已经在运行了——而且很健康。以下是当前状态：

## 状态

| 服务 | 容器 | 状态 |
|---|---|---|
| PHP 8.5-FPM 应用 | `live-server-app-1` | 运行45小时 |
| nginx | `live-server-web-1` | 运行2天 |
| MySQL 5.7 (`qulive`) | `live-server-database-1` | 运行2天 — 23个表，2个用户 |
| Redis 7 | `live-server-redis-1` | 运行2天 |

## 冒烟测试（全部通过）

```
GET  /            -> 200  {"app":"live-server","status":"migrated from CI3"}
GET  /home        -> 200
GET  /users/1     -> 200  {"status":"object_not_exists", ...}   (数据库往返正常)
POST /users/list  -> 200
POST /login       -> 200
GET  /lives/count -> 200  {"count":"0"}
GET  /static/     -> 200  (前端 dist 卷已挂载)
```

**入口：`http://localhost:8088`**（nginx → `app:9000` fastcgi）。

## 发现一个实际问题

`docker-compose.yml:21` 将 `"8082:80"` 映射到 `app` 服务，但该镜像是 `php:8.5-fpm`，**没有 nginx**——容器内没有任何服务监听80端口（只有 `:9000`）。因此 `http://localhost:8082` 接受连接后立即重置：

```
> GET / HTTP/1.1
* Recv failure: Connection reset by peer
```

仓库中没有其他地方引用 8082，所以这是一个无效映射。两个选项：

1. **移除该映射** — 8088 是唯一的入口（最干净）。
2. **重新映射到 FPM** — `"9000:9000"`，如果你希望将来直接用主机侧的 nginx 指向它。

需要我删除无效的 `8082:80` 映射吗？否则我会保持容器不变，因为一切都在正常服务。