---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CI4迁移总结与修复方案
translated: true
type: note
---

## CI4 迁移 — 今晚完成的内容

### ✅ Composer 与依赖项

- `composer install --no-dev` — 所有 SDK 现已安装（`qiniu/php-sdk`、`predis/predis`、`pingpp-php`、`phpspreadsheet`、`php-amqplib`、`pili-engineering-sdk`）
- `php-ffmpeg` 已排除（需要 `ext-gd` 但不可用；误删后已恢复 `CI4 framework`）

### ✅ 支付桩模块（关键）

- `app/Libraries/WxPay.php` — JSAPI/应用/二维码支付桩模块，退款/转账/红包桩模块
- `app/Libraries/WxPayCallback.php` — 微信支付回调处理器（桩模块，可安全接收真实通知）
- `app/Libraries/Alipay.php` — 支付宝支付桩模块

### ✅ CI3 兼容层

- `app/Config/CI3Compat.php` — 提供 `get_instance()`、`CI3_Loader_Proxy` 和 `CI3_Loader`，用于 CI3 时期的库代码（Pay、WeChatAppClient 等）
- `app/Config/NamespaceBridge.php` — 映射 `App\Libraries\*` → `App\Models\*`，用于 DAO 跨命名空间访问

### ✅ 已修复的损坏文件

- **Constants.php** — 修复了 8 处以上损坏的 `define()` 调用（被截断的 heredoc，重复的环境常量及错误的 if-else 判断）
- **Wechat.php** — 重复的 `callback()` 方法拆分为 `callback`（GET）和 `callbackPost`（POST）
- **Accounts.php** — 移除多余的 `public public` PHP 8 语法错误
- **Lives.php** — 添加 `use` 语句导入 `WeChatAppClient`、`QiniuLive`
- **JobHelperDao.php** — 添加 `use App\Controllers\WeChatAppClient`
- **Pay.php / PayNotifyDao.php** — 模型类使用完全限定名称引用
- **WeChatAppClient.php** — 重定向至 `namespace App\Controllers` 并添加全局别名
- **wxencrypt/** — 命名空间包装器，mcrypt→OpenSSL 替换

### ✅ CI4 数据库 API 迁移

- 在所有模型文件中批量替换 `->result()` → `->getResult()`、`->row()` → `->getRow()`

### ✅ PSR-4 与类映射修复

- `App\Libraries` 添加为 PSR-4 命名空间
- 所有模型文件添加 `class_alias` 以支持跨命名空间解析

### ✅ 旧代码归档

- `application/` → `application_ci3/`（所有 CI3 代码已安全归档）

### ✅ 已推送至 GitHub

---

### 当前路由状态

| 路由 | 状态 | 说明 |
|-------|--------|------|
| `/` | ✅ 200 | |
| `/users/isRegister` | ✅ 200 | |
| `/lives/count` | ✅ 200 | |
| `/lives/recommend` | ✅ 200 | |
| `/wechat/sign` | ✅ 200 | |
| `/topics` | ✅ 200 | |
| `/applications/me` | ✅ 200 | |
| `/accounts/me` | ✅ 200 | |
| `/wechat/menu` | ⚠️ 500 | 容器中 Redis 未运行 |
| `/jobs/alive` | ⚠️ 500 | 容器中 Redis 未运行 |

### 剩余任务（本次未完成）

- **Redis** — 需要启动（`live-server-redis-1`）以支持 `/wechat/menu` 和 `/jobs/alive`
- **会话/认证流程** — 真实的登录往返测试
- **数据库迁移** — CI4 迁移与现有 CI3 表结构对比
- **`POST /charges`、`POST /rewards`** — 路由已存在，但支付逻辑目前使用桩模块
