---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 WebSocket Origin 检查拒绝错误
translated: true
type: note
---

WS 立即关闭，因为 origin 检查仍在拒绝它。浏览器在 WS 升级时发送 `Origin: http://192.168.1.36:18789`，它必须与 `allowedOrigins` 完全匹配。

同时运行以下两个修复：

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.36:18789"]'
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
```

然后重启：

```bash
systemctl --user restart openclaw-gateway.service
```

origin 必须是浏览器发送的**确切** origin 字符串 — scheme + host + port，没有尾随斜杠。由于您使用的是 `http://192.168.1.36:18789`，这就是值。

如果您想允许 LAN 上的任何客户端，而无需单独列出 IP，请使用 `"*"`：

```bash
openclaw config set gateway.controlUi.allowedOrigins '["*"]'
```