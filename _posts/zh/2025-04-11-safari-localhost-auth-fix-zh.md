---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Safari本地主机身份验证修复
translated: true
type: note
---

此问题的出现是因为 macOS 上的 Safari 对本地 URL 执行比 Chrome 更严格的安全策略。具体而言，Safari 要求安全的 HTTPS 环境才能允许持久性 Cookie 和认证会话，这防止了在 HTTP 上运行的应用（如 LibreChat）出现潜在登出循环或每次访问都需要重新认证的情况。Chrome 对本地 HTTP 更为宽松，因此认证能在 Chrome 中持久保持，但在 Safari 中则不行。[1][2][3]

### 影响因素
- **浏览器策略**：Safari 等现代浏览器要求对本地使用 HTTPS，以避免混合内容警告和会话不安全问题。
- **LibreChat 行为**：LibreChat 使用安全 Cookie 或基于 localStorage 的令牌进行认证，在 Safari 的 HTTP 环境下会因其对非安全源的严格处理而失效。

### 解决方案（按简易和有效性排序）
1. **为本地设置 HTTPS（推荐）**：
   - LibreChat 官方文档和博客推荐此方法以防止 HTTP 引起的登出问题。[1]
   - 使用 `mkcert`（免费工具）生成并信任本地的 SSL 证书：
     - 通过 `brew install mkcert` 安装或从 GitHub 下载。
     - 运行 `mkcert -install` 安装根证书。
     - 创建证书：`mkcert localhost 127.0.0.1`。
     - 配置 LibreChat（如通过 Docker 环境变量或配置）使用这些证书：在 `.env` 文件或环境中添加 `HTTPS=true`、`SSL_CRT_FILE=/path/to/localhost.pem` 和 `SSL_KEY_FILE=/path/to/localhost-key.pem`。
     - 重启 LibreChat 并通过 `https://localhost:3080` 访问。
     - Safari 现在会将其视为安全来源，允许无缝登录。

2. **替代方案：使用 127.0.0.1 代替本地**：
   - Safari 有时对 `localhost` 的行为不同（由于 IPv6 或 DNS 解析）。尝试访问 `http://127.0.0.1:3080` —— 这在某些情况下解决了类似的连接问题，但可能无法完全修复认证持久性。[4][4][5]

3. **清除 Safari 中本地的网站数据**：
   - 前往 Safari > 偏好设置 > 隐私 > 管理网站数据 > 搜索 "localhost" > 移除所有相关条目。
   - 这会强制 Safari 停止强制执行 HTTPS 升级或缓存的不安全上下文。[3][2]
   - 重启 Safari 并测试；如果 LibreChat 支持，认证应能保持。

如果以上方法均无效，请检查 LibreChat 日志中的认证错误，确保 `.env` 中没有冲突标志（例如 `ALLOW_ANONYMOUS=true` 会完全禁用认证，如需要），并确认未处于 Safari 的私密浏览模式，该模式会阻止持久存储。[6][7] 如果问题仍然存在，请提供您的 LibreChat 版本和 .env 配置以便进一步排查。

引用：
[1] https://www.librechat.ai/blog/2024-05-16_unsecured_http
[2] https://github.com/danny-avila/LibreChat/discussions/529
[3] https://stackoverflow.com/questions/46394682/safari-keeps-forcing-https-on-localhost
[4] https://superuser.com/questions/30827/safari-is-unable-to-reach-localhost-127-0-0-1
[5] https://apple.stackexchange.com/questions/422556/localhost-has-stopped-working-on-chrome-and-safari-since-upgrading-to-big-sur
[6] https://www.librechat.ai/docs/configuration/authentication
[7] https://discussions.apple.com/thread/255906354
