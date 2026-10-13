---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GD重建与调试配置修复
translated: true
type: note
---

两者均已完成并验证。以下是摘要。

## ✅ #2 — 使用 GD 重新构建镜像

- 使用修正后的 `Dockerfile` 重新构建了 `app` 镜像（GD 现在实际上是已安装的，而不仅仅是配置了）。
- 已验证：`gd`、`imagecreate()`、`imagecreatetruecolor()` 均已存在。
- 结果：`/lives/:id/card`（邀请卡）现在可以越过 GD 检查，进入正常的 auth 处理，而不再被降级。

## ✅ #3 — 生产环境调试配置已修复

- **`app/Config/Boot/production.php`** → 现在生产环境安全：`CI_DEBUG=false`、`display_errors=0`、`log_errors=1`、`E_DEPRECATED` 已抑制。错误仍记录到 `writable/logs`，但堆栈跟踪/路径不再泄露给客户端。这就是真实部署所使用的配置。
- **在此过程中发现的根本原因：** docker-compose 设置了 `CI_ENV=production` — 但 **CI4 读取的是 `CI_ENVIRONMENT`**，因此该变量是一个静默空操作，应用始终默认处于生产模式。已修正该名称。
- 为了避免在开发时失去错误可见性，我将**本地**栈指向了 `CI_ENVIRONMENT=development`（docker-compose）。你在本地保留完整的调试跟踪；生产环境保持锁定。
- **发现并处理的副作用：** 开发模式重新启用了 `E_ALL`，这使得 Qiniu SDK 的 PHP 8.5 弃用（`Config.php:44`）会在 JSON 内容前添加前缀——它破坏了 `/wechat/wxpayNotify`，这是一个**支付回调**。已在 `development.php` 中添加 `& ~E_DEPRECATED`（与生产环境匹配）。真实错误/警告仍然显示。

## 重建后已验证

- **96/96 个 GET 路由**返回 HTTP 200
- **95/96 返回干净有效的 JSON**（唯一例外是 `/wechat/wxpayNotify`，它*故意*返回纯文本 `success` — 这不是污染）
- 栈健康：app/database/redis/web 全部正常

## 关于你即将进行的支付工作，有一件事需要了解

在开发模式下，CI4 的 **DebugBar 会向响应追加 `<script>` HTML**。对于 JSON 路由来说这只是外观问题，但像 `wxpayNotify` 这样的纯文本支付回调，它会在 `success` 之后追加 HTML。这不会影响真实生产环境（那里 `CI_DEBUG=false`），但如果你**将真实的微信/支付宝回调隧道到本地进行测试**，尾部 HTML 可能会破坏回调验证。当你进行支付移植时值得记住 — 通过针对生产模式实例测试回调即可轻松绕过。

## 尚未提交

三个文件已更改（在 Docker 挂载的活动工作区副本中）：

- `app/Config/Boot/production.php`
- `app/Config/Boot/development.php`
- `docker-compose.yml`

需要我将**这些同步到正式仓库并提交**（并推送）吗？然后你就可以继续处理 **#1，支付 SDK 移植**，这是个大任务。
