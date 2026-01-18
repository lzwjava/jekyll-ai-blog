---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Hysteria 2 服务器搭建指南
translated: true
type: note
---

**Question:** 如何在服务器上设置 Hysteria 2？

**Answer:**

这是一份清晰且最新的指南（截至 2026 年），用于在 Linux VPS（最常见的情况，如 Ubuntu/Debian/CentOS 等）上部署 **Hysteria 2** 服务器。

### Prerequisites

- 拥有 **public IP**（IPv4 和/或 IPv6）的 VPS
- 指向服务器 IP 的 **domain name**（A/AAAA 记录）
- Root 或 sudo 权限
- 防火墙已开放 **443** 端口 (UDP)（非常重要 —— Hysteria 2 使用 QUIC/UDP）
- 可选但强烈建议：具备获取真实 TLS certificate 的能力（通过 ACME/Let's Encrypt）

### Recommended Method: 使用官方一键安装脚本

这是 Linux 服务器最简单且持续维护的方法。

1. 运行官方 bash 脚本（安装 binary 并创建 systemd service）：
   ```bash
   bash <(curl -fsSL https://get.hy2.sh/)
   ```
   - 它会根据你的架构（amd64/arm64）下载最新的 Hysteria 2 binary
   - 安装到 `/usr/local/bin/hysteria`
   - 创建 `/etc/hysteria/config.yaml`（示例配置）
   - 设置 systemd service：`hysteria-server.service`

2. 编辑配置文件：
   ```bash
   nano /etc/hysteria/config.yaml
   ```

   **最小化可行示例（ACME 自动证书 + password 认证）：**
   ```yaml
   listen: :443

   acme:
     domains:
       - your.domain.com           # ← 更改为你的域名
     email: your@email.com         # ← 用于 Let's Encrypt 的邮箱

   auth:
     type: password
     password: YOUR_STRONG_PASSWORD_HERE   # ← 更改此处！

   masquerade:
     type: proxy
     proxy:
       url: https://news.ycombinator.com/   # ← 伪装站点（有助于应对 DPI）
       rewriteHost: true
   ```

   **另一种方案（如果你已经有了自己的 cert/key）：**
   ```yaml
   listen: :443

   tls:
     cert: /path/to/fullchain.pem
     key: /path/to/privkey.pem

   auth:
     type: password
     password: YOUR_STRONG_PASSWORD_HERE

   masquerade:
     type: proxy
     proxy:
       url: https://www.bing.com/
       rewriteHost: true
   ```

   **配置说明：**
   - 端口 443 是默认端口且强烈推荐（看起来像正常的 HTTP/3）
   - `masquerade` 让服务器响应像一个真实的网站 → 极难被屏蔽
   - 对于个人使用，你可以完全删除 `bandwidth` 限制（或设置得非常高）
   - 保存并退出

3. 启动并启用服务：
   ```bash
   systemctl start hysteria-server
   systemctl enable hysteria-server
   ```

4. 检查状态和日志：
   ```bash
   systemctl status hysteria-server
   journalctl -u hysteria-server -e -f
   ```

   查找：`server up and running` → 成功！

### Alternative: 手动安装（不用脚本）

1. 下载最新 binary：
   ```bash
   wget https://download.hysteria.network/app/latest/hysteria-linux-amd64   # 或 -arm64
   chmod +x hysteria-linux-amd64
   mv hysteria-linux-amd64 /usr/local/bin/hysteria
   ```

2. 允许非 root 用户绑定低位端口：
   ```bash
   setcap cap_net_bind_service=+ep /usr/local/bin/hysteria
   ```

3. 按照上文创建配置文件（例如 `/etc/hysteria/config.yaml`）。

4. 手动运行（进行调试）：
   ```bash
   hysteria server -c /etc/hysteria/config.yaml
   ```

5. 自行创建 systemd service（或使用上述脚本方法）。

### Firewall (以 ufw 为例)

```bash
ufw allow 443/udp
ufw reload
```

### After Setup

- 服务器会打印（或记录）一个 `hysteria2://` URI → 直接分享给 client（例如 NekoBox, sing-box, Shadowrocket）
- 示例 client 代码片段：
  ```yaml
  server: your.domain.com:443
  auth: YOUR_STRONG_PASSWORD_HERE
  bandwidth:
    up: 30 mbps
    down: 200 mbps
  ```

### Common Tips / Troubleshooting

- 确保 VPS 提供商/防火墙没有屏蔽 **UDP 443**
- 如果 ACME 失败 → 检查 DNS 解析是否生效，80 端口是否临时开放（用于 http-01 验证），或使用 DNS-01 验证
- 无伪装 (No masquerade) = 服务器返回 404 → 仍然可用但更容易被发现
- 为了获得极高性能 → 将 `bandwidth` 调整为实际值（server 的 upload = client 的 download）

**References:**

- [Official Server Quick Start](https://v2.hysteria.network/docs/getting-started/Server/)
- [Official Installation Page](https://v2.hysteria.network/docs/getting-started/Installation/)
- [Server Installation Script](https://v2.hysteria.network/docs/getting-started/Server-Installation-Script/)
- [Full Server Configuration Reference](https://v2.hysteria.network/docs/advanced/Full-Server-Config/)