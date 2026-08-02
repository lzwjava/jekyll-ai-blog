---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare 域名服务器传播详解
translated: true
type: note
---

**问题：** 在Cloudflare中，“Waiting for your registrar to propagate your new nameservers”是什么意思？

**回答：**

你正在**将DNS管理从Namecheap迁移到Cloudflare**的过程中。

你的域名：

```
lzwjava.com
```

仍然在**Namecheap**注册，但你已告诉Cloudflare：

> “我希望Cloudflare来管理我的DNS。”

Cloudflare给了你两个域名服务器：

```
barbara.ns.cloudflare.com
dion.ns.cloudflare.com
```

现在你需要告诉Namecheap：

> “使用Cloudflare的域名服务器，而不是Namecheap的DNS。”

目前Namecheap仍然使用：

```
dns1.registrar-servers.com
dns2.registrar-servers.com
```

所以Cloudflare正在等待公共DNS系统显示：

```
lzwjava.com NS barbara.ns.cloudflare.com
lzwjava.com NS dion.ns.cloudflare.com
```

---

## 你现在应该做什么

前往：

Namecheap → 域名列表 → lzwjava.com → 域名服务器

将：

```
dns1.registrar-servers.com
dns2.registrar-servers.com
```

改为：

```
barbara.ns.cloudflare.com
dion.ns.cloudflare.com
```

保存。

---

## 然后等待

通常情况：

* 快速：10分钟
* 正常：1–2小时
* 最坏情况：24–48小时

Cloudflare会自动检测到变更。

你可以通过以下命令检查：

```bash
dig NS lzwjava.com
```

变更前：

```
lzwjava.com. NS dns1.registrar-servers.com
lzwjava.com. NS dns2.registrar-servers.com
```

变更后：

```
lzwjava.com. NS barbara.ns.cloudflare.com
lzwjava.com. NS dion.ns.cloudflare.com
```

---

## 重要：切换前检查DNS记录

Cloudflare已经导入了你的DNS记录，但请确认：

Cloudflare控制面板：

```
lzwjava.com
  → DNS
```

你应该看到类似这样的内容：

```
A     lzwjava.com       xxx.xxx.xxx.xxx
CNAME www               lzwjava.com
```

如果你在GitHub Pages上托管Jekyll博客，通常应该是：

```
CNAME
www
lzwjava.github.io
```

以及根域名：

```
A
@
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

---

## SSL/TLS

Cloudflare生效后：

前往：

```
Cloudflare
 → SSL/TLS
```

对于GitHub Pages：

```
加密模式：
完全
```

通常Cloudflare会自动颁发以下证书：

```
https://lzwjava.com
https://www.lzwjava.com
```

---

## DNSSEC 警告

消息提示：

> 确保DNSSEC已关闭

因为如果Namecheap的DNSSEC已启用，更改域名服务器可能会导致DNS验证失败。

在Namecheap中：

```
域名
 → 高级DNS
 → DNSSEC
```

先禁用它。

之后你可以启用Cloudflare的DNSSEC。

---

完成后，你的流程将是：

```
浏览器
   |
   v
Cloudflare DNS
   |
   v
GitHub Pages / 服务器
```

优势：

* 免费SSL
* CDN
* DDoS防护
* 更快的DNS
* 更便捷的未来部署

对于你的Jekyll博客（`lzwjava.com` → GitHub Pages），这是标准配置。
