---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Supabase 迁移完成并已验证
translated: true
type: note
---

Supabase 迁移已完成，已提交、推送，两个 checkout 均验证一致。

## ✅ 我做了什么

**新的 Supabase 客户端** — `app/Libraries/Supabase.php`（直接使用 cURL，无新增 Composer 依赖）：
- `requestSmsCode()` / `verifySmsCode()` → Supabase Auth 手机 OTP（`/auth/v1/otp`、`/auth/v1/verify`）
- `createConversation()` → 通过 PostgREST 插入 `public.conversations`
- `sendTemplateSms()` → 可选的 Edge Function（`SUPABASE_SMS_FUNCTION`）
- `e164()` 将存储的裸号码规范化（`13888888888` → `+8613888888888`）
- 每个方法在未配置/不可达时都会**优雅降级**（记录日志并返回失败），因此 cron 短信任务可以继续运行

**调用点已重新接入**（全部 3 个 LeanCloud 功能）：
- `Users.php` → Supabase Auth OTP；保留调试 `5555` 和 `specialPhones()` 的绕过逻辑
- `LiveDao.php` → Supabase `createConversation()`
- `Sms.php` → 通过 Supabase 发送模板短信

**立即解除了直播创建的阻塞** — 当 Supabase 未配置时，`createConversation()` 会回退到本地生成的 ID，因此在等待凭据期间仍可创建直播。已验证：直播创建会返回 `conversationId` + `hlsUrl`。

**移除了无用的 LeanCloud 代码** — 删除了 `LeanCloud.php`、其 Autoload/CI3Compat 条目，以及未使用的 `LC_APP_ID` 常量和环境变量。

**修复了一个因解除直播创建阻塞而暴露的潜在 bug**：`random_element()` 来自 CI3 的 `array_helper`（在 CI4 中未自动加载）→ 一旦会话创建步骤成功就会引发致命错误。已将其移植到 `base_helper.php`。

**配置** — 在 `.env`/`.env.example`/`docker-compose.yml` 中新增 `SUPABASE_*` 变量，并新增 `supabase/schema.sql`（包含 conversations + messages 表、RLS 和 Realtime 发布），供在 Supabase SQL 编辑器中运行。

## ✅ 端到端已验证

- 注册/登录/self 均正常；直播创建成功；**96/96 个 GET 路由**通过
- 支付渠道不受影响；未配置 Supabase 的路径会记录优雅跳过日志
- 两个 checkout 在 `ab46f8f` 处完全一致，工作区干净，已推送

## 🔑 激活步骤（需要你提供信息）

1. **创建一个 Supabase 项目**，然后填写 `SUPABASE_URL`、`SUPABASE_ANON_KEY`、`SUPABASE_SERVICE_ROLE_KEY`
2. **在 SQL 编辑器中运行 `supabase/schema.sql`**
3. **在 Supabase Auth → Phone 中接入短信服务商**（Twilio/Aliyun），用于实际 OTP 发送
4. 可选：部署一个 SMS Edge Function，并设置 `SUPABASE_SMS_FUNCTION` 用于 cron 模板通知

## ⚠️ 剩余事项（跨仓库，前端）

`live-web` 和 `live-mobile-web` 仍在使用 `leancloud-realtime`，并且为直播聊天硬编码了 app ID。后端现在会存储 Supabase conversation ID，但**客户端聊天需要迁移到 Supabase Realtime**，并单独使用 `messages` 表。需要我接下来处理这部分吗？