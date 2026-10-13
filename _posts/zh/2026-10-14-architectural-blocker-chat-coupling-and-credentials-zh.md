---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 架构阻塞：聊天耦合与凭据
translated: true
type: note
---

我已经完成了调查，在写代码之前需要提出一个**关键的架构发现**——因为它会大幅改变范围，而且存在一个硬性阻塞。

## LeanCloud在这里实际做的事情（3个功能）

| 功能 | Backend位置 | 是否可以backend-only替换？ |
| --- | --- | --- |
| **SMS验证码**（`requestSmsCode`/`verifySmsCode`） | `Users.php` | ✅ 可以——Supabase Auth phone OTP |
| **IM conversations**（`createConversation`） | `LiveDao.php` → 在live上存储`conversationId` | ⚠️ **不可以——见下文** |
| **Template SMS notifications**（`sendTemplateSms`：LiveStart/VideoReady/Invite） | `Sms.php`（cron） | ⚠️ 有差距——Supabase没有对应功能 |

## 🚨 阻塞点：chat在client-side与另外2个repo耦合

backend的`createConversation`返回一个**LeanCloud conversation ID**，两个frontend都直接通过`leancloud-realtime` npm SDK使用它：

```
live-web/src/views/LiveView.vue:108    import { Realtime, ... } from 'leancloud-realtime'
live-mobile-web/src/views/LiveView.vue:75   import { Realtime, ... } from 'leancloud-realtime'
   appId: 's83aTX5nigX1KYu9fjaBTxIa-gzGzoHsz'   ← hardcoded LeanCloud app
   client.getConversation(live.conversationId)   ← connects to LeanCloud's servers
```

因此，frontend在chat上**完全绕过了backend**，直接与LeanCloud的realtime基础设施通信。如果我只把backend的`createConversation`改为返回一个Supabase ID，chat会以**新的方式损坏**——frontend会拿到`leancloud-realtime`无法使用的ID。完整的chat迁移意味着需要在**两个Vue应用**中重写chat，使用`supabase-js` Realtime + `messages`表（Supabase没有像LeanCloud conversations那样内建的消息历史）。

另外：**template SMS在Supabase中没有对应功能**——需要通过Edge Function接入Twilio/其他provider。

## 🚫 硬性阻塞：没有Supabase凭据

在repo或env中，任何位置都不存在project ref、anon key或service role key。没有这些，我既无法接入，也无法进行端到端验证。

## 我的建议

分两个阶段迁移，先backend，这样每个部分都可验证：

1. **SMS验证** → Supabase Auth phone OTP（明确，仅backend，一旦已归档应用中的SMS验证码下线，即可解除登录阻塞）
2. **Conversation存储** → Supabase `conversations`表，并把**frontend chat重写**标记为`live-web` + `live-mobile-web`中必要的后续工作

但在开始构建之前，有两个问题确实会改变我要写的内容：

1. **chat的范围** —（a）现在先只做backend（在frontend迁移完成前chat保持不可用），还是（b）完整迁移，包括重写两个Vue应用中的chat？
2. **凭据** — 你能给我Supabase的**project URL + anon key + service role key**吗？（另外，SMS是走Supabase的phone provider，还是你会接Twilio？）

如果你直接说**“backend-only，先做SMS，这是凭据”**，我会立即开始，并把chat frontend重写留作记录清晰的后续工作。你想选哪种方式？
