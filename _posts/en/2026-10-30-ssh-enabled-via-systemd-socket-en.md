---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Enabled via Systemd Socket
translated: false
type: note
---

Confirmed. SSH is **open and enabled via systemd socket activation**:

- `ssh.socket` → **active (listening)** on port 22, IPv4 + IPv6, bound to all interfaces (`0.0.0.0` / `[::]`).
- `sshd-unix-local.socket` → active (AF_UNIX local socket).
- No persistent `sshd` process is running yet — that's normal: systemd spawns `sshd` on demand when a client connects.

So other machines **can** reach this laptop's SSH on port 22. If you want to confirm it's actually usable, run:

```bash
ssh localhost
```

(If a firewall is active, note that an open listening port can still be blocked externally — check with `sudo ufw status` or `sudo nft list ruleset` if you need external access.)
