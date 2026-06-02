---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hysteria ACME 验证需要 80 端口
translated: true
type: note
---

**问题：** 当 Hysteria 处理 Let's Encrypt 时，为什么需要开放端口 80，使用 UFW？

**回答：**

Hysteria（特别是 **Hysteria 2**）内置了 **ACME client** 支持，可以自动从 **Let's Encrypt**（或 ZeroSSL）获取和续期 **TLS certificates**。

Let's Encrypt 主要使用两种 Hysteria 支持的验证方法：

- **http-01** challenge → 需要 **TCP port 80** 公网可达。
- **tls-alpn-01** challenge → 需要 **TCP port 443** 公网可达。

默认情况下，当你在 Hysteria 的配置文件中配置 `acme` 部分（例如 `listenHTTP: :80`）时，它使用 **http-01** challenge。Let's Encrypt 服务器会连接到你的域名 **<http://yourdomain.com/.well-known/acme-challenge/...**（纯> HTTP，端口 80）来验证你控制该域名。

如果你的防火墙（例如 UFW）中 **port 80 被阻塞**，验证将失败，并出现如下错误：

- "Connection refused"
- "Timeout during connect (likely firewall problem)"
- "Fetching http://... : Connection refused"

这就是为什么你必须在 UFW 中允许入站 **TCP/80**（至少在初始颁发和续期期间）：

```bash
sudo ufw allow 80/tcp
```

Hysteria 的文档明确警告：

> (Note: Changing to a port other than 80 requires port forwarding or HTTP reverse proxy, or the challenge will fail!)

**始终保持端口 80 关闭的替代方案：**

1. 仅使用 **tls-alpn-01** challenge
   在 acme 部分设置 `disableHTTP: true` → Hysteria 将尝试 **tls-alpn-01**（仅端口 443）。
   如果端口 443 已开放（Hysteria 反正必须开放它），这有效。

2. 使用 **DNS-01** challenge
   这不需要在服务器上开放任何端口。
   你必须使用支持你的 DNS 提供商 API 的 ACME client（例如 acme.sh、带 DNS 插件的 certbot，或手动设置），然后将 Hysteria 指向获取到的证书文件。

3. 使用 **external tool** 如 certbot 的 `--standalone` 或 `--webroot` 模式（仅在续期期间通过 hooks/scripts 临时开放端口 80）。

大多数简单的 Hysteria 设置使用内置的 ACME 与 **http-01**，因为它自动且方便——但这就是端口 80 必须在 UFW 中允许的主要原因。

**参考：**

- <https://v2.hysteria.network/docs/advanced/Full-Server-Config>
- <https://letsencrypt.org/docs/allow-port-80>
- <https://letsencrypt.org/docs/challenge-types>
- <https://github.com/apernet/hysteria/issues/942>
