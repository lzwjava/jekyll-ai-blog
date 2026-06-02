---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Gitea PostgreSQL Docker Connection Issues
translated: false
type: note
---

## 🔧 How I Fixed the Gitea ↔ PostgreSQL Connection

### The Error

```
The database settings are invalid: dial tcp 172.17.0.1:5433: connect: connection timed out
```

Gitea (running in Docker) couldn't reach PostgreSQL (running on the host). Three separate problems were blocking it.

---

### Problem 1: PostgreSQL Only Listening on `localhost`

**What happened:** PostgreSQL's default config binds to `127.0.0.1` only. That means it only accepts connections from the host machine itself — not from Docker containers.

**How I found it:**
```bash
sudo ss -tlnp | grep 5433
# Output showed: 127.0.0.1:5433 — only localhost!
```

**The fix:**
```bash
# Changed in /etc/postgresql/16/main/postgresql.conf:
# listen_addresses = 'localhost'        ← old (commented out default)
listen_addresses = '*'                  ← new (listen on all interfaces)
```

Now PostgreSQL accepts connections on `0.0.0.0:5433` (all IPs) instead of just `127.0.0.1`.

**Why it matters:** A Docker container has its own network namespace. From inside the container, `127.0.0.1` is the container itself — not the host. So `localhost` inside Docker ≠ `localhost` on the host.

---

### Problem 2: Docker Network Mismatch

**What happened:** Gitea was running on a custom Docker network (`gitea_default`) with gateway `172.22.0.1`, but `host.docker.internal` was resolving to `172.17.0.1` (the default `docker0` bridge).

**How I found it:**
{% raw %}
```bash
docker inspect gitea --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}: {{$v.Gateway}}{{"\n"}}{{end}}'
# Output: gitea_default: 172.22.0.1

docker exec gitea sh -c "getent hosts host.docker.internal"
# Output: 172.17.0.1  host.docker.internal
```
{% endraw %}

Docker Compose creates its own network per project. The `host.docker.internal` mapping uses the default bridge IP, but traffic from a custom network doesn't always route cleanly to the default bridge.

**The fix:** By changing `listen_addresses = '*'`, PostgreSQL now listens on **all** interfaces — including the one reachable from the custom Docker network. No matter which Docker network connects, as long as traffic reaches port 5433 on the host, PostgreSQL accepts it.

---

### Problem 3: iptables Blocking the Connection

**What happened:** Even after fixing the above two issues, the connection still timed out. The real blocker was iptables — the Linux firewall was silently dropping packets from Docker to the host on port 5433.

**How I found it:**
```bash
# After fixing listen_addresses, tried again:
docker exec gitea sh -c "timeout 3 bash -c 'echo > /dev/tcp/host.docker.internal/5433'"
# Still FAILED

# Then manually opened the port:
sudo iptables -I INPUT -p tcp --dport 5433 -j ACCEPT
# Tried again → OK!
```

Docker has its own iptables chains. When a container tries to reach the host, the packet goes through the host's `INPUT` chain. If no rule allows it, it gets dropped.

**The fix (permanent):**
```bash
sudo ufw allow from 172.16.0.0/12 to any port 5433 proto tcp comment 'postgresql-docker'
```

| Part | Meaning |
|------|---------|
| `from 172.16.0.0/12` | Only Docker networks (172.16.0.0 – 172.31.255.255) |
| `to any port 5433` | PostgreSQL's port |
| `proto tcp` | PostgreSQL uses TCP |

This is more secure than opening 5433 to the whole internet — only Docker containers can reach it.

---

### The Flow After Fixing

```
1. Browser → http://192.168.1.36:3000
              ↓
2. Gitea container (172.22.0.x)
   resolves host.docker.internal → 172.17.0.1
              ↓
3. Packet hits host's iptables INPUT chain
   ufw rule: "allow from 172.16.0.0/12 to port 5433" → ACCEPT ✅
              ↓
4. PostgreSQL on 0.0.0.0:5433 receives the connection
   pg_hba.conf: "allow gitea user from 172.16.0.0/12" → AUTHENTICATE ✅
              ↓
5. Gitea connects to DB, install page works 🎉
```

---

### Summary

| Problem | Symptom | Fix |
|---------|---------|-----|
| PostgreSQL only on `localhost` | Container can't reach host's loopback | `listen_addresses = '*'` |
| Custom Docker network ≠ bridge | `host.docker.internal` resolves to wrong gateway | Already handled by `listen_addresses = '*'` |
| iptables drops Docker → host traffic | Connection times out | `ufw allow from 172.16.0.0/12 to port 5433` |
