---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Nextcloud Talk提及功能丢失
translated: true
type: note
---

以下是导致消息被丢弃的流程：

1. `extensions/nextcloud-talk/src/inbound.ts:206-211` — 对于群组房间，会调用 `resolveNextcloudTalkRequireMention()`
2. `extensions/nextcloud-talk/src/policy.ts:105-116` — 若未配置房间级别或通配符覆盖规则，此项默认值为 `true`
3. `extensions/nextcloud-talk/src/inbound.ts:220-222` — 若 `mentionGate.shouldSkip` 为 true，消息将被丢弃并记录您所见的日志

提及检查使用 `buildMentionRegexes` 来匹配消息正文中的 `@OpenClaw` 等模式。若无匹配 → `wasMentioned = false` → 门控机制将其丢弃。

## 如何修复（无需代码修改）

在房间或通配符配置中设置 `requireMention: false`：

```bash
openclaw config set channels.nextcloud-talk.rooms.eu42ecdy.requireMention false
```

或针对所有房间设置：

```bash
openclaw config set channels.nextcloud-talk.rooms.*.requireMention false
```

## 如何检查/调试

- 观察网关日志中的 `nextcloud-talk: drop room` 行 — 这确认消息已抵达但被门控机制拦截
- 若要验证提及检测功能，请在 Nextcloud 房间发送包含 `@OpenClaw hello` 的消息 — 若机器人显示名称与提及正则表达式匹配，则应通过门控
- 检查已配置的提及模式：查看配置中的 `channels.nextcloud-talk.mentions`（或全局 `mentions` 配置）

最简解决方案：要么为该房间设置 `requireMention: false`，要么在 1:1 私聊中使用机器人（此时第206行的 `isGroup` 将为 `false`，提及门控将完全跳过）。
