---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 数据库连接与库文件修复
translated: true
type: note
---

**已修复！** 🦞 本次会话完成内容如下：

---

## 修复内容

### 🔴 P0 — 数据库连接
- **`app/Config/Database.php`** — 之前硬编码了 `hostname: 'localhost'`。环境变量（`DB_HOST=database`）已注入容器但未被 CI4 的 `$default` 配置读取。通过在构造函数中添加 `getenv()` 调用修复此问题。**结果：数据库现已正常连接。**

### 🔴 P0 — 缺失 `JSSDK` 库
- **`app/Libraries/JSSDK.php`** — 从零创建（适配 CI4，不使用 `get_instance()`，通过 `WxDao` 和 `WeChatClient` 实现正确依赖注入）
- **`app/Libraries/WeChatPlatform.php`** — 创建（包含所有通知/模板消息方法）
- **`app/Models/UserDao.php`** — 添加 `use App\Libraries\JSSDK;` 以修复 PHP 命名空间解析问题（在 `App\Models` 中，`new JSSDK()` 原先解析为 `App\Models\JSSDK` 而非全局的 `JSSDK`）

### 🟡 P1 — 缺失 `Pay`、`Sms`、`LeanCloud` 库
- **`app/Libraries/Pay.php`** — 创建（支持支付宝/微信支付处理）
- **`app/Libraries/Sms.php`** — 创建（LeanCloud 短信通知功能）
- **`app/Libraries/LeanCloud.php`** — 创建（兼容 CI4 的 HTTP 客户端）
- **`app/Config/Autoload.php`** — 为所有 CI3 风格类名添加类映射条目

### ✅ 结果：`curl localhost:8088/` → **HTTP 200**

---

## 待办事项（非阻塞性问题，但需处理）

| 项目 | 优先级 | 说明 |
|------|---------|-------|
| `WxPay`、`Alipay`、`WxPayCallback` 桩模块 | 🟡 P1 | 被 `Wechat`、`Charges`、`Rewards` 控制器调用 — 若访问相关端点将返回 500 错误 |
| 所有 20 个控制器中的 `$this->load->library()` / `$this->load->model()` 调用 | 🟡 P1 | 仍为 CI3 风格，需重构为依赖注入或 `Services::` 形式 |
| 路由配置 | 🟡 P1 | 当前仅定义 `/` 路由 — 需为所有其他 CI3 路由添加 CI4 `$routes->` 条目 |
| `REST_Controller` 移除 | 🟢 P2 | API 控制器可能仍继承此基类 — 需检查确认 |

是否需要我继续处理 P1 事项，还是暂时到此为止？