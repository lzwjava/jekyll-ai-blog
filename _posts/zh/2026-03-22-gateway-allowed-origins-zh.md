---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 配置网关允许来源
translated: true
type: note
---

配置键是 `gateway.controlUi.allowedOrigins`。您可以列出特定来源，或者使用 `"*"` 来允许所有来源。

对于您的 LAN 设置，通过以下方式设置：

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.1", "http://192.168.1.2"]'
```

或者允许**任意**来源（通配符 — 对于受信任的 LAN 更简单）：

```bash
openclaw config set gateway.controlUi.allowedOrigins '["*"]'
```

注意：`"*

` 会完全禁用来源白名单（审计会警告，但不会阻止启动）。对于私有 LAN，这通常是可以接受的。

更新后，重启 gateway：

```bash
systemctl --user restart openclaw-gateway.service
```