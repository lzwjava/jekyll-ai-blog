---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快速修复 Nginx Mozilla 仓库错误
translated: true
type: note
---

问题：如何修复 `nginx/binary-i386/Packages` 架构警告和 Mozilla apt 仓库 `400 Bad Request` 错误，以及如何移除这些仓库？

回答：

您有**两个独立的问题**需要修复：

---

## 问题 1：Nginx i386 架构警告 (N: warning)

这**不是真正的错误**——只是一个通知。您的系统试图从 nginx 仓库获取 i386 (32-bit) 软件包，但 nginx 只发布 amd64 软件包。

### 选项 A：在仓库文件中指定架构（推荐）

编辑 nginx 源文件并添加 `arch=amd64` 以限制为仅 64 位：

```bash
sudo nano /etc/apt/sources.list.d/nginx.list
```

将此更改为：

```
deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu jammy nginx
```

```
deb [arch=amd64 signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu jammy nginx
```

如果没有 `signed-by` 部分，只需添加 `[arch=amd64]`，如下：

```
deb [arch=amd64] http://nginx.org/packages/ubuntu jammy nginx
```

### 选项 B：完全移除 nginx 仓库

如果您想**完全移除** nginx 外部仓库：

```bash
sudo rm /etc/apt/sources.list.d/nginx.list
```

---

## 问题 2：Mozilla 仓库 `400 Bad Request` (E: error — 这是一个真正的错误)

`400 Bad Request [IP: 127.0.0.1 7890]` 错误表示您的系统通过**本地代理**（端口 7890，可能为 Clash 或类似代理工具），并且代理阻塞或错误处理了对 `packages.mozilla.org` 的请求。

### 修复 A：移除 Mozilla apt 仓库（最干净的解决方案）

查找 Mozilla 源文件：

```bash
ls /etc/apt/sources.list.d/ | grep -i mozilla
```

然后移除它：

```bash
sudo rm /etc/apt/sources.list.d/mozilla.list
# 或根据实际文件名，例如：
sudo rm /etc/apt/sources.list.d/mozillateam-ubuntu-ppa-jammy.list
```

如果存在，也移除相关的 GPG 密钥：

```bash
sudo rm /usr/share/keyrings/mozillateam-archive-keyring.gpg
```

### 修复 B：为该特定域名绕过代理

如果您想保留 Mozilla 仓库但修复代理问题，请在代理软件（例如 Clash）中为 `packages.mozilla.org` 添加代理绕过，或为 apt 设置 `no_proxy`：

```bash
sudo nano /etc/apt/apt.conf.d/99proxy-bypass
```

添加：

```
Acquire::https::packages.mozilla.org::DIRECT "true";
```

---

## 修复后 — 运行更新以验证

```bash
sudo apt update
```

您应该不再看到 `N:` 警告或 `E:` 错误。

---

## 总结表格

| 问题 | 类型 | 解决方案 |
|---|---|---|
| `nginx binary-i386` | Warning (N:) | 在 nginx.list 中添加 `arch=amd64`，或移除该文件 |
| `Mozilla 400 Bad Request` | Error (E:) | 移除 mozilla 源文件，或修复代理绕过 |

参考资料：

- [修复 nginx i386 架构警告](https://ariq.nauf.al/blog/n-skipping-acquire-of-configured-file-nginx-binary-i386-packages-as-repository-http-nginx-org-packages-ubuntu-bionic-inrelease-doesnt-support-architecture-i386/)
- [如何修复 APT i386 架构警告 — TechOverflow](https://techoverflow.net/2025/01/27/how-to-fix-apt-skipping-acquire-of-configured-file-doesn-t-support-architecture-i386/)
- [仓库不支持 i386 架构 — It's FOSS](https://itsfoss.com/repository-doesnt-support-architecture-i386/)
