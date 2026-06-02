---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Gitea PostgreSQL Docker 连接问题
translated: true
type: note
---

## 🔧 我如何修复 Gitea ↔ PostgreSQL 连接

### 错误

```
The database settings are invalid: dial tcp 172.17.0.1:5433: connect: connection timed out
```

Gitea（在 Docker 中运行）无法连接到 PostgreSQL（在主机上运行）。有三个独立问题阻塞了它。

---

### 问题 1：PostgreSQL 仅监听 `localhost`

**发生的情况：** PostgreSQL 的默认配置仅绑定到 `127.0.0.1`。这意味着它只接受来自主机本身的连接 — 而不是来自 Docker 容器的连接。

**如何发现：**
```bash
sudo ss -tlnp | grep 5433
# 输出显示：127.0.0.1:5433 — 仅 localhost！
```

**修复方法：**
```bash
# 在 /etc/postgresql/16/main/postgresql.conf 中更改：
# listen_addresses = 'localhost'        ← 旧的（注释掉的默认值）
listen_addresses = '*'                  ← 新（监听所有接口）
```

现在 PostgreSQL 在 `0.0.0.0:5433`（所有 IP）接受连接，而不是仅 `127.0.0.1`。

**为什么重要：** Docker 容器有自己的网络命名空间。从容器内部看，`127.0.0.1` 是容器本身 — 而不是主机。所以 Docker 内的 `localhost` ≠ 主机的 `localhost`。

---

### 问题 2：Docker 网络不匹配

**发生的情况：** Gitea 运行在自定义 Docker 网络（`gitea_default`）上，网关为 `172.22.0.1`，但 `host.docker.internal` 解析为 `172.17.0.1`（默认 `docker0` 桥接）。

**如何发现：**
{% raw %}
```bash
docker inspect gitea --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}: {{$v.Gateway}}{{"\n"}}{{end}}'
# 输出：gitea_default: 172.22.0.1

docker exec gitea sh -c "getent hosts host.docker.internal"
# 输出：172.17.0.1  host.docker.internal
```
{% endraw %}

Docker Compose 为每个项目创建自己的网络。`host.docker.internal` 映射使用默认桥接 IP，但来自自定义网络的流量并不总是能干净地路由到默认桥接。

**修复方法：** 通过将 `listen_addresses = '*'`，PostgreSQL 现在监听**所有**接口 — 包括自定义 Docker 网络可达的接口。无论哪个 Docker 网络连接，只要流量到达主机的 5433 端口，PostgreSQL 就会接受。

---

### 问题 3：iptables 阻塞连接

**发生的情况：** 即使修复了上述两个问题，连接仍然超时。真正的阻塞者是 iptables — Linux 防火墙悄无声息地丢弃了来自 Docker 到主机 5433 端口的数据包。

**如何发现：**
```bash
# 修复 listen_addresses 后，再试一次：
docker exec gitea sh -c "timeout 3 bash -c 'echo > /dev/tcp/host.docker.internal/5433'"
# 仍然失败

# 然后手动打开端口：
sudo iptables -I INPUT -p tcp --dport 5433 -j ACCEPT
# 再试 → 成功！
```

Docker 有自己的 iptables 链。当容器尝试连接主机时，数据包会通过主机的 `INPUT` 链。如果没有规则允许，它就会被丢弃。

**永久修复：**
```bash
sudo ufw allow from 172.16.0.0/12 to any port 5433 proto tcp comment 'postgresql-docker'
```

| 部分 | 含义 |
|------|------|
| `from 172.16.0.0/12` | 仅 Docker 网络（172.16.0.0 – 172.31.255.255） |
| `to any port 5433` | PostgreSQL 的端口 |
| `proto tcp` | PostgreSQL 使用 TCP |

这比向整个互联网开放 5433 端口更安全 — 只有 Docker 容器才能访问。

---

### 修复后的流程

```
1. 浏览器 → http://192.168.1.36:3000
              ↓
2. Gitea 容器（172.22.0.x）
   将 host.docker.internal 解析为 → 172.17.0.1
              ↓
3. 数据包击中主机的 iptables INPUT 链
   ufw 规则："allow from 172.16.0.0/12 to port 5433" → ACCEPT ✅
              ↓
4. PostgreSQL 在 0.0.0.0:5433 接收连接
   pg_hba.conf："allow gitea user from 172.16.0.0/12" → AUTHENTICATE ✅
              ↓
5. Gitea 连接到 DB，安装页面正常工作 🎉
```

---

### 总结

| 问题 | 症状 | 修复 |
|------|------|------|
| PostgreSQL 仅在 `localhost` | 容器无法访问主机的 loopback | `listen_addresses = '*'` |
| 自定义 Docker 网络 ≠ 桥接 | `host.docker.internal` 解析到错误的网关 | 已由 `listen_addresses = '*'` 处理 |
| iptables 丢弃 Docker → 主机流量 | 连接超时 | `ufw allow from 172.16.0.0/12 to port 5433` |
