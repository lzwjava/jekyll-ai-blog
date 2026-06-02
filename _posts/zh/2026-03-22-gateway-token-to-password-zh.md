---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将网关令牌切换为密码
translated: true
type: note
---

要从 gateway token 切换为 password：

**1. 设置 password：**
```bash
openclaw config set gateway.auth.password "your-password"
```

**2. 将 auth mode 设置为 password：**
```bash
openclaw config set gateway.auth.mode password
```

**3. 移除旧的 token（可选，但建议这样做以避免歧义）：**
```bash
openclaw config set gateway.auth.token ""
```

如果 config 中同时存在 `gateway.auth.token` 和 `gateway.auth.password`，你 **必须** 显式设置 `gateway.auth.mode`，否则 startup 将会失败。

你也可以通过 environment variable 而不是 config 来设置 password：
```bash
export OPENCLAW_GATEWAY_PASSWORD="your-password"
```

专门针对 remote gateway 连接，请使用 `gateway.remote.password` 代替 `gateway.auth.password`。
