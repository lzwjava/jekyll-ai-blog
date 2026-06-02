---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 数据库迁移评审发现
translated: true
type: note
---

## 🦞 CI3→CI4 迁移评审

**总体情况：基础良好，但应用在数据库层面仍存在故障。**

### ✅ 已完成的工作
- **容器栈** 稳固 — PHP 8.5-FPM + nginx + MySQL 5.7 + Redis 全部运行正常，并通过 Docker 内部网络通信
- **BaseController** 迁移正确 — 采用 CI4 风格的 HTTP 请求方法、响应辅助函数和会话处理
- **BaseDao** 存在并包含 `SET NAMES utf8mb4` 初始化设置
- **WeChatClient** 是整洁的 CI4 兼容代码（无 `get_instance()` 依赖）
- **CI4 `public/index.php`** 正确配置，使用恰当的 `Boot::bootWeb()` 入口点
- **Constants/env** 已填充所有真实密钥（微信、七牛、RTMP、数据库凭证）

### 🚨 关键阻碍（应用返回 HTTP 500）

**1. 数据库连接完全中断（当前根本原因）**
```
mysqli_sql_exception: No such file or directory
```
`app/Config/Database.php` 中硬编码了 `hostname: 'localhost'` — 在容器内，MySQL 位于 `database` 主机，而非套接字文件。环境变量（`DB_HOST=database`，`DB_USER=root`，`DB_PASS=WeImg4096`）已注入 PHP，但 **`Database.php` 配置从未读取它们**。需要从 `$_ENV` 或 `env()` 中获取。

**2. 每个控制器仍在使用 CI3 风格的 `$this->load`**（约 20 个控制器中出现了 60 多次）：
```php
$this->load->library(JSSDK::class);
$this->load->model(UserDao::class);
$this->load->library(WeChatPlatform::class);
```
在 CI4 中，这些应改为构造函数注入或服务定位器解析。

**3. Libraries 目录几乎为空** — `WeChatClient.php` 存在，但：
   - `JSSDK.php` — **缺失**，仍为 CI3 版本
   - `WeChatPlatform.php` — **缺失**，仍为 CI3 版本
   - `Pay.php`、`Sms.php`、`wx/WxPay.php`、`wx/WxPayCallback.php` — 均缺少 CI4 版本

**4. 不存在 `REST_Controller`** — 检查 grep 输出未发现 `REST_Controller` 引用，这很好（可能已处理），但需要确认所有 API 控制器正常工作。

### 📋 剩余工作（优先级排序）

| 优先级 | 任务 | 预估耗时 |
|---------|------|--------|
| 🔴 P0 | 修复 `Database.php` 以读取环境变量（`hostname => env('DB_HOST', 'database')`） | 5 分钟 |
| 🔴 P0 | 修复 `BaseController` 构造函数 — 移除触发每次请求都连接数据库的 `new UserDao()` 实例化 | 10 分钟 |
| 🟡 P1 | 为 CI4 重写 `JSSDK.php`（使用 `Services::curlrequest()`，`Services::cache()`） | ~1 小时 |
| 🟡 P1 | 创建 CI4 版本的 `WeChatPlatform` 库 | ~1 小时 |
| 🟡 P1 | 修复所有 20 个控制器中的 `$this->load->model/library` → 改为恰当的依赖注入 | ~2 小时 |
| 🟢 P2 | 验证 Pay、Sms、WxPay 库 | ~1 小时 |
| 🟢 P2 | 端到端测试所有主要路由 | ~1 小时 |

### 💡 最快达到 HTTP 200 的路径

1. 修复 `Database.php` 的环境变量读取 → 可能触发其他错误（而非数据库连接失败）
2. 延迟 `BaseController` 中的 `UserDao` 实例化 → 改为惰性初始化或从构造函数中移除
3. 修复 `JSSDK.php` → 仅此一项可能解封大部分微信路由
4. 然后逐个控制器重构 `$this->load` 引用

希望我从最高优先级开始修复吗？
