---
audio: false
date: 2025-09-14
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 禁用LibreChat身份验证变通方案
translated: true
type: note
---

简短回答：你无法完全关闭 LibreChat 的身份验证功能，但可以解决"频繁要求登录"的问题，实现接近"免登录"的使用体验。以下是实际有效的解决方案（及原理说明）：

### 1) 无法完全禁用身份验证

维护者已确认：可以禁用注册功能，但身份验证系统本身无法关闭。（[GitHub][1]）

### 2) 频繁退出登录的原因

如果在 **HTTP** 协议下访问实例（例如通过局域网 IP），生产环境中的 cookie 会被标记为 `secure` 导致浏览器无法保存，系统会强制跳转回登录页面。解决方案是使用 **HTTPS**（即使是自签名证书）或在开发模式下运行 API 以禁用安全 cookie。（[GitHub][1]）

### 3) 两种可靠解决方案

#### 方案 A — 规范/安全方案（推荐）

* 为 LibreChat 配置 HTTPS 反向代理（nginx/caddy/traefik；局域网内自签名证书即可）
* 在 `.env` 文件中延长会话有效期：

  ```
  SESSION_EXPIRY=1000 * 60 * 60 * 24       # 24小时
  REFRESH_TOKEN_EXPIRY=(1000 * 60 * 60 * 24) * 30  # 30天
  ```

* 修改环境变量后重启容器
  这样可保持登录状态数天/数周，同时修复 cookie 丢失问题。（[GitHub][2]）

#### 方案 B — "我在私有网络环境，只想解决频繁退出问题"

* 创建 `docker-compose.override.yml` 在开发模式下运行 API（禁用安全 cookie）：

  ```yaml
  services:
    api:
      command: npm run backend:dev
  ```

* 执行 `docker compose up -d` 应用更改
  此方案安全性较低（cookie 不启用 `secure` 标志），但能解决普通 HTTP 协议下的强制重新登录问题。（[librechat.ai][3]）

### 4) 可选体验优化设置

* **禁用新用户注册** 实现准单用户模式：

  ```
  ALLOW_REGISTRATION=false
  ```

  （如需添加用户仍可通过 `npm run create-user` 实现）（[librechat.ai][4]）
* 在 `.env` 中保留其他认证开关（邮件/社交登录标志）以简化登录流程。（[librechat.ai][5]）

### 5) 快速配置清单（v0.8.0-rc3 版本）

1. 选择方案：HTTPS 代理（最佳）**或** 开发模式（快速局域网方案）
2. 在 `.env` 中设置更长的 `SESSION_EXPIRY` 和 `REFRESH_TOKEN_EXPIRY`
3. 重启服务栈使环境变量生效
4. （可选）关闭注册功能实现"单用户"体验

如果需要，可提供你当前的 `docker-compose.yml` 和 `.env` 文件内容（剔除敏感信息），我会标注出需要修改的具体位置。

[1]: https://github.com/danny-avila/LibreChat/discussions/572
[2]: https://github.com/danny-avila/LibreChat/discussions/2571?utm_source=chatgpt.com
[3]: https://www.librechat.ai/blog/2024-05-16_unsecured_http
[4]: https://www.librechat.ai/docs/configuration/authentication
[5]: https://www.librechat.ai/docs/configuration/dotenv
