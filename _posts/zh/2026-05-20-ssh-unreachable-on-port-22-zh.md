---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH在端口22不可达
translated: true
type: note
---

`165.245.135.10` 上的 22 端口拒绝连接——无论使用哪个用户名，SSH 都无法接入。只有 80 端口（HTTP）处于开放状态。

```
PORT   STATE SERVICE
80/tcp open  http
```

你的 SSH 配置会将非本地 IP 通过 SOCKS5 代理（localhost:7891）路由，但即使通过代理，该主机的 22 端口仍是关闭的。

可能的原因：
- 服务器的防火墙/安全组未允许 22 端口
- SSH 运行在非标准端口上（我扫描了约 15 个常见替代端口——均未开放）
- 服务器可能已宕机或 SSH 服务未运行
- 你可能需要通过 VPN 或跳板机才能访问它

你能否检查服务器的防火墙，或者告诉我 SSH 实际所在的端口？