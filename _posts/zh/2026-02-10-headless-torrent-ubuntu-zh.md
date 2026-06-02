---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 适用于 Ubuntu 的无界面 BitTorrent 客户端
translated: true
type: note
---

Question: 如何在 Ubuntu server 上使用命令行下载 torrent 文件？qBittorrent 是 GUI 程序吗？

Answer:

是的，标准的 **qBittorrent** 软件包是一个 GUI 应用程序（它需要 X11/Wayland 等桌面环境）。

但在 Ubuntu Server（无头模式 / 无 GUI）上，你应该使用 **qbittorrent-nox**。这是 qBittorrent 的 **headless**（无 X/GUI）版本。它作为一个 daemon 运行，并提供一个**非常出色的 web interface**，你可以通过网络上的任何浏览器访问它。

### Ubuntu Server 推荐选项 (CLI / headless)

以下是 2025–2026 年最流行且可靠的选择：

| Client              | Type              | Best for                          | Web UI? | Install command                              | Download example                                      |
|---------------------|-------------------|-----------------------------------|---------|----------------------------------------------|-------------------------------------------------------|
| qbittorrent-nox     | daemon + web UI   | Modern features, best overall     | Yes     | `sudo apt install qbittorrent-nox`           | 通过 web UI 添加 torrent (http://server-ip:8080)        |
| transmission-cli    | pure CLI          | Very simple one-shot downloads    | No      | `sudo apt install transmission-cli`          | `transmission-cli file.torrent`                       |
| aria2c              | pure CLI          | Fast, lightweight, multi-protocol | No      | `sudo apt install aria2`                     | `aria2c file.torrent` 或 `aria2c magnet-link`         |
| rtorrent            | ncurses TUI       | Power users who like vim-style UI | No      | `sudo apt install rtorrent`                  | 运行 `rtorrent` 然后通过 ^O 快捷键加载 torrent     |

### Ubuntu Server 最流行的选择：qbittorrent-nox + Web UI

```bash
# 1. (可选但推荐) 使用官方稳定的 PPA 以获取较新版本
sudo add-apt-repository ppa:qbittorrent-team/qbittorrent-stable
sudo apt update

# 2. 安装
sudo apt install qbittorrent-nox

# 3. 为运行 daemon 创建专用用户 (安全最佳实践)
sudo adduser --system --group qbittorrent

# 4. 创建下载和配置文件夹 (根据喜好调整路径)
sudo mkdir -p /var/lib/qbittorrent/downloads
sudo chown -R qbittorrent:qbittorrent /var/lib/qbittorrent

# 5. 运行一次以创建配置文件并设置 web UI 密码
sudo -u qbittorrent qbittorrent-nox
# → 它会显示默认用户名 = admin, 密码 = adminadmin
# 按 Ctrl+C 停止
```

然后创建一个 systemd service 以便它自动启动：

```bash
sudo nano /etc/systemd/system/qbittorrent-nox.service
```

粘贴以下内容（如有需要请调整路径）：

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

现在在浏览器中打开：
**http://your-server-ip:8080**
(默认登录: admin / adminadmin — 请立即更改！)

你可以直接从 web 界面添加 .torrent 文件或 magnet 链接。

### 纯 CLI 替代方案

**transmission-cli** (非常简单)

```bash
sudo apt install transmission-cli

# 基础下载 (下载到当前文件夹)
transmission-cli ubuntu-24.04-desktop-amd64.iso.torrent

# 下载到特定文件夹 + daemon 模式
transmission-cli -w /path/to/downloads ubuntu-24.04-desktop-amd64.iso.torrent
```

**aria2c** (快速且现代)

```bash
sudo apt install aria2

aria2c "magnet:?xt=urn:btih:..."
# 或者
aria2c file.torrent --dir=/downloads --seed-time=0   # 下载完成后停止 seeding
```

如果你想要友好的界面和丰富的功能，请选择 **qbittorrent-nox**。
如果你只想进行快速的命令行单次下载，请选择 **aria2c** 或 **transmission-cli**。

References:

- [qBittorrent 官方网站](https://www.qbittorrent.org/)
- [Ubuntu torrent 客户端概览](https://linuxconfig.org/ubuntu-22-04-list-of-torrent-clients)
- [qbittorrent-nox systemd 设置指南](https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-(WebUI-only,-systemd-service-set-up,-Ubuntu-15.04-or-newer))
