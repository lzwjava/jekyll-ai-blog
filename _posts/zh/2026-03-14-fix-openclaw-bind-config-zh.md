---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 OpenClaw 绑定配置错误
translated: true
type: note
---

Question: `openclaw config set server.host 0.0.0.0` 失败，提示 `Unrecognized key: "server"` — 如何正确配置 OpenClaw 以绑定到 `0.0.0.0`？Question: `openclaw config set server.host 0.0.0.0` 失败，提示 `Unrecognized key: "server"` — 绑定 OpenClaw gateway 到 `0.0.0.0` 以实现 LAN 访问的正确配置键是什么？

Answer:

## 根本原因

正确的配置键是 **`gateway.bind`**，而不是 `server.host`。在 `openclaw.json` 中，gateway 绑定由 `gateway.bind` 键控制，它接受诸如 `loopback`、`lan` 或自定义地址的值。

---

## 修复：逐步操作

### 步骤 1 — 首先停止 gateway

```bash
openclaw gateway stop
# or
systemctl --user stop openclaw-gateway.service
```

---

### 步骤 2 — 设置正确的绑定键

```bash
openclaw config set gateway.bind lan
```

gateway 支持多种绑定模式：`loopback`（仅 127.0.0.1）、`lan`（本地网络接口）、`tailnet`（Tailscale 接口）和 `custom`（指定地址）。除 `loopback` 外的每种模式都需要额外的身份验证配置。

---

### 步骤 3 — 或者直接编辑 `openclaw.json`

```bash
nano ~/.openclaw/openclaw.json
```

更改/添加 gateway 块：

```json
{
  "gateway": {
    "bind": "lan"
  }
}
```

如果要显式指定确切 IP：

```json
{
  "gateway": {
    "bind": "0.0.0.0"
  }
}
```

保存前验证 JSON：

```bash
python3 -m json.tool ~/.openclaw/openclaw.json
```

---

### 步骤 4 — 重新启动 gateway

```bash
openclaw gateway start
```

---

### 步骤 5 — 验证是否已绑定到 `0.0.0.0`

```bash
ss -tlnp | grep 18789
```

您应该看到：

```
LISTEN  0.0.0.0:18789  ...  openclaw-gateway
```

---

### 步骤 6 — 从主 PC 浏览器测试

```
http://192.168.1.36:18789
```

---

## ⚠️ 重要：更改绑定后需要 Auth Token

非 loopback 绑定强制要求身份验证。OpenClaw 每次重启都会生成新 token，除非您设置固定 token。要设置稳定 token：

```bash
openclaw config set gateway.token "your-stable-token-here"
```

在浏览器打开 `http://192.168.1.36:18789` 时，它会要求输入此 token。随时检索它：

```bash
openclaw config get gateway.token
```

或获取包含 token 的完整 dashboard URL：

```bash
openclaw dashboard --no-open
```

---

## 正确键汇总

| 错误（导致错误） | 正确 |
|---|---|
| `server.host` | `gateway.bind` |
| `server.port` | `gateway.port` |

```bash
# 正确命令
openclaw config set gateway.bind lan
openclaw config set gateway.port 18789
openclaw config set gateway.token "your-token"
```

References:

- [OpenClaw Config Reference - ClawTank](https://clawtank.dev/blog/openclaw-config-reference)
- [OpenClaw Port Troubleshooting Guide - AI Free API](https://www.aifreeapi.com/en/posts/openclaw-port-not-listening)
- [OpenClaw 127.0.0.1:18789 Binding Guide](https://openclawconsult.com/lab/openclaw-127-0-0-1-18789)