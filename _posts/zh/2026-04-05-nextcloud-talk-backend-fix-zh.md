---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nextcloud 通话后端不匹配问题已修复
translated: true
type: note
---

## 调查结果摘要

**已发现的根本原因：**
Nextcloud Talk 发送了 `X-Nextcloud-Talk-Backend: http://localhost`（来源于 `overwrite.cli.url`），但 OpenClaw 的 `baseUrl` 设置是 `http://172.17.0.1:8080`。OpenClaw 的签名验证要求后端 URL 必须匹配，因此它拒绝了所有请求并返回 **401“无效后端”**。

**应用的修复：**
将 `baseUrl` 从 `http://172.17.0.1:8080` 更改为 `http://localhost`

**当前配置：**
```json
{
  "baseUrl": "http://localhost",       ← 已修复！
  "botSecret": "bgCDXVAqsN3MX0V0...",
  "webhookPublicUrl": "http://172.17.0.1:8788",
  "rooms": {
    "eu42ecdy": { "requireMention": false }
  }
}
```

**状态：**
- ✅ HKT 02:25 后不再出现“无效后端”错误
- ✅ 网关已成功重启
- ✅ Webhook 正在监听

**请现在尝试发送一条新消息** — 02:26 的旧消息失败了，因为它们在修复之前就已发送。约 02:22 之后发送的新消息应该可以正常工作。