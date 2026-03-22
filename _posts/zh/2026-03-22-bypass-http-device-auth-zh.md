---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 绕过设备认证以使用明文 HTTP
translated: true
type: note
---

您需要设置 `gateway.controlUi.dangerouslyDisableDeviceAuth=true` 以绕过纯 HTTP 上的安全上下文要求：

```bash
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
```

然后重启：

```bash
systemctl --user restart openclaw-gateway.service
```

这将禁用设备身份验证，并改为依赖您的 token/password auth。它在审计输出中被标记为危险，但这是为受信任的 LAN 上的纯 HTTP 提供的预期逃生舱。添加 HTTPS 时（例如通过带有 cert 的 reverse proxy），请将其关闭。