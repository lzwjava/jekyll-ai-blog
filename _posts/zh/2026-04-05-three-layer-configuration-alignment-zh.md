---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 三层配置对齐问题
translated: true
type: note
---

## 扩展：三层配置问题

### 配置存放位置

```
┌─────────────────────────────────────────────────────────────────────────┐
│  配置位置 #1: Nextcloud config.php                                       │
│  文件: /path/to/nextcloud/config/config.php                              │
│  键:   'overwrite.cli.url'                                               │
│  用途: Nextcloud 向机器人告知自身信息                                    │
│  值: 'http://localhost:8080'                                             │
│  使用方: Nextcloud 发送 X-Nextcloud-Talk-Backend 头部时使用              │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
                         该值进入请求头部
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  配置位置 #2: OpenClaw openclaw.json                                    │
│  文件: ~/.openclaw/openclaw.json                                        │
│  键:  baseUrl, webhookPublicUrl, botSecret, rooms[].requireMention      │
│  用途: OpenClaw 如何验证并响应 Nextcloud                                │
│                                                                         
│  baseUrl = "http://localhost:8080"                                      │
│    ↑ 必须与 X-Nextcloud-Talk-Backend 头部值完全匹配                      │
│    ↓ 同时用于传入签名验证 和 传出 API 调用                                │
│                                                                         
│  webhookPublicUrl = "http://172.17.0.1:8788"                           │
│    ↑ Nextcloud 应向此地址发送 webhook（必须能从 Docker 网络内访问到）      │
│                                                                         
│  botSecret = "bgCDXVAqsN3MX..."                                         │
│    ↑ 用于 HMAC 签名的共享密钥（必须与机器人注册时匹配）                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
                        OpenClaw 回复时调用此 URL
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  配置位置 #3: Nextcloud 数据库 (oc_talk_bots_server)                    │
│  表: oc_talk_bots_server                                               │
│  列: id, name, url, url_hash, secret, features, state                  │
│  用途: Nextcloud 内部记录的已注册机器人信息                             │
│                                                                         
│  url = "http://172.17.0.1:8788/nextcloud-talk-webhook"                 │
│    ↑ Nextcloud 在消息到达时调用的 webhook URL                           │
│    ↑ 必须与 OpenClaw 的 webhookPublicUrl 匹配                           │
│                                                                         
│  secret = "bgCDXVAqsN3MX..."                                            │
│    ↑ 必须与 OpenClaw 的 botSecret 匹配                                  │
│    ↑ 由 Nextcloud 用于签署传出的 webhooks                               │
│    ↑ 由 OpenClaw 用于验证传入的签名                                      │
│                                                                         
│  表: oc_talk_bots_conversation                                         │
│  列: id, bot_id, token, state                                          │
│  用途: 机器人启用于哪些房间                                             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 对齐矩阵

| 设置项 | config.php | openclaw.json | 数据库 | 必须匹配 |
|---------|------------|---------------|----------|------------|
| Nextcloud 内部 URL | `http://localhost:8080` | `baseUrl` | - | ✅ 三者 |
| Webhook URL (公开) | - | `webhookPublicUrl` | `url` 列 | ✅ 两者 |
| 共享密钥 | - | `botSecret` | `secret` 列 | ✅ 两者 |
| 房间启用状态 | - | `rooms.eu42ecdy` | `oc_talk_bots_conversation` | ✅ 两者 |

**如果其中任何一项未对齐，系统会静默失效。**

---

### 签名验证与 API 调用：静默的不匹配

这是最令人困惑的部分。原因如下：

#### "签名验证"的含义

```
┌──────────────────────────────────────────────────────────────────┐
│  NEXTcloud 向 OpenClaw 发送 webhook                               │
│                                                                   │
│  头部:                                                             │
│    X-Nextcloud-Talk-Backend: http://localhost:8080               │
│    X-Nextcloud-Talk-Random: <random-64-chars>                    │
│    X-Nextcloud-Talk-Signature: <hmac-sha256>                      │
│                                                                   │
│  正文:                                                            │
│    {"type":"Activity", "actor":{...}, "object":{...}, ...}       │
└──────────────────────────────────────────────────────────────────┘
                              ↓
                    OpenClaw 验证签名
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  签名 = HMAC-SHA256(                                             │
│    Random + Body,    ← 拼接的字符串                                │
│    BotSecret         ← 共享密钥                                    │
│  )                                                                 │
│                                                                   │
│  OpenClaw 使用其 botSecret 计算此值                                │
│  与 X-Nextcloud-Talk-Signature 头部值进行比较                     │
│  若匹配 → 请求验证通过 ✅                                          │
│  若不匹配 → 401 无效签名 ❌                                        │
└──────────────────────────────────────────────────────────────────┘
```

