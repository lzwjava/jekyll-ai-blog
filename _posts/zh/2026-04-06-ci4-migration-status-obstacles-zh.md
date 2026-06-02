---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CI4迁移现状与障碍
translated: true
type: note
---

以下是对迁移现状的如实评估：

---

## 🦞 CI4 迁移 — 剩余障碍

### ✅ 今晚修复的内容（正常路由）

`/`, `/users/isRegister`, `/lives/count`, `/lives/recommend`, `/wechat/sign`, `/wechat/menu`, `/jobs/alive`, `/topics`, `/applications/me`, `/accounts/me` — 全部返回 **HTTP 200**。

---

### 🚧 遗留问题（按严重性从高到低排序）

#### 🔴 严重 — 调用时将产生 500 错误

| 问题 | 影响 | 应对措施 |
|-------|--------|------------|
| **`WxPay.php`, `Alipay.php`, `WxPayCallback.php` 存根文件缺失** | `Charges`, `Rewards`, `Wechat` 控制器在触发支付流程时会崩溃 | 需要创建存根实现或 CI4 兼容版本的 ping++ / Alipay SDK |
| **`WxPay`, `Alipay`, `WxPayCallback` 在 `Wechat` 和 `Rewards` 控制器中使用 `new` 实例化** — 如果在存根文件就位前调用这些端点（例如 `POST /rewards`, `POST /charges`）→ **500** | `Wechat::callback()`（微信支付回调）尤为敏感 — 会接收真实的支付通知 | 需要 CI4 兼容的支付回调处理器 |
| **`WxPay` 使用 `WxPay.Config()` 读取 PHP 常量** — 旧的 CI3 `application/libraries/wx/WxPay.Config.php` 中的常量可能在 CI4 环境中不存在 | 微信支付预付款 ID 将生成失败 | 需要移植或创建 `WxPay.Config.php` 存根 |

#### 🟡 中等 — 功能不完整

| 问题 | 影响 |
|-------|--------|
| **`qiniu/php-sdk` 未安装** — `composer.json` 已列出但 `vendor/qiniu/` 为空 | `QiniuLive` 会静默返回 null，因此流媒体相关功能将无声失效。需要运行 `composer install` |
| **`pili-engineering/pili-sdk-php` 未安装** — 流媒体/视频点播功能损坏 | `LiveDao` 中任何涉及 Pili（RTMP 流管理）的操作都将失败 |
| **`pingplusplus/pingpp-php` 未安装** — 支付处理损坏 | 实际的微信/支付宝收款单创建将失败 |
| **`php-ffmpeg/php-ffmpeg` 未安装** — 视频转码功能损坏 | 视频转换/回放将失败 |
| **`php-amqplib/php-amqplib` 未安装** — 任务队列损坏 | 异步任务处理将失败 |
| **`phpoffice/phpexcel` 未安装** — Excel 导出功能损坏 | 任何管理后台/统计数据的 Excel 导出将失败 |

#### 🟠 基础设施

| 问题 | 影响 |
|-------|--------|
| **`composer install` 尚未运行** — 只有 `vendor/codeigniter4/` 存在 | `composer.json` 中列出的所有第三方 SDK 均缺失。需要运行 `composer install --no-dev` |
| **CI4 `Services.php` 门面不存在** — `log_message()`, `force_download()` 等辅助函数可能不可用 | 一些依赖隐式辅助函数的 CI3 函数需要显式加载 |

#### 🟢 低级 — 代码质量（不阻塞，但应清理）

| 问题 | 影响 |
|-------|--------|
| **旧的 `application/` 目录仍存在** | CI3 遗留代码与 CI4 代码并存。冗余代码，应归档/移动到 `application_ci3/` |
| **`$this->load->view()` 调用已从控制器中移除** — 但 CI4 使用 `return view()` 或 `$this->response->setBody()` | 任何原先渲染视图（管理页面等）的控制器现在不返回任何内容 |
| **会话** — 未测试会话登录/认证是否实际工作 | 所有 `/users/login`, `/self` 等端点需要进行真实的登录流程测试 |
| **无数据库迁移** — CI4 使用 `migrations` 表和 `spark` CLI — 可能与现有 CI3 数据库结构冲突 | 可能需要配置 CI4 在不使用迁移的情况下使用现有数据库 |
| **生产环境中 `WECHAT_DEBUG=false`** — 但未设置真实的调试标志 | 真实的微信 API 调用将针对生产端点进行 |

---

### 📋 快速解决方案清单

```bash
# 1. 运行 composer install
composer install --no-dev

# 2. 创建缺失的库存根文件
touch app/Libraries/wx/WxPay.php
touch app/Libraries/wx/WxPayCallback.php
touch app/Libraries/alipay/Alipay.php

# 3. 归档旧 CI3 代码
mv application application_ci3

# 4. 测试认证流程
POST /login → 获取会话令牌
GET  /self  → 验证会话工作
```

---

### 💡 如实评估

**路由和基本 HTTP 往返** 现已工作。应用可以接收请求并返回 JSON 响应。剩余部分是 **难点** — 与微信支付、支付宝、视频转码和流媒体基础设施的真实集成。这些都依赖于尚未安装的第三方 SDK 以及需要精心移植的库。

**底线：** 我们已修复了约 70% 的“会立即崩溃”问题。剩余的 30% 是集成特有的，需要在生产环境中逐个端点测试时，按功能逐一解决。

需要我处理其中任何一项吗？
