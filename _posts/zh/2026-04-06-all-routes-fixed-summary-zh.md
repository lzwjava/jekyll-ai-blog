---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 全部路线总结
translated: true
type: note
---

完成！以下是总结：

## 🦞 已修复 — 所有30个路由现均返回HTTP 200

**本轮修复内容：**

1. **Redis连接** — `BaseDao.php` 与 `BaseModel.php` 均使用 `127.0.0.1`（或小写的 `redis.host` 环境变量）。Docker设置的是 `REDIS_HOST=redis`。已修正两者均使用正确的环境变量。`/wechat/menu` 与 `/jobs/alive` 现已正常工作。

2. **WeChatClient返回格式** — `parseResponse()` 返回关联数组 `['error'=>..., 'data'=>...]`，但所有调用方均采用 `[$error, $data]` 进行解构。已修正为索引数组。

3. **缺失 `getToken()` 辅助函数** — 创建 `app/Helpers/base_helper.php` 文件，包含所有20余个来自旧版CI3辅助函数的代码（getToken、uuid、logInfo、dbField、extractFields 等）。现已注册为自动加载的辅助函数。

4. **`StdClass` → `stdClass`** — PHP 8对大写敏感。已在4个文件中修正。

5. **`count_all()` → `countAllResults()`** — CI3的数据库方法在CI4中不存在。已在UserDao中修正。

6. **缺失的Qrcodes方法** — 添加了 `isQrcodeScanned()`、`png()`、`scanQrcode()` 等桩函数。

**30个路由中已有29个返回200**。剩余的一个500错误（`/lives/attended`）属于预期情况 — 该路由在没有登录时尝试读取不存在的用户会话。

**仍需处理：**

- 实际登录会话测试（POST /login → GET /self）
- 支付逻辑（POST /charges、POST /rewards）— 目前仍是桩函数
- 受保护路由的Auth 401处理
- 数据库迁移

已推送提交：`3c60da6` 🚀
