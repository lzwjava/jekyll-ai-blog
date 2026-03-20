---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gitea PostgreSQL Docker 设置指南
translated: true
type: note
---

## 🐙 Gitea + PostgreSQL 设置指南

### 我们构建的内容

一个自托管的 Git 服务器（类似于轻量级的 GitHub），由 PostgreSQL 提供可靠的数据存储，在 Docker 中运行。

---

### 1. 架构

```
┌─────────────────────────────────────────────┐
│  Browser / Git Client                       │
│  http://192.168.1.36:3000  (web UI)         │
│  ssh://git@192.168.1.36:2222  (git SSH)     │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │   Docker: gitea     │
        │   (Gitea container) │
        │   Port 3000 → web   │
        │   Port 2222 → SSH   │
        └──────────┬──────────┘
                   │ host.docker.internal
        ┌──────────▼──────────┐
        │   PostgreSQL 16     │
        │   (host OS service) │
        │   Port 5433         │
        │   DB: gitea         │
        └─────────────────────┘
```

---

### 2. 逐步分解

#### 步骤 1：安装 PostgreSQL

```bash
sudo apt install -y postgresql postgresql-contrib
```

这会安装 PostgreSQL 16（Ubuntu 24.04 自带）。它会自动创建：
- 一个 `postgres` 超级用户（OS 用户 + DB 角色）
- 默认的 `main` 集群在端口 **5433**（不是 5432 — 端口 5432 有之前安装的过时/损坏集群）

#### 步骤 2：启动并启用 PostgreSQL

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

`enable` = 开机自启。我们需要等待片刻，让 socket 出现后再连接。

#### 步骤 3：创建数据库用户和数据库

```bash
sudo -u postgres psql -p 5433

CREATE USER gitea WITH PASSWORD 'gitea2026';
CREATE DATABASE gitea OWNER gitea;
GRANT ALL PRIVILEGES ON DATABASE gitea TO gitea;
```

| 内容 | 原因 |
|------|------|
| `CREATE USER` | 为 Gitea 专用 DB 角色 — 遵循最小权限原则 |
| `OWNER gitea` | Gitea 用户拥有 DB，可以创建/修改表 |
| `GRANT ALL` | 确保对 `gitea` 数据库的完全访问权限 |

#### 步骤 4：配置认证（`pg_hba.conf`）

PostgreSQL 通过 `/etc/postgresql/16/main/pg_hba.conf` 控制谁可以连接。我们添加了两条规则：

```
host gitea gitea 127.0.0.1/32 scram-sha-256
host gitea gitea 172.16.0.0/12 scram-sha-256
```

| 行 | 作用 |
|------|-------------|
| `127.0.0.1/32` | 允许本地连接（用于测试/调试） |
| `172.16.0.0/12` | 允许 Docker 容器连接（Docker 使用 172.16.x.x – 172.31.x.x 范围） |
| `scram-sha-256` | 现代密码认证（不是旧的 `md5`） |

编辑后，我们重启了 PostgreSQL：
```bash
sudo systemctl restart postgresql@16-main
```

#### 步骤 5：Gitea 的 Docker Compose

创建 `/opt/gitea/docker-compose.yml`：

```yaml
services:
  gitea:
    image: gitea/gitea:latest
    container_name: gitea
    restart: always
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__database__DB_TYPE=postgres
      - GITEA__database__HOST=host.docker.internal:5433
      - GITEA__database__NAME=gitea
      - GITEA__database__USER=gitea
      - GITEA__database__PASSWD=gitea2026
      - GITEA__server__ROOT_URL=http://192.168.1.36:3000
      - GITEA__server__SSH_DOMAIN=192.168.1.36
      - GITEA__server__SSH_PORT=2222
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - gitea_data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "2222:22"

volumes:
  gitea_data:
```

| 关键设置 | 说明 |
|---|---|
| `restart: always` | 崩溃或重启时自动重启 |
| `DB_TYPE=postgres` | 使用 PostgreSQL 而非 SQLite |
| `HOST=host.docker.internal:5433` | Docker 容器连接到宿主的 PostgreSQL |
| `extra_hosts` | 将 `host.docker.internal` 映射到 Docker 网关 IP |
| `ROOT_URL` | Gitea 用于链接/重定向的外部 URL |
| `SSH_PORT=2222` | 避免与宿主端口 22 的 SSH 冲突 |
| `gitea_data` volume | 仓库、配置等的持久存储 |

#### 步骤 6：开放防火墙端口

```bash
sudo ufw allow 3000/tcp comment 'gitea'
sudo ufw allow 2222/tcp comment 'gitea-ssh'
```

| 端口 | 用途 |
|------|---------|
| 3000 | Web UI (HTTP) |
| 2222 | Git over SSH (`git clone ssh://git@host:2222/repo.git`) |

#### 步骤 7：启动并验证

```bash
cd /opt/gitea && docker compose up -d
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
# 返回 200 ✅
```

---

### 3. 为什么选择 PostgreSQL 而非 SQLite？

|  | SQLite | PostgreSQL |
|---|---|---|
| **并发写入** | 单写入者，高负载下可能锁定 | 完全并发访问 |
| **数据安全** | 单文件，一个损坏风险 | ACID 合规，WAL 日志 |
| **可扩展性** | 适合个人使用 | 处理团队 + CI 工作负载 |
| **备份** | 复制文件 | `pg_dump` 进行正确备份 |
| **最适合** | 微型个人使用 | 任何严肃用途 |

---

### 4. 实用命令

```bash
# Gitea
docker ps --filter name=gitea          # 状态
docker logs gitea -f                   # 实时日志
cd /opt/gitea && docker compose restart
cd /opt/gitea && docker compose pull && docker compose up -d  # 更新

# PostgreSQL
sudo systemctl status postgresql@16-main
sudo -u postgres psql -p 5433 -d gitea  # 连接到 Gitea DB
sudo -u postgres pg_dump -p 5433 gitea > /tmp/gitea-backup.sql  # 备份

# 防火墙
sudo ufw status numbered
```

---

### 5. 快速检查清单

- [ ] 打开 `http://192.168.1.36:3000`
- [ ] 数据库字段已预填充 — 点击 **Install Gitea**
- [ ] 注册您的管理员账户（第一个用户默认是管理员）
- [ ] 创建您的第一个仓库
- [ ] 通过 SSH 克隆：`git clone ssh://git@192.168.1.36:2222/username/repo.git`

---

需要我设置 nginx 反向代理以使用干净的域名，还是配置自动 PostgreSQL 备份？