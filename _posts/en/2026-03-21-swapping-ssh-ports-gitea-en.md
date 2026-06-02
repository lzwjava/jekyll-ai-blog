---
audio: false
generated: true
image: false
lang: en
layout: post
title: Swapping SSH Ports for Gitea Setup
translated: false
type: note
---

## 🔧 How I Swapped the SSH Ports

### The Problem

Gitea was running SSH on port **2222** (`git clone ssh://git@host:2222/repo.git`). The user wanted it on port **22** so they could just do `git clone git@host:repo.git` — no port number needed.

But the host's sshd was already on port 22. Two services can't share the same port. So we had to swap them:

```
Before:  Host SSH = 22    |  Gitea SSH = 2222
After:   Host SSH = 2222  |  Gitea SSH = 22
```

---

### Step 1: Move Host SSH to Port 2222

#### Problem: sshd_config alone wasn't enough

I edited `/etc/ssh/sshd_config`:

```
Port 2222
```

But after restarting SSH, it was **still on port 22**. Why?

#### Discovery: systemd socket activation

```bash
systemctl list-units | grep ssh
# Output:
# ssh.service    loaded active running
# ssh.socket     loaded active running   ← this is the culprit
```

Ubuntu uses **socket activation** for SSH. Instead of sshd creating its own socket, systemd creates the socket first and hands it to sshd. The socket is defined in `/lib/systemd/system/ssh.socket`:

```ini
[Socket]
ListenStream=0.0.0.0:22        ← systemd binds to port 22
ListenStream=[::]:22
```

This **overrides** whatever `Port` is set in `sshd_config`. So changing `sshd_config` had no effect.

#### Fix: Override the socket unit

Created a systemd override:

```bash
sudo mkdir -p /etc/systemd/system/ssh.socket.d

# /etc/systemd/system/ssh.socket.d/override.conf
[Socket]
ListenStream=                   # ← Clear ALL existing ListenStream directives
ListenStream=0.0.0.0:2222       # ← Set new port
ListenStream=[::]:2222
```

The empty `ListenStream=` is critical — it **resets** the list before adding new entries. Without it, systemd would try to listen on both 22 and 2222.

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket ssh.service
```

#### Problem: Port 2222 was in use

Restart failed with:

```
ssh.socket: Failed to create listening socket (0.0.0.0:2222): Address already in use
```

Gitea's Docker container was using port 2222 via `docker-proxy`. The container needed to go first.

---

### Step 2: Update Gitea to Use Port 22

#### Change docker-compose.yml

Edited `/opt/gitea/docker-compose.yml`:

```yaml
# Before:
ports:
  - "3000:3000"
  - "2222:22"      # host:container

# After:
ports:
  - "3000:3000"
  - "22:22"         # host:container
```

Also updated the environment variable:

```yaml
# Before:
- GITEA__server__SSH_PORT=2222

# After:
- GITEA__server__SSH_PORT=22
```

#### Stop Gitea to free port 2222

```bash
cd /opt/gitea && docker compose down
```

This released port 2222 from `docker-proxy`.

---

### Step 3: Start Host SSH on 2222 First

Now that 2222 was free:

```bash
sudo systemctl start ssh.socket ssh.service
```

Verified:

```bash
sudo ss -tlnp | grep sshd
# 0.0.0.0:2222 ← success!
```

---

### Step 4: Start Gitea on Port 22

```bash
cd /opt/gitea && docker compose up -d
```

Verified:
{% raw %}

```bash
docker ps --filter name=gitea --format "table {{.Names}}\t{{.Ports}}"
# gitea   0.0.0.0:22->22/tcp, 0.0.0.0:3000->3000/tcp  ← success!
```

{% endraw %}

---

### Step 5: Verify Firewall

```bash
sudo ufw status | grep -E '(22|2222)'
```

| Port | Rule | Purpose |
|------|------|---------|
| 22/tcp | ALLOW Anywhere | Gitea SSH |
| 2222/tcp | ALLOW Anywhere (host-ssh) | Host SSH |

Both were already open from earlier rules. No changes needed.

---

### Final State

```bash
sudo ss -tlnp | grep -E ':(22|2222)\b'

# Port 2222 → sshd (host SSH)
# Port 22   → docker-proxy (Gitea SSH)
```

```
User connects to port 22 → Docker proxy → Gitea container (SSH server)
User connects to port 2222 → sshd (host shell access)
```

---

### Key Lesson

On Ubuntu with systemd, SSH port isn't controlled by `sshd_config` alone. The **socket unit** (`ssh.socket`) takes precedence. To change SSH port, you need to:

1. Override the socket unit (`/etc/systemd/system/ssh.socket.d/override.conf`)
2. Update `sshd_config` (for consistency)
3. Both `daemon-reload` + restart
