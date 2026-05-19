---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gitea 设置中更换 SSH 端口
translated: true
type: note
---

## 🔧 我如何交换 SSH 端口

### 问题

Gitea 在端口 **2222** 上运行 SSH（`git clone ssh://git@host:2222/repo.git`）。用户希望它运行在端口 **22** 上，这样就可以直接使用 `git clone git@host:repo.git` —— 无需端口号。

但主机的 sshd 已经在端口 22 上运行。两个服务不能共享同一端口。因此我们必须交换它们：

```
Before:  Host SSH = 22    |  Gitea SSH = 2222
After:   Host SSH = 2222  |  Gitea SSH = 22
```

---

### 步骤 1：将主机 SSH 移动到端口 2222

#### 问题：仅编辑 sshd_config 不足以解决问题

我编辑了 `/etc/ssh/sshd_config`：
```
Port 2222
```

但重启 SSH 后，它仍然在端口 **22** 上运行。为什么？

#### 发现：systemd socket activation

```bash
systemctl list-units | grep ssh
# Output:
# ssh.service    loaded active running
# ssh.socket     loaded active running   ← this is the culprit
```

Ubuntu 使用 **socket activation** 来处理 SSH。sshd 不再创建自己的 socket，而是由 systemd 先创建 socket 然后交给 sshd。该 socket 定义在 `/lib/systemd/system/ssh.socket` 中：

```ini
[Socket]
ListenStream=0.0.0.0:22        ← systemd binds to port 22
ListenStream=[::]:22
```

这会**覆盖** `sshd_config` 中的任何 `Port` 设置。因此更改 `sshd_config` 没有效果。

#### 修复：覆盖 socket unit

创建 systemd 覆盖：
```bash
sudo mkdir -p /etc/systemd/system/ssh.socket.d

# /etc/systemd/system/ssh.socket.d/override.conf
[Socket]
ListenStream=                   # ← Clear ALL existing ListenStream directives
ListenStream=0.0.0.0:2222       # ← Set new port
ListenStream=[::]:2222
```

空 `ListenStream=` 至关重要 —— 它会**重置**列表，然后添加新条目。没有它，systemd 会尝试同时监听 22 和 2222。

然后：
```bash
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket ssh.service
```

#### 问题：端口 2222 已被占用

重启失败，错误信息：
```
ssh.socket: Failed to create listening socket (0.0.0.0:2222): Address already in use
```

Gitea 的 Docker 容器通过 `docker-proxy` 占用了端口 2222。必须先停止容器。

---

### 步骤 2：更新 Gitea 使用端口 22

#### 修改 docker-compose.yml

编辑 `/opt/gitea/docker-compose.yml`：
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

同时更新环境变量：
```yaml
# Before:
- GITEA__server__SSH_PORT=2222

# After:
- GITEA__server__SSH_PORT=22
```

#### 停止 Gitea 以释放端口 2222

```bash
cd /opt/gitea && docker compose down
```

这释放了 `docker-proxy` 占用的端口 2222。

---

### 步骤 3：首先在 2222 上启动主机 SSH

现在 2222 已空闲：
```bash
sudo systemctl start ssh.socket ssh.service
```

验证：
```bash
sudo ss -tlnp | grep sshd
# 0.0.0.0:2222 ← success!
```

---

### 步骤 4：在端口 22 上启动 Gitea

```bash
cd /opt/gitea && docker compose up -d
```

验证：
{% raw %}
```bash
docker ps --filter name=gitea --format "table {{.Names}}\t{{.Ports}}"
# gitea   0.0.0.0:22->22/tcp, 0.0.0.0:3000->3000/tcp  ← success!
```
{% endraw %}

---

### 步骤 5：验证防火墙

```bash
sudo ufw status | grep -E '(22|2222)'
```

| 端口 | 规则 | 用途 |
|------|------|---------|
| 22/tcp | ALLOW Anywhere | Gitea SSH |
| 2222/tcp | ALLOW Anywhere (host-ssh) | Host SSH |

两个端口已由之前的规则开放。无需更改。

---

### 最终状态

```bash
sudo ss -tlnp | grep -E ':(22|2222)\b'

# Port 2222 → sshd (host SSH)
# Port 22   → docker-proxy (Gitea SSH)
```

```
用户连接到端口 22 → Docker proxy → Gitea 容器 (SSH server)
用户连接到端口 2222 → sshd (host shell access)
```

---

### 关键经验

在带有 systemd 的 Ubuntu 上，SSH 端口不仅仅由 `sshd_config` 控制。**socket unit**（`ssh.socket`）优先。要更改 SSH 端口，需要：

1. 覆盖 socket unit（`/etc/systemd/system/ssh.socket.d/override.conf`）
2. 更新 `sshd_config`（保持一致性）
3. 执行 `daemon-reload` + 重启