---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Cloudflare上启用HTTPS
translated: true
type: note
---

问题：将 DNS 迁移到 Cloudflare 后，如何为 `lzwjava.com` 启用 HTTPS？

回答：

由于你的域名已在 Cloudflare 上生效，HTTPS 基本是自动的。请执行以下步骤：

## 1. 启用 Cloudflare SSL/TLS

前往：

```
Cloudflare 控制面板
 → lzwjava.com
 → SSL/TLS
```

设置：

```
加密模式：完全
```

（如果你的源站有有效证书，可选择 **完全（严格）**）

对于 GitHub Pages，**完全** 通常就足够了。

---

## 2. 等待 Cloudflare 证书颁发

前往：

```
SSL/TLS
 → 边缘证书
```

你应该看到：

```
通用 SSL：已激活
```

Cloudflare 会自动创建证书：

```
lzwjava.com
www.lzwjava.com
```

通常需要：

```
5 分钟 - 24 小时
```

---

## 3. 启用 HTTPS 重定向

在：

```
SSL/TLS
 → 边缘证书
```

中启用：

```
始终使用 HTTPS：开启
```

然后：

```
自动 HTTPS 重写：开启
```

现在：

```
http://lzwjava.com
```

会重定向到：

```
https://lzwjava.com
```

---

## 4. 检查 DNS 代理状态

前往：

```
DNS → 记录
```

对于你的网站记录，云图标应为：

```
橙色云 ☁️ 已代理
```

示例：

```
类型   名称      目标                  代理
CNAME  www        lzwjava.github.io    ☁️
A      @          185.199.xxx.xxx      ☁️
```

如果是：

```
灰色云 ☁️ 仅 DNS
```

则 Cloudflare HTTPS 功能不会生效。

---

## 5. 测试

运行：

```bash
curl -I https://lzwjava.com
```

预期结果：

```
HTTP/2 200
server: cloudflare
```

检查证书：

```bash
openssl s_client -connect lzwjava.com:443 -servername lzwjava.com
```

你应该看到：

```
issuer=Cloudflare Inc ECC CA-3
```

---

针对你的情况（Jekyll 博客 + GitHub Pages），最终架构应为：

```
用户
 |
 HTTPS
 |
Cloudflare 边缘节点
 |
 HTTPS
 |
GitHub Pages
 |
 Jekyll 静态站点
```

无需购买 SSL 证书。Cloudflare 通用 SSL 是免费的。
