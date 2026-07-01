---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 项目状态与遗留问题
translated: true
type: note
---

好问题。目前状况如下：

**✅ 已修复/正常：**

- 数据库连接（数据库正确连接）
- JSSDK、WeChatPlatform、Pay、Sms、LeanCloud 的 CI4 库
- `localhost:8088/` → HTTP 200
- Git 规范：`.env` 已忽略，`.env.example` 已提交

---

**🚧 待解决问题（按影响程度由低到高）：**

| # | 问题 | 影响 | 预计耗时 |
| --- | ------- | -------- | -------- |
| 1 | **20 个控制器中存在 `$this->load->library/model`** | 不会立即崩溃（惰性调用），但在相关端点正常工作前需修复 | ~2 小时 |
| 2 | **`WxPay`、`Alipay`、`WxPayCallback` 存根文件缺失** | 若调用相关方法，`Wechat`、`Charges`、`Rewards` 控制器将报 500 错误 | ~1 小时 |
| 3 | **仅定义了 `/` 路由** | 无论代码质量如何，其他所有端点均返回 404 | ~30 分钟 |
| 4 | **仍存在对 `REST_Controller` 的引用** | API 风格控制器可能继承此类（`app/Controllers` 中未 grep 到，但建议核实） | ~30 分钟 |
| 5 | **BaseController 预初始化 `UserDao`** | 轻微性能问题——每个请求即使未使用也会访问数据库 | ~10 分钟 |

**当前首要阻塞问题是 #3**——没有路由定义时，即使所有代码都完美，`/wechat`、`/users`、`/lives` 等路径仍会返回 404。需要将旧版 CI3 `application/config/routes.php` 中的路由定义转换为 CI4 格式。

接下来需要我着手处理路由配置吗？