**此验证过程使用 `baseUrl` 来检查 `X-Nextcloud-Talk-Backend` 头部。**

---

#### "API 调用"的含义

```
┌──────────────────────────────────────────────────────────────────┐
│  OPENCLAW 向 Nextcloud 发送回复                                   │
│                                                                   │
│  OpenClaw 调用:                                                   │
│    POST http://localhost:8080/ocs/v2.php/apps/spreed/...         │
│                 ↑                                                 │
│                 baseUrl 也在这里使用！                            │
└──────────────────────────────────────────────────────────────────┘
                              ↓
                   Nextcloud 接收 API 调用
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  如果 baseUrl = "http://localhost" (不带端口):                    │
│    Nextcloud 未监听 80 端口                                       │
│    nginx 在 80 端口 → 返回 404                                   │
│    OpenClaw 看到: "room not found (token=eu42ecdy)"              │
│                                                                   │
│  如果 baseUrl = "http://localhost:8080":                         │
│    Nextcloud 监听 8080 端口                                       │
│    返回正确响应 ✅                                                │
└──────────────────────────────────────────────────────────────────┘
```

---

### 为何看起来像是"签名验证通过但 API 调用失败"

```
NEXT CLOUD 日志 (Nextcloud 向我们报告的内容):
┌─────────────────────────────────────────────────────────────┐
│  POST http://172.17.0.1:8788/nextcloud-talk-webhook        │
│  ← 这是向 OpenClaw 发送的 webhook 请求                      │
│                                                             │
│  结果: 401 Invalid backend                                  │
│  ← OpenClaw 因 baseUrl 不匹配而拒绝                         │
│                                                             │
│  但是: Nextcloud 不知道失败原因                             │
│  它只看到最终的 401 响应                                     │
└─────────────────────────────────────────────────────────────┘

OPENCLAW 日志 (OpenClaw 向我们报告的内容):
┌─────────────────────────────────────────────────────────────┐
│  收到来自 Nextcloud 的 webhook                              │
│  签名检查... 失败 (401 Invalid backend)                     │
│  ← 这阻止了我们看到实际负载                                  │
│                                                             │
│  之后，修复 baseUrl 后:                                     │
│  收到 webhook (成功)                                        │
│  尝试向 http://localhost/ocs/... 发送回复                  │
│  ← 但我们从未记录该 URL 解析为何种情况                      │
│                                                             │
│  响应: 404                                                  │
│  我们记录: "room not found (token=eu42ecdy)"               │
│  ← 这个错误信息并未告诉我们 URL 是错误的！                  │
└─────────────────────────────────────────────────────────────┘
```

**静默故障的原因：** OpenClaw 的错误信息显示"找不到房间"，但真正的问题是"我尝试调用 `http://localhost/ocs/v2.php/...`，它命中了 nginx（80 端口）而不是 Nextcloud（8080 端口）。"

---

### 三个静默故障点

| 故障点 | 我们的预期 | 实际情况 | 错误信息 |
|---------------|------------------|------------------------|---------------|
| **签名** | `baseUrl` 与头部匹配 | `baseUrl` 是 `http://172.17.0.1:8080`，头部是 `http://localhost` | `401 Invalid backend` |
| **负载解析** | `type` 是 "Create" | Nextcloud 发送 `type: "Activity"` | `400 Invalid payload format` |
| **API 调用** | `http://localhost:8080` 有效 | `http://localhost`（80 端口）→ nginx → 404 | `room not found` |

每个故障都隐藏在前一个故障背后，因为：
1. 签名拒绝 = 负载从未被解析
2. 负载拒绝 = API 从未被调用
3. API 404 = 看起来像是房间问题，而不是 URL 问题

---

### 端口 80 与端口 8080 的混淆

```
┌────────────────────────────────────────────────────────────────┐
│  你的笔记本电脑 (你访问服务的位置)                               │
│                                                                 │
│  端口 80:   nginx 反向代理 (处理 https://yourdomain.com)        │
│  端口 8080: Docker 内的 Nextcloud Apache                         │
│                                                                 │
│  当 OpenClaw 从宿主机调用 "http://localhost:8080" 时:          │
│    localhost = 宿主机                                           │
│    :8080 = Docker 端口映射 → 可达 Nextcloud ✅                   │
│                                                                 │
│  当 OpenClaw 调用 "http://localhost" (无端口) 时:              │
│    localhost = 宿主机                                           │
│    (默认端口 80) → 到达 nginx ❌                                 │
│    nginx 不认识 /ocs/v2.php/... → 404                          │
└────────────────────────────────────────────────────────────────┘
```

**这就是为什么 `http://localhost` 对签名验证有效（Nextcloud 发送它，OpenClaw 比较它）但对 API 调用失败（OpenClaw 使用它进行调用，命中了错误的服务）。** 🦞