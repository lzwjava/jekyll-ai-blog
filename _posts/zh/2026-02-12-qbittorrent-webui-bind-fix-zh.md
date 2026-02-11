---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 qBittorrent WebUI 绑定问题
translated: true
type: note
---

Question: 为什么 `--webui-address=0.0.0.0` 对 qbittorrent-nox 来说是一个无效的命令行参数？如何让 WebUI 监听所有网卡接口？

Answer: 

出现该错误是因为 **`--webui-address`** **不是 `qbittorrent-nox` 的有效命令行选项**。支持的命令行参数非常有限（你可以通过运行 `qbittorrent-nox --help` 来查看）。

根据官方帮助输出和 man pages，可用的选项包括：
- `--webui-port=<port>` (或 `-p <port>`) → 修改 WebUI 端口 (默认: 8080)
- `-d` 或 `--daemon` → 以 background/daemon 模式运行
- 其他诸如 `--help`, `--version`, `--profile` 等。

命令行中**不存在 `--webui-address`** 参数。

**默认行为**  
默认情况下，qBittorrent WebUI（包括 `qbittorrent-nox`）会监听**所有网络接口**（IPv4 为 `0.0.0.0:8080`，IPv6 通常也是类似配置）——而不仅仅是 localhost。  
这意味着它已经可以被远程访问（例如 `http://your-server-ip:8080`），除非被以下因素阻断：
- 防火墙 (例如 ufw, firewalld, iptables)
- qBittorrent 内部的 WebUI "IP address whitelist" 或身份验证设置
- 网络配置（例如由于之前的配置导致仅监听在 loopback 接口）

**正确命令**  
你的命令应该简化为：

```bash
/usr/bin/qbittorrent-nox --webui-port=8080 --daemon
```

（如果你想使用默认端口，可以省略 `--webui-port=8080`）。

**如果你想强制指定特定 IP（通常不需要）**  
- **没有命令行参数**可以将 WebUI 绑定到特定 IP。
- 相反，你需要在配置中进行设置：
  1. 启动一次 qBittorrent-nox（初始设置时在前台运行即可）
  2. 访问 WebUI： `http://localhost:8080` (默认凭据: admin / adminadmin)
  3. 进入 **Tools → Options → Web UI**
  4. 找到 **"IP address to listen on"** 或 **"WebUI address"** (字样随版本略有不同)
  5. 将其设置为 `0.0.0.0`（或保持为空以监听所有接口）
  6. 应用并重启进程

或者，你可以直接编辑配置文件（通常路径为 `~/.config/qBittorrent/qBittorrent.conf`）：

```ini
[Preferences]
WebUI\Address=0.0.0.0
WebUI\Port=8080
```

**快速排障清单**
- 运行 `qbittorrent-nox --help` 以确认你所用版本的准确参数。
- 检查防火墙：`sudo ufw allow 8080` (Ubuntu) 或 `sudo firewall-cmd --add-port=8080/tcp --permanent` (Fedora/RHEL)。
- 验证监听状态：启动后运行 `ss -tuln | grep 8080` 或 `netstat -tuln | grep 8080` ——你应该看到 `0.0.0.0:8080` 或 `*:8080`。
- 如果仍然只有 localhost：检查配置文件或 WebUI 设置中是否有任何 IP 限制。

References:  

- [https://manpages.ubuntu.com/manpages/focal/man1/qbittorrent-nox.1.html](https://manpages.ubuntu.com/manpages/focal/man1/qbittorrent-nox.1.html)
- [https://wiki.archlinux.org/title/QBittorrent](https://wiki.archlinux.org/title/QBittorrent)
- [https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-(WebUI-only,-systemd-service-set-up,-Ubuntu-15.04-or-newer)](https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-(WebUI-only,-systemd-service-set-up,-Ubuntu-15.04-or-newer))
- [https://userdocs.github.io/qbittorrent-nox-static/install-qbittorrent](https://userdocs.github.io/qbittorrent-nox-static/install-qbittorrent)