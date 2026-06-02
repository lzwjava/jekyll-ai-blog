---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix qBittorrent WebUI Binding Issue
translated: false
type: note
---

Question: Why is --webui-address=0.0.0.0 an unknown command line parameter for qbittorrent-nox, and how to make the WebUI listen on all interfaces?

Answer:

The error occurs because **`--webui-address`** is **not a valid command-line option** for `qbittorrent-nox`. The supported command-line flags are very limited (you can see them by running `qbittorrent-nox --help`).

From the official help output and man pages, the available options include:

- `--webui-port=<port>` (or `-p <port>`) → to change the WebUI port (default: 8080)
- `-d` or `--daemon` → run in background/daemon mode
- Others like `--help`, `--version`, `--profile`, etc.

There is **no `--webui-address`** flag at the command line.

**Default behavior**
By default, the qBittorrent WebUI (including in `qbittorrent-nox`) listens on **all network interfaces** (`0.0.0.0:8080` for IPv4 and usually the equivalent for IPv6) — not just localhost.
This means it is already accessible remotely (e.g. `http://your-server-ip:8080`) unless blocked by:

- A firewall (e.g. ufw, firewalld, iptables)
- The WebUI "IP address whitelist" or authentication settings inside qBittorrent
- Network configuration (e.g. listening only on loopback due to earlier config)

**Correct command**
Your command should simply be:

```bash
/usr/bin/qbittorrent-nox --webui-port=8080 --daemon
```

(or omit `--webui-port=8080` if you want the default port).

**If you want to force a specific IP (not usually needed)**

- There is **no command-line flag** for binding the WebUI to a specific IP.
- Instead, set it inside the configuration:
  1. Start qBittorrent-nox once (foreground is fine for initial setup)
  2. Access the WebUI at `http://localhost:8080` (default credentials: admin / adminadmin)
  3. Go to **Tools → Options → Web UI**
  4. Look for **"IP address to listen on"** or **"WebUI address"** (wording varies slightly by version)
  5. Set it to `0.0.0.0` (or leave blank/empty for all interfaces)
  6. Apply and restart the process

Alternatively, you can edit the config file directly (usually `~/.config/qBittorrent/qBittorrent.conf`):

```ini
[Preferences]
WebUI\Address=0.0.0.0
WebUI\Port=8080
```

**Quick troubleshooting checklist**

- Run `qbittorrent-nox --help` to confirm your version's exact flags.
- Check firewall: `sudo ufw allow 8080` (Ubuntu) or `sudo firewall-cmd --add-port=8080/tcp --permanent` (Fedora/RHEL).
- Verify listening: After starting, run `ss -tuln | grep 8080` or `netstat -tuln | grep 8080` — you should see `0.0.0.0:8080` or `*:8080`.
- If still only localhost: Check the config file or WebUI settings for any IP restriction.

References:

- [https://manpages.ubuntu.com/manpages/focal/man1/qbittorrent-nox.1.html](https://manpages.ubuntu.com/manpages/focal/man1/qbittorrent-nox.1.html)
- [https://wiki.archlinux.org/title/QBittorrent](https://wiki.archlinux.org/title/QBittorrent)
- [https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-(WebUI-only,-systemd-service-set-up,-Ubuntu-15.04-or-newer)](https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-(WebUI-only,-systemd-service-set-up,-Ubuntu-15.04-or-newer))
- [https://userdocs.github.io/qbittorrent-nox-static/install-qbittorrent](https://userdocs.github.io/qbittorrent-nox-static/install-qbittorrent)
