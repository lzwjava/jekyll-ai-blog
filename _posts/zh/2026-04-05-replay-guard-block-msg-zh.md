---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重播防护拦截重复消息
translated: true
type: note
---

我找到了问题所在。情况如下：

**问题分析：**

1. **你的 `requireMention: false` 配置是正确的** —— 它位于 `rooms.eu42ecdy.requireMention`，位置无误。

2. **真正的问题：Replay Guard 去重机制**
   - 去重文件显示：`{"eu42ecdy:1": 1775323541972}`
   - 这意味着来自房间 `eu42ecdy` 且 `messageId=1` 的消息在 24 小时内（TTL = 86400000毫秒）会被视为重复并拦截
   - 第一条之后所有 `messageId=1` 的消息**甚至在**提及检查运行之前就被拒绝了

3. **流程：** `shouldProcessMessage（重放检查）` → 若通过 → `handleNextcloudTalkInbound` → 提及门控检查

重放保护最先运行，因此即便 `requireMention: false` 设置正确，具有重复消息ID的消息也会在到达提及逻辑之前被拦截。

**可能原因：** Nextcloud Talk 为所有消息发送了相同的 `messageId`（或者你在重复发送相同的测试 webhook）。

**修复方案：**

1. **快速修复 —— 清空重放去重文件：**
   ```bash
   rm /home/lzw/.openclaw/nextcloud-talk/replay-dedupe/*.json
   echo '{}' > /home/lzw/.openclaw/nextcloud-talk/replay-dedupe/*.json
   ```
   然后发送一条具有唯一ID的新消息。

2. **或者重启网关**，以重新加载配置。

3. **检查 Nextcloud Talk** —— 确保它为每条消息生成唯一的消息ID，而不是重复使用 `1`。

需要我清空去重文件并验证配置吗？