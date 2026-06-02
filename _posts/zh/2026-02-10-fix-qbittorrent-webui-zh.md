---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 qBittorrent WebUI 空白页访问问题
translated: true
type: note
---

Question: 访问 http://192.168.1.36:8080 时 Web UI 没有任何显示

Answer:

如果在 `http://192.168.1.36:8080` **没有任何显示**（空白页、超时、连接被拒绝或无限加载），请在你的 Ubuntu server 上按顺序执行以下 troubleshooting 步骤。大多数“无显示”情况是由以下原因之一引起的：service 未运行、bind address 错误、firewall 拦截、端口错误、config 问题或浏览器/网络问题。

### 1. 检查 service 是否正在运行
```bash
sudo systemctl status qbittorrent-nox
```

- 确认状态为 **Active: active (running)**。
- 如果显示 failed / inactive / dead → 请参阅步骤 7。
- 同时检查最近的 logs：
```bash
sudo journalctl -u qbittorrent-nox -n 50 --no-pager
```

查找类似以下内容的行：
- `WebUI: Now listening on IP: *, port: 8080` → 正常
- `WebUI: Now listening on IP: 127.0.0.1` 或 `localhost` → 异常（仅限本地访问）
- 任何关于 binding、permissions 或 crashes 的错误。

### 2. 在服务器本地进行测试
直接在 Ubuntu server 上运行（通过 SSH 或控制台）：
```bash
curl http://localhost:8080
```

或者
```bash
curl http://127.0.0.1:8080
```

- 如果你收到了 **HTML code**（以 `<!DOCTYPE html>` 开头或显示登录页源码）→ service 正在运行，问题出在网络/firewall/浏览器端。
- 如果显示 `curl: (7) Failed to connect to localhost port 8080: Connection refused` → service 未监听或仅 bound 到了错误的接口。
- 如果显示 `curl: (52) Empty reply from server` 或超时 → service 正在运行但 WebUI 已损坏/崩溃。

### 3. 检查 8080 端口的实际监听状态
```bash
sudo ss -tuln | grep 8080
# 或者
sudo netstat -tuln | grep 8080   # 如果已安装 netstat
```

- 预期的正常输出：`tcp LISTEN 0 128 *:8080 *:*` 或 `0.0.0.0:8080`（在所有接口上监听）。
- 如果显示 `127.0.0.1:8080` 或无任何内容 → WebUI 仅 bound 到了 localhost。

**修复仅 bound 到 localhost 的问题**
编辑 config（先停止 service）：
```bash
sudo systemctl stop qbittorrent-nox
```

然后编辑（以 qbittorrent 用户身份或使用 sudo）：
```bash
nano /var/lib/qbittorrent/.config/qBittorrent/qBittorrent.conf
# 或者你的 config 所在位置 (使用 find / -name qBittorrent.conf 查找)
```

在 `[Preferences]` 下找到或添加以下行：
```
WebUI\Address=0.0.0.0
WebUI\Port=8080
WebUI\Enabled=true
```
（0.0.0.0 表示监听所有网络接口）

重启：
```bash
sudo systemctl start qbittorrent-nox
```

替代方案：使用显式 bind 手动运行：
```bash
sudo -u qbittorrent qbittorrent-nox --webui-port=8080 --webui-address=0.0.0.0
```

### 4. 检查 Ubuntu firewall (ufw)
```bash
sudo ufw status
```

如果处于 active 状态，请允许该端口：
```bash
sudo ufw allow 8080/tcp
sudo ufw reload
```

### 5. 浏览器 / 网络检查（从你的其他电脑）
- 尝试在 **无痕/私密模式**下访问 http://192.168.1.36:8080（cache/extensions 可能会干扰）。
- 尝试使用不同的浏览器。
- Ping 服务器：`ping 192.168.1.36`（必须有响应）。
- 测试端口连通性：在你的本地 PC 运行 `telnet 192.168.1.36 8080` 或使用在线端口检查工具。
- 如果连接被拒绝 → firewall/router 问题或 IP 错误。
- 确保你处于同一个局域网内 (192.168.1.x)。

### 6. 重置 WebUI 密码 / config（如果出现登录页但无法接受 admin/adminadmin）
停止 service → 删除或重命名 config：
```bash
sudo systemctl stop qbittorrent-nox
sudo mv /var/lib/qbittorrent/.config/qBittorrent/qBittorrent.conf /var/lib/qbittorrent/.config/qBittorrent/qBittorrent.conf.bak
sudo systemctl start qbittorrent-nox
```

手动运行一次以在终端查看临时密码：
```bash
sudo -u qbittorrent qbittorrent-nox
```

### 7. 如果 service 启动失败
- 检查 journalctl 输出中的错误（/var/lib/qbittorrent 的 permissions、缺少 libs 等）。
- 常见修复：确保文件夹所有权正确
```bash
sudo chown -R qbittorrent:qbittorrent /var/lib/qbittorrent
```

- 如果文件损坏则重新安装：
```bash
sudo apt reinstall qbittorrent-nox
```

### 诊断用的快速单行命令总结
```bash
sudo systemctl status qbittorrent-nox && sudo ss -tuln | grep 8080 && curl -I http://localhost:8080
```

运行该命令，如果仍然卡住请分享输出内容——它几乎能告诉我们所有信息。

References:

- [qBittorrent GitHub issues on WebUI problems](https://github.com/qbittorrent/qBittorrent/issues)
- [Running qBittorrent-nox systemd setup](https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-(WebUI-only,-systemd-service-set-up,-Ubuntu-15.04-or-newer))
- [Common qBittorrent-nox troubleshooting threads](https://www.reddit.com/r/qBittorrent)
