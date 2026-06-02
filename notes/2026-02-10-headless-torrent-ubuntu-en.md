---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Headless Torrent Clients for Ubuntu
translated: false
type: note
---

Question: How to use the command line to download torrent files on an Ubuntu server? Is qBittorrent a GUI program?

Answer:

Yes, the regular **qBittorrent** package is a GUI application (it requires a desktop environment with X11/Wayland).

However, on Ubuntu Server (headless / no GUI), you should use **qbittorrent-nox** instead. This is the **headless** (no X/GUI) version of qBittorrent. It runs as a daemon and provides a **very good web interface** that you can access from any browser on your network.

### Recommended Options for Ubuntu Server (CLI / headless)

Here are the most popular and reliable choices in 2025–2026:

| Client              | Type              | Best for                          | Web UI? | Install command                              | Download example                                      |
|---------------------|-------------------|-----------------------------------|---------|----------------------------------------------|-------------------------------------------------------|
| qbittorrent-nox     | daemon + web UI   | Modern features, best overall     | Yes     | `sudo apt install qbittorrent-nox`           | Add torrent via web UI (<http://server-ip:8080>)        |
| transmission-cli    | pure CLI          | Very simple one-shot downloads    | No      | `sudo apt install transmission-cli`          | `transmission-cli file.torrent`                       |
| aria2c              | pure CLI          | Fast, lightweight, multi-protocol | No      | `sudo apt install aria2`                     | `aria2c file.torrent` or `aria2c magnet-link`         |
| rtorrent            | ncurses TUI       | Power users who like vim-style UI | No      | `sudo apt install rtorrent`                  | Run `rtorrent` then load torrent with ^O shortcut     |

### Most Popular Choice for Ubuntu Servers: qbittorrent-nox + Web UI

```bash
# 1. (Optional but recommended) Use the official stable PPA for newer version
sudo add-apt-repository ppa:qbittorrent-team/qbittorrent-stable
sudo apt update

# 2. Install
sudo apt install qbittorrent-nox

# 3. Create a user for running the daemon (security best practice)
sudo adduser --system --group qbittorrent

# 4. Create download & config folders (adjust paths as you like)
sudo mkdir -p /var/lib/qbittorrent/downloads
sudo chown -R qbittorrent:qbittorrent /var/lib/qbittorrent

# 5. Run it once to create config file and set web UI password
sudo -u qbittorrent qbittorrent-nox
# → it will show default username = admin, password = adminadmin
# Press Ctrl+C to stop
```

Then create a systemd service so it starts automatically:

```bash
sudo nano /etc/systemd/system/qbittorrent-nox.service
```

Paste this content (adjust paths if needed):

```ini
[Unit]
Description=qBittorrent-nox service
After=network.target nss-lookup.target

[Service]
Type=simple
User=qbittorrent
Group=qbittorrent
UMask=0027
ExecStart=/usr/bin/qbittorrent-nox --daemon --webui-port=8080
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now qbittorrent-nox
```

Now open in browser:
**<http://your-server-ip:8080>**
(default login: admin / adminadmin — change it immediately!)

You can add .torrent files or magnet links directly from the web interface.

### Quick CLI-only Alternatives

**transmission-cli** (very simple)

```bash
sudo apt install transmission-cli

# Basic download (downloads to current folder)
transmission-cli ubuntu-24.04-desktop-amd64.iso.torrent

# Download to specific folder + daemon mode
transmission-cli -w /path/to/downloads ubuntu-24.04-desktop-amd64.iso.torrent
```

**aria2c** (fast & modern)

```bash
sudo apt install aria2

aria2c "magnet:?xt=urn:btih:..."
# or
aria2c file.torrent --dir=/downloads --seed-time=0   # stop seeding after download
```

Choose **qbittorrent-nox** if you want a nice interface and many features.
Choose **aria2c** or **transmission-cli** if you only want quick command-line one-shot downloads.

References:

- [qBittorrent official site](https://www.qbittorrent.org/)
- [Ubuntu torrent clients overview](https://linuxconfig.org/ubuntu-22-04-list-of-torrent-clients)
- [qbittorrent-nox systemd setup guide](https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-(WebUI-only,-systemd-service-set-up,-Ubuntu-15.04-or-newer))
