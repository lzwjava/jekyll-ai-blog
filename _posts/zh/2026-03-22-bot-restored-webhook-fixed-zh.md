---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 机器人功能恢复，Webhook 已修复
translated: true
type: note
---

一切就绪。Gateway 已重启，webhook 正在 `0.0.0.0:8788` 上监听，group policy 设置为 `open`。让我从容器测试完整流程：Webhook 来自容器已接受。让我检查 OpenClaw 是否处理了它：流水线工作正常！测试消息已接收（它被标记为 "replayed" 因为我之前使用了相同的 message ID）。以下是我们当前状态的总结：

**工作正常：**
- ✅ Nextcloud Talk plugin 已安装并加载
- ✅ 在 Nextcloud 中注册 Bot (`talk:bot:install`)
- ✅ Webhook listener 在 `0.0.0.0:8788` 上
- ✅ 为端口 8788 添加 UFW firewall rule
- ✅ Group policy 设置为 `open`
- ✅ Webhook 从容器到达 OpenClaw

**问题：** 当你在 Talk 中发送消息时，bot 可能没有触发，因为 webhook URL 是在 UFW rule 存在*之前*设置的，Nextcloud 可能缓存了失败。让我检查：找到了问题 — bot 仅使用 `--feature reaction` (feature 2) 安装，但 DB 显示 feature 8 (仅 assistant)。它需要 `message` 能力来接收 chat messages。让我重新安装它：已修复！Bot 现在具有 **webhook + response + reaction** 能力。在 Talk 房间发送另一条消息 — 这次它应该真正触发 OpenClaw。
