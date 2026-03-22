---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 WebSocket 连接和来源错误
translated: true
type: note
---

**HTTP 对于你的情况是可行的** — `ws://` 错误并不是由于使用 HTTP 导致的。原因如下：

- 只有当 **页面本身通过 HTTPS 提供服务** 时（混合内容拦截），浏览器才会拦截 `ws://`。由于你正在访问 `http://192.168.1.36:18789`（普通 HTTP），`ws://` 是完全允许的。
- 只有当你前面放了提供 HTTPS 的 reverse proxy 时，才需要 HTTPS + `wss://`。

**真正的原因** 仍然是 server-side 的 origin check 拒绝了连接并立即将其关闭 — 这就是导致 "closed before connection established" 的原因。根据搜索结果，最常见的原因包括：

1. **CORS/Origin 配置错误** — server 拒绝了 origin header（你的情况）
2. **无效的 port/host** — client 连接的地址与 server 监听的地址不匹配
3. **Server 未配置 WebSocket upgrades**

**检查你的 config 更改是否已实际保存：**

```bash
openclaw config get gateway.controlUi
```

如果 `allowedOrigins` 或 `dangerouslyDisableDeviceAuth` 不存在，请重新运行：

```bash
openclaw config set gateway.controlUi.allowedOrigins '["*"]'
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
systemctl --user restart openclaw-gateway.service
```

然后检查 gateway logs 以获取实际的拒绝原因：

```bash
journalctl --user -u openclaw-gateway.service -n 100 --no-pager | grep -i "origin\|closed\|reject\|error"
```

Sources:
- [Sentry: How to fix "WebSocket is closed before the connection is established"](https://sentry.io/answers/how-do-i-fix-the-error-websocket-is-closed-before-the-connection-is-established/)
- [wss vs ws explained — WebSocket.org](https://websocket.org/reference/wss-vs-ws/)
- [WS on HTTP vs WSS on HTTPS — APIdog](https://apidog.com/blog/ws-on-http-vs-wss-on-https/)