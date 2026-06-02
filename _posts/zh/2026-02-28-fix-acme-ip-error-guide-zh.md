---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Hysteria ACME IP 错误指南
translated: true
type: note
---

```
invalid config: acme.domains: 64.186.xx.xx: >
...
hysteria-server.service: Main process exited, code=exited, status=1/FAILURE
```

表示 **Hysteria 2 启动失败，因为 ACME 配置无效**。具体来说，您在 `acme.domains` 列表中放置了 **IP 地址** (`64.186.xx.xx`) 而不是有效的域名。

### 为什么会发生这种情况

- `acme` 部分用于通过 Let's Encrypt（或类似服务）使用 ACME 协议进行 **自动证书颁发/续期**。
- Let's Encrypt（以及大多数 ACME CA）**无法为原始 IP 地址颁发证书** — 它们需要 **完全限定域名 (FQDN)**，如 `example.com` 或 `vpn.mydomain.net`。
- Hysteria 2 在启动时验证这一点：如果 `acme.domains` 包含无效域名（或其他原因导致证书颁发失败），它会将整个配置视为无效并以状态码 1 退出。
- 您的部分错误消息被截断 (`64.186.xx.xx: >`)，但很可能继续显示类似 "obtaining certificate: ... invalid domain" 或其他验证失败的内容。

### 如何修复

根据您是否有（或想要）域名，有两种主要选项。

#### 选项 1: 使用真实域名（推荐以获得最佳兼容性）
1. **获取域名**（如果您还没有）：从 Namecheap、Porkbun 等处购买一个廉价域名，并将其 A 记录指向服务器 IP (64.186.xx.xx)。
   - 示例：`hy2.mydomain.com` → A 记录 → 64.186.xx.xx

2. **编辑 `/etc/hysteria/config.yaml`**：
   将 IP 替换为您的域名：
   ```yaml
   listen: :443

   acme:
     domains:
       - hy2.mydomain.com          # ← 更改为您的实际域名
     email: your@email.com         # Let's Encrypt 通知所需

   auth:
     type: password
     password: your-strong-password

   # ... 您的配置其余部分 ...
   ```

3. **重启服务**：
   ```bash
   systemctl restart hysteria-server
   ```

4. **检查日志**：
   ```bash
   journalctl -u hysteria-server -e
   ```
   - 首次启动时，它将请求证书（需要临时打开 TCP 端口 80 以进行 HTTP-01 验证，或使用 DNS-01 如果端口 80 被阻塞）。
   - 如果端口 80 被防火墙阻止：临时添加 `ufw allow 80/tcp`，或切换到 DNS 验证（见下文）。

#### 选项 2: 使用自签名证书（无需域名，快速修复）
如果您没有/不想使用域名，请禁用 ACME 并使用手动/自签名 TLS。

1. **生成自签名证书**（针对您的 IP 或任意 CN）：
   ```bash
   mkdir -p /etc/hysteria/certs
   openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
     -keyout /etc/hysteria/certs/server.key \
     -out /etc/hysteria/certs/server.crt \
     -subj "/CN=64.186.xx.xx" \
     -addext "subjectAltName = IP:64.186.xx.xx"
   ```

   （或使用 Hysteria 文档中的脚本以获得更多选项。）

2. **更新 config.yaml** — 完全移除 `acme` 并添加 `tls`：
   ```yaml
   listen: :443

   tls:
     cert: /etc/hysteria/certs/server.crt
     key: /etc/hysteria/certs/server.key

   auth:
     type: password
     password: your-strong-password

   masquerade:
     type: proxy
     proxy:
       url: https://news.ycombinator.com/
       rewriteHost: true
   ```

3. **重启**：
   ```bash
   systemctl restart hysteria-server
   ```

4. **在 Shadowrocket (iOS 客户端)**：
   - 启用 **insecure** / **Allow Insecure**（或在 hy2:// URI 中添加 `&insecure=1`）。
   - 使用 SNI = 服务器 IP 或留空（某些客户端允许空 SNI）。
   - 这可以工作，但浏览器/应用可能显示警告；用于代理是没问题的。

#### 可选: 使用 DNS 验证的高级 ACME（如果端口 80 被阻塞）
如果您有域名但无法打开 TCP/80：
```yaml
acme:
  domains:
    - hy2.mydomain.com
  email: your@email.com
  type: dns
  dns:
    name: cloudflare          # 或 godaddy 等
    config:
      cloudflare_api_token: your-api-token-here
```

请参阅官方文档以获取支持的提供商。

修复配置后，服务应该正常启动（`systemctl status hysteria-server` 显示 active/running）。

参考资料：

- [Hysteria 2 Full Server Config (tls vs acme)](https://v2.hysteria.network/docs/advanced/Full-Server-Config)
- [Hysteria 2 ACME DNS Config (alternative to HTTP challenge)](https://v2.hysteria.network/docs/advanced/ACME-DNS-Config)
- [GitHub Issue - ACME failures and config examples](https://github.com/apernet/hysteria/issues/942)
