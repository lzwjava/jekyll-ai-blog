---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Webhook重启后未接收消息
translated: true
type: note
---

**当前状态总结：**

1. ✅ 配置正确：聊天室 `eu42ecdy` 已设置 `requireMention: false`
2. ✅ 网关正在运行
3. ✅ Webhook 监听于 `http://localhost:8788/nextcloud-talk-webhook`
4. ✅ 去重文件已清空（状态为 `{}`）
5. ❌ **重启后未收到新的 Webhook 消息**（日志中仅显示我自己的命令）

**问题描述：** 重启后网关未从 Nextcloud Talk 接收到任何新消息。

**疑问点：**

1. **您在重启后（凌晨 02:03 之后）是否从 Nextcloud Talk 发送过新消息？**
2. 还是您查看的是之前被拦截的同一条旧消息？

如果您确实发送了新消息但问题仍存在，可能的原因包括：

- **Nextcloud Talk 重复发送 messageId=1** —— 每条消息 ID 相同，因此重启后的第一条消息会被处理，但后续所有 ID=1 的消息都会被重放防护机制拦截（因为第一条消息的记录已存入去重系统）

能否请您检查 Nextcloud Talk 当前发送的消息 ID？或者尝试立即发送一条消息，以便我实时查看日志？