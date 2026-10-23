---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Cloudflare 上配置 HTTPS
translated: true
type: note
---

Question: 如何为 Cloudflare 中的域名添加 HTTPS 支持？

Answer:

Cloudflare 让启用 HTTPS 变得简单直接。以下为主要步骤：

**快速建议：**

- 对于大多数网站：使用 **Full (Strict)** 模式 + **Always Use HTTPS** 开关。这样可以提供正确的端到端加密。
- 如果您的源服务器还没有 SSL 证书：暂时从 **Flexible** 开始，然后安装 Cloudflare Origin Certificate 并切换到 **Full (Strict)**。

**SSL 模式摘要：**

| 模式 | 访问者 ↔ Cloudflare | Cloudflare ↔ 源服务器 |
| --- | --- | --- |
| Flexible | HTTPS | HTTP |
| Full | HTTPS | HTTPS（自签名证书可以） |
| Full (Strict) | HTTPS | HTTPS（需要有效证书） |

---

参考文献：

- [Cloudflare SSL/TLS 概述](https://developers.cloudflare.com/ssl/get-started/)
- [Cloudflare 边缘证书](https://developers.cloudflare.com/ssl/edge-certificates/)
- [Cloudflare 源服务器 CA 证书](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/)
- [始终使用 HTTPS 设置](https://developers.cloudflare.com/ssl/edge-certificates/additional-options/always-use-https/)
