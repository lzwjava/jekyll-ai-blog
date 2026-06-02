---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为 OpenClaw 启用局域网访问
translated: true
type: note
---

问题：OpenClaw gateway 绑定到 `127.0.0.1:18789`，无法通过 `http://192.168.1.36:18789` 访问。是否应该重新绑定到 `0.0.0.0` 以允许 LAN 访问？

答案：

## 根本原因

日志清楚显示：

```
pid 85445 lzw: openclaw-gateway (127.0.0.1:18789)
```

OpenClaw **仅监听 localhost** (`127.0.0.1`)，不在 LAN 接口上监听。这就是为什么 `192.168.1.36:18789` 无法连接——端口从机器外部无法访问。

**是的，您需要绑定到 `0.0.0.0`** 以允许 LAN 访问。由于您处于私有家庭网络 (`192.168.1.x`) 且 UFW 已限制为仅 LAN，这很安全。

---

## 步骤 1 — 首先停止 Gateway

```bash
openclaw gateway stop
# or
systemctl --user stop openclaw-gateway.service
```

验证它已停止：

```bash
ss -tlnp | grep 18789
# should return nothing
```

---

## 步骤 2 — 将绑定地址设置为 `0.0.0.0`

```bash
openclaw config set server.host 0.0.0.0
```

或手动编辑配置文件：

```bash
nano ~/.openclaw/openclaw.json
```

添加或更新 `server` 块：

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 18789
  }
}
```

---

## 步骤 3 — 重新启动 Gateway

```bash
openclaw gateway start
```

验证它现在监听在 `0.0.0.0` 上：

```bash
ss -tlnp | grep 18789
```

您现在应该看到：

```
LISTEN  0.0.0.0:18789   ...   openclaw-gateway
```

而不是 `127.0.0.1:18789`。

---

## 步骤 4 — 确认 UFW 仍保护它

由于您绑定到 `0.0.0.0`，请再次检查 UFW 仅允许您的 LAN：

```bash
sudo ufw status numbered
```

确保您有此规则（来自之前步骤）：

```
ALLOW IN    192.168.1.0/24    18789
```

如果没有，添加它：

```bash
sudo ufw allow from 192.168.1.0/24 to any port 18789
sudo ufw reload
```

---

## 步骤 5 — 从主 PC 测试

在您的主计算机上打开浏览器并访问：

```
http://192.168.1.36:18789
```

或从主 PC 使用 curl 测试：

```bash
curl http://192.168.1.36:18789
```

---

## 安全摘要

| 绑定 | 可从何处访问 | 安全？ |
|---|---|---|
| `127.0.0.1` | 仅 localhost | ✅ 最安全，但无法从 LAN 访问 |
| `0.0.0.0` + UFW LAN 规则 | 仅您的家庭 LAN | ✅ 适合家庭使用 |
| `0.0.0.0` + 无 UFW | 任何人包括互联网 | ❌ 危险 |

您的 `0.0.0.0` + UFW 规则 `192.168.1.0/24` 配置对于家庭网络来说 **完全安全**。
