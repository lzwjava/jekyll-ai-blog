---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将旧笔记本电脑改造成无头服务器
translated: true
type: note
---

**问题：** 我可以在旧笔记本电脑上安装 Ubuntu Server，然后完全通过 SSH 使用它——即使键盘或屏幕坏了——来利用其 CPU 和内存进行轻量级部署吗？

**回答：**

## 是的——绝对可以！这是一个经典的“Headless Server”设置

你的想法完全可行且被广泛采用。在旧笔记本电脑上安装 **Ubuntu Server** 并完全通过 **SSH** 管理它，就称为 **headless server** 设置。初始设置完成后，你再也不需要碰笔记本的键盘或屏幕。

---

## 步骤 1：选择合适的操作系统

由于无头服务器不需要渲染图形元素，你可以使用 Ubuntu Server 24.04 LTS 并分配最小资源——完全绕过 GUI 可以节省大量的 RAM 和 CPU。

**推荐选项：**
- **Ubuntu Server 24.04 LTS** — 文档最佳、社区支持最多、对初学者友好
- **Debian 12** — 更轻量、非常稳定
- **DietPi** — 仅需 512 MB RAM，资源消耗最少，从而将所有处理能力转向服务器任务

---

## 步骤 2：安装 Ubuntu Server（带屏幕或无屏幕）

Ubuntu Server 支持多种无头安装方法，从串口控制台访问到完全自动安装，无需任何交互。

**如果首次设置仍有屏幕（推荐方法）：**

1. 下载 **Ubuntu Server ISO**（不是 Ubuntu Desktop）
2. 使用 Rufus 或 Balena Etcher 将其刻录到 USB 驱动器
3. 从 USB 启动笔记本，跟随文本安装程序
4. **关键：安装过程中选择“Install OpenSSH Server”**
5. 在网络设置中配置静态 IP——这是管理设备所必需的。

**如果完全无屏幕（完全无头）：**

使用 Ubuntu 的 Autoinstall 功能，机器会无提示自动安装——你将包含 `user-data` YAML 配置文件嵌入 ISO 中，指定 hostname、username、password hash、SSH keys 和网络设置。

---

## 步骤 3：启用并通过 SSH 连接

安装完成后，从同一网络上的任何其他电脑：

```bash
ssh username@<laptop-ip-address>
```

为提升安全性，禁用密码认证并改用 SSH 密钥登录。在客户端机器上使用 `ssh-keygen -t ed25519` 生成密钥，然后用 `ssh-copy-id` 复制到服务器。

同时启用防火墙并允许 SSH：

```bash
sudo ufw allow ssh
sudo ufw enable
```

---

## 步骤 4：处理笔记本盖子问题

一个关键挑战是笔记本合上盖子时倾向于进入睡眠模式。要修复此问题，编辑 `/etc/systemd/logind.conf`，将 `HandleLidSwitch=suspend` 改为 `HandleLidSwitch=ignore`，然后用 `sudo service systemd-logind restart` 重启服务。

同时检查 BIOS：某些电脑的 BIOS/UEFI 配置如果未插入键盘或显示器就会停止启动过程——进入 BIOS 设置并禁用该功能。

---

## 步骤 5：可以部署哪些轻量级服务？

旧笔记本上的家庭服务器可以运行：用于文件存储的 NAS、使用 AdGuard 的全网广告阻挡、使用 Jellyfin 的媒体服务器等——多个服务可顺畅运行。

通过 **Docker** 的热门轻量级部署（强烈推荐）：

| Service | Purpose |
|---|---|
| **Nginx / Caddy** | Web server / reverse proxy |
| **Pi-hole / AdGuard Home** | Network-wide ad blocker |
| **Jellyfin** | Media server |
| **Nextcloud** | Personal cloud storage |
| **Portainer** | Docker web UI |
| **Gitea** | Self-hosted Git |
| **Home Assistant** | Smart home automation |
| **Uptime Kuma** | Service monitoring |

安装 Ubuntu Server 后，Docker 是绝佳起点——它在沙箱环境中运行容器，非常适合自托管各种服务。

---

## 额外提示：通过路由器分配静态 IP

在路由器设置中为笔记本的 MAC 地址分配 **DHCP reservation**。这确保笔记本始终获得相同 IP，因此你的 SSH 命令永不变更——即使重启后也是如此。

---

## 总结检查清单

1. ✅ 下载 Ubuntu Server 24.04 LTS ISO
2. ✅ 刻录到 USB，启动并安装——安装时勾选“OpenSSH Server”
3. ✅ 设置静态 IP（路由器预留或手动 netplan 配置）
4. ✅ 在 `logind.conf` 中禁用合盖休眠
5. ✅ 从任何设备 SSH 登录：`ssh user@<ip>`
6. ✅ 安装 Docker：`sudo apt install docker.io docker-compose`
7. ✅ 根据需要部署轻量级服务

---

**参考资料：**

- [Deploying a Headless Ubuntu Server (Medium)](https://medium.com/@pacegaming/deploying-a-headless-ubuntu-server-fe4ffa0bf8e1)
- [How to Install Ubuntu Server Without a Monitor](https://oneuptime.com/blog/post/2026-03-02-install-ubuntu-server-without-monitor-headless/view)
- [Transforming an Old Laptop into Ubuntu Server Homelab](https://medium.com/@azhar9/transforming-an-old-asus-laptop-into-a-ubuntu-server-for-my-homelab-setup-e3c99f076080)
- [Building My Home Server from an Old Laptop (DEV Community)](https://dev.to/strikeraryu/building-my-home-server-from-an-old-laptop-4b39)
- [New Life for an Old Laptop as a Linux Home Server](https://medium.com/@rghv064/new-life-for-an-old-laptop-as-a-linux-home-server-8e4557d5cc8c)
- [Setting Up a Headless Linux Server (LinkedIn)](https://www.linkedin.com/pulse/setting-up-headless-linux-server-jose-chapa)
