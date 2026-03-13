---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快速修复 OpenClaw Origin 错误
translated: true
type: note
---

问题：从另一台机器访问 `http://192.168.1.36:18789` 时，OpenClaw 显示 "origin not allowed" 错误 — 如何通过配置 `gateway.controlUi.allowedOrigins` 来修复此问题？

回答：

## 根本原因

OpenClaw 在 Control UI 上有一个 **CORS/origin 安全检查**。当您从与 gateway 主机 (`192.168.1.36`) 不同的机器 (`192.168.1.100`) 打开 dashboard 时，origin 默认被阻止。

---

## 修复：将您的 LAN IP 添加到 `allowedOrigins`

### 步骤 1 — 停止 gateway

```bash
openclaw gateway stop
# or
systemctl --user stop openclaw-gateway.service
```

---

### 步骤 2 — 通过 config 命令设置允许的 origins

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.36:18789"]'
```

如果您想允许 **LAN 上的任意机器**（更灵活）：

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.36:18789","http://192.168.1.100:18789","http://192.168.1.1:18789"]'
```

或者最简单的方法 — **允许所有 origins**（适用于家庭 LAN）：

```bash
openclaw config set gateway.controlUi.allowedOrigins '["*"]'
```

---

### 步骤 3 — 或者直接编辑 `openclaw.json`

```bash
nano ~/.openclaw/openclaw.json
```

在 `gateway` 块内添加：

```json
{
  "gateway": {
    "bind": "lan",
    "port": 18789,
    "controlUi": {
      "allowedOrigins": [
        "http://192.168.1.36:18789",
        "http://192.168.1.100"
      ]
    }
  }
}
```

允许所有（通配符）：

```json
{
  "gateway": {
    "bind": "lan",
    "port": 18789,
    "controlUi": {
      "allowedOrigins": ["*"]
    }
  }
}
```

验证 JSON 语法：

```bash
python3 -m json.tool ~/.openclaw/openclaw.json
```

---

### 步骤 4 — 重启 gateway

```bash
openclaw gateway start
```

---

### 步骤 5 — 在主 PC 上打开浏览器

```
http://192.168.1.36:18789
```

现在应该可以加载 Control UI 而不会出现 origin 错误。

---

## 完整的推荐 `openclaw.json` Gateway 块

以下是适用于家庭 LAN 设置的干净完整的 gateway 配置：

```json
{
  "gateway": {
    "bind": "lan",
    "port": 18789,
    "controlUi": {
      "allowedOrigins": ["*"]
    }
  }
}
```

---

## 总结

| 配置键 | 用途 |
| --- | --- |
| `gateway.bind` | 监听的接口（`lan` = LAN IP） |
| `gateway.port` | 端口号（默认 `18789`） |
| `gateway.controlUi.allowedOrigins` | 允许打开 UI 的浏览器 origins |

在家庭 LAN 上使用 `["*"]` 是 **安全的**，因为 UFW 已经阻止了对端口 `18789` 的外部访问。只有 `192.168.1.x` 上的设备才能访问它。