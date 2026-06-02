---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gitea PostgreSQL Docker Setup Guide
translated: false
type: note
---

## 🐙 Gitea + PostgreSQL Setup Guide

### What We Built

A self-hosted Git server (like a lightweight GitHub) backed by PostgreSQL for reliable data storage, running in Docker.

---

### 1. Architecture

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

### 2. Step-by-Step Breakdown

#### Step 1: Install PostgreSQL

```bash
sudo apt install -y postgresql postgresql-contrib
```

This installs PostgreSQL 16 (ships with Ubuntu 24.04). It auto-creates:

- A `postgres` superuser (OS user + DB role)
- A default `main` cluster on port **5433** (not 5432 — port 5432 had a stale/broken cluster from a previous install)

#### Step 2: Start & Enable PostgreSQL

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

`enable` = starts on boot. We had to wait a moment for the socket to appear before connecting.

#### Step 3: Create Database User & Database

```bash
sudo -u postgres psql -p 5433

CREATE USER gitea WITH PASSWORD 'gitea2026';
CREATE DATABASE gitea OWNER gitea;
GRANT ALL PRIVILEGES ON DATABASE gitea TO gitea;
```

| What | Why |
|------|-----|
| `CREATE USER` | Dedicated DB role for Gitea — follows least-privilege |
| `OWNER gitea` | Gitea user owns the DB, can create/modify tables |
| `GRANT ALL` | Ensures full access on the `gitea` database |

#### Step 4: Configure Authentication (`pg_hba.conf`)

PostgreSQL controls who can connect via `/etc/postgresql/16/main/pg_hba.conf`. We added two rules:

```
host gitea gitea 127.0.0.1/32 scram-sha-256
host gitea gitea 172.16.0.0/12 scram-sha-256
```

| Line | What it does |
|------|-------------|
| `127.0.0.1/32` | Allows localhost connections (for testing/debug) |
| `172.16.0.0/12` | Allows Docker containers (Docker uses 172.16.x.x – 172.31.x.x range) |
| `scram-sha-256` | Modern password auth (not the old `md5`) |

After editing, we restarted PostgreSQL:

```bash
sudo systemctl restart postgresql@16-main
```

#### Step 5: Docker Compose for Gitea

Created `/opt/gitea/docker-compose.yml`:

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

| Key Setting | Explanation |
|---|---|
| `restart: always` | Auto-restart on crash or reboot |
| `DB_TYPE=postgres` | Uses PostgreSQL instead of SQLite |
| `HOST=host.docker.internal:5433` | Docker container connects to host's PostgreSQL |
| `extra_hosts` | Maps `host.docker.internal` → Docker gateway IP |
| `ROOT_URL` | External URL Gitea uses for links/redirects |
| `SSH_PORT=2222` | Avoids conflict with host's SSH on port 22 |
| `gitea_data` volume | Persistent storage for repos, configs, etc. |

#### Step 6: Open Firewall Ports

```bash
sudo ufw allow 3000/tcp comment 'gitea'
sudo ufw allow 2222/tcp comment 'gitea-ssh'
```

| Port | Purpose |
|------|---------|
| 3000 | Web UI (HTTP) |
| 2222 | Git over SSH (`git clone ssh://git@host:2222/repo.git`) |

#### Step 7: Start & Verify

```bash
cd /opt/gitea && docker compose up -d
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
# Returns 200 ✅
```

---

### 3. Why PostgreSQL Over SQLite?

| | SQLite | PostgreSQL |
|---|---|---|
| **Concurrent writes** | Single-writer, can lock under load | Full concurrent access |
| **Data safety** | Single file, one corruption risk | ACID-compliant, WAL logging |
| **Scalability** | Fine for solo use | Handles teams + CI workloads |
| **Backup** | Copy the file | `pg_dump` for proper backups |
| **Best for** | Tiny personal use | Anything serious |

---

### 4. Useful Commands

```bash
# Gitea
docker ps --filter name=gitea          # status
docker logs gitea -f                   # live logs
cd /opt/gitea && docker compose restart
cd /opt/gitea && docker compose pull && docker compose up -d  # update

# PostgreSQL
sudo systemctl status postgresql@16-main
sudo -u postgres psql -p 5433 -d gitea  # connect to Gitea DB
sudo -u postgres pg_dump -p 5433 gitea > /tmp/gitea-backup.sql  # backup

# Firewall
sudo ufw status numbered
```

---

### 5. Quick Checklist

- [ ] Open `http://192.168.1.36:3000`
- [ ] Database fields are pre-filled — click **Install Gitea**
- [ ] Register your admin account (first user = admin by default)
- [ ] Create your first repo
- [ ] Clone via SSH: `git clone ssh://git@192.168.1.36:2222/username/repo.git`

---

Want me to set up nginx reverse proxy for a clean domain, or configure automated PostgreSQL backups?
