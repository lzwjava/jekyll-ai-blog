---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare SSL/TLS 边缘证书概述
translated: true
type: note
---

## 问题：Cloudflare SSL/TLS 边缘证书简介

## 回答：

Cloudflare SSL/TLS 的思路很简单：

```
访客浏览器
      |
      | HTTPS（加密）
      |
Cloudflare 边缘服务器
      |
      | HTTP 或 HTTPS
      |
你的源服务器
```

Cloudflare 作为**反向代理**位于中间。访客看到的证书通常是 **Cloudflare 的边缘证书**，而不是你的服务器证书。

---

## 1. 什么是 SSL/TLS？

SSL 是旧名称。如今我们主要使用 **TLS（传输层安全协议）**。

TLS 提供以下功能：

### 1. 加密

用户和 Cloudflare 之间的任何第三方都无法读取：

```
GET /login
Cookie: session=xxxx
password=123
```

它会变成加密字节：

```
9a 7f 3c a8 ...
```

---

### 2. 身份验证

浏览器会验证：

```
lzwjava.com
        |
        证书
        |
        Cloudflare
        |
        受信任的 CA
```

示例：

```
证书：
  主体：
      lzwjava.com

  颁发者：
      Google Trust Services CA

  有效期：
      2026-08-01 -> 2026-11-01
```

浏览器会询问：

“我可以信任这个证书吗？”

答案来自 CA 证书链。

---

### 3. 完整性

TLS 可防止篡改。

没有 TLS：

```
用户
 |
 | 你好
 |
攻击者修改为：
“下载应用”
        |
        v
“下载恶意软件”
```

TLS 可以检测到这种篡改。

---

# 2. 什么是边缘证书？

“边缘”指的是 Cloudflare 的边缘网络。

示例：

居住在加利福尼亚州的用户：

```
浏览器
   |
   |
Cloudflare 洛杉矶边缘节点
   |
   |
你的服务器
```

安装在 Cloudflare 边缘节点上的证书：

```
*.lzwjava.com
lzwjava.com
```

被称为：

```
边缘证书
```

你的浏览器看到：

```
https://lzwjava.com
```

证书：

```
颁发给：
lzwjava.com

颁发者：
Cloudflare
```

而非你的 VPS。

---

# 3. 你当前的证书

你拥有：

```
*.lzwjava.com, lzwjava.com

高级
到期时间：
2026-11-01

通用
到期时间：
2026-11-01

备份
到期时间：
2026-11-01
```

这很好。

这意味着：

```
lzwjava.com
```

可以工作：

```
https://lzwjava.com
```

以及通配符子域名：

```
https://blog.lzwjava.com
https://api.lzwjava.com
https://test.lzwjava.com
```

因为：

```
*.lzwjava.com
```

覆盖了子域名。

---

# 4. Universal SSL 与 Advanced Certificate Manager

## Universal SSL（免费）

Cloudflare 会自动提供：

```
lzwjava.com
*.lzwjava.com
```

你无需进行任何管理。

适用于：

* 个人网站
* 博客
* 小型应用

你当前的设置已经足够。

---

## Advanced Certificate Manager（付费）

获得更多控制权。

示例：

你有：

```
dev.api.internal.lzwjava.com
```

普通的通配符证书：

```
*.lzwjava.com
```

**不**覆盖：

```
dev.api.internal.lzwjava.com
```

因为它只覆盖一层子域名：

```
xxx.lzwjava.com
```

ACM 可以创建：

```
*.api.internal.lzwjava.com
```

---

# 5. TLS 版本

你的设置：

```
最低 TLS 版本
TLS 1.0（默认）
```

我建议修改此设置。

现代设置：

```
TLS 1.2
```

或：

```
TLS 1.3
```

原因：

TLS 1.0/1.1 已过时。

现代浏览器支持：

```
TLS 1.2（2010 年）
TLS 1.3（2018 年）
```

大多数网站使用：

```
最低 TLS：1.2
TLS 1.3：开启
```

---

# 6. Always Use HTTPS

你已启用：

```
Always Use HTTPS
```

这意味着：

用户访问：

```
http://lzwjava.com
```

Cloudflare 返回：

```
301 重定向

https://lzwjava.com
```

很好。

---

# 7. HSTS

HTTP 严格传输安全：

没有 HSTS：

```
首次访问：

http://lzwjava.com

重定向

https://lzwjava.com
```

启用 HSTS：

浏览器会记住：

```
lzwjava.com 始终使用 HTTPS
```

因此：

```
http://lzwjava.com
```

会被自动升级。

建议：

```
启用 HSTS
```

但需要注意：

如果你启用：

```
includeSubDomains
```

那么：

```
api.lzwjava.com
dev.lzwjava.com
```

也必须支持 HTTPS。

---

# 8. TLS 1.3

启用：

```
TLS 1.3：开启
```

好处：

TLS 握手：

TLS 1.2：

```
客户端
 |
 | 打招呼
 |
服务器
 |
 | 证书
 |
客户端
 |
 | 密钥交换
 |
已加密
```

TLS 1.3：

```
客户端打招呼
+
密钥交换

已加密
```

连接更快。

---

# 9. Automatic HTTPS Rewrites

问题：

你的 HTML：

```html
<img src="http://example.com/a.png">
```

浏览器：

```
混合内容警告
```

Cloudflare 重写为：

```html
<img src="https://example.com/a.png">
```

对迁移的网站很有用。

---

# 针对 lzwjava.com 的建议设置

对于个人 AI 博客 / 作品集网站：

```
SSL/TLS 模式：
    Full（strict）

Always Use HTTPS：
    开启

最低 TLS 版本：
    TLS 1.2

TLS 1.3：
    开启

Automatic HTTPS Rewrites：
    开启

HSTS：
    确认一切正常后再启用

Universal SSL：
    保持开启
```

架构：

```
浏览器
   |
   | HTTPS
   |
Cloudflare 边缘节点
   |
   | HTTPS（Full Strict）
   |
你的服务器 / GitHub Pages
```

这是 2026 年常见的生产环境配置。你当前的 Cloudflare 证书状态看起来已经健康。