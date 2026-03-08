---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Dig 命令 DNS 指南精要
translated: true
type: note
---

**问题：** 什么是针对 DNS 用途的 `dig` 命令的全面介绍？

**答案：**

---

## 什么是 `dig`？

`dig`（Domain Information Groper）是一个用于查询域名系统（DNS）的强大工具。它通常用于排查域名解析问题并获取 DNS 记录的详细信息。`dig` 实用程序是 Berkeley Internet Name Domain (BIND) 套件的一部分，这是由 Internet Systems Consortium (ISC) 维护的广泛使用的 DNS 软件包。

对于网络管理员和开发者来说，它是诊断 DNS 问题、验证配置以及深入了解域名如何解析为 IP 地址的必不可少工具。

---

## 安装

在大多数 Linux 发行版中，`dig` 命令是 `dnsutils` 或 `bind-utils` 软件包的一部分。在基于 Debian 的系统（如 Ubuntu）上，您可以使用发行版的包管理器安装它。

```bash
# Ubuntu/Debian
sudo apt install dnsutils

# CentOS/RHEL
sudo yum install bind-utils

# 验证安装
dig -v
```

`dig` 在大多数 macOS 版本和某些 Linux 发行版中预装。

---

## 基本语法

```bash
dig [@server] [domain] [type] [options]
```

其中：
- `@server` — 可选。指定要查询的 DNS 服务器。如果省略，`dig` 使用默认服务器。
- `domain` — 要查询的域名。
- `query-type` — 所需的 DNS 记录类型（例如 A、MX、NS）。如果未指定，`dig` 默认查询 A 记录。

默认情况下，`dig` 将查询定向到 `/etc/resolv.conf` 文件中列出的 DNS 服务器，但它也提供了直接查询任何其他名称服务器的灵活性。

---

## 理解输出部分

典型的 `dig` 响应包含以下部分：

### 1. 头部部分
HEADER 部分总结了 DNS 查询和响应细节。它包括查询类型（例如标准查询）、响应状态（例如成功响应的 NOERROR）以及指示关键属性的标志，如递归。

### 2. 问题部分
此部分显示查询细节，包括请求的域名和记录类型。例如，对 `example.com` 的 A 记录查询表示请求将域名解析为 IPv4 地址。

### 3. 回答部分
回答部分包含查询返回的实际 DNS 记录，例如 A 记录查找的 IP 地址。例如：`example.com. 3600 IN A 93.184.216.34` — 这表明 `example.com` 解析为 IPv4 地址 `93.184.216.34`，生存时间 (TTL) 为 3600 秒。

### 4. 权威部分
如果查询的 DNS 服务器对域名具有权威性，此部分列出负责该域名的权威名称服务器。例如：`example.com. 172800 IN NS a.iana-servers.net.`。

### 5. 附加部分
此部分可能包含额外信息，例如权威部分中列出的权威名称服务器的 IP 地址。

### 6. 页脚 / 统计信息
在页脚部分，您可以找到以毫秒为单位的延迟时间，以及用于解决请求的 DNS 服务器。

---

## 常见 DNS 记录类型

| 记录类型 | 用途 |
|----------|------|
| `A` | 域名的 IPv4 地址 |
| `AAAA` | 域名的 IPv6 地址 |
| `MX` | 邮件交换服务器 |
| `NS` | 权威名称服务器 |
| `CNAME` | 规范名称（别名） |
| `TXT` | 文本记录（SPF、DKIM 等） |
| `PTR` | 反向 DNS（IP → 主机名） |
| `SOA` | 权威记录开始 |

---

## 实际示例

### 1. 基本 DNS 查找（A 记录）
```bash
dig google.com
```

### 2. 仅短输出
```bash
dig +short google.com
```
`+short` 仅显示最相关信息，例如 A 记录的 IP 地址。

### 3. 查询特定记录类型
```bash
dig google.com MX
dig google.com NS
dig google.com TXT
dig google.com AAAA
```

### 4. 使用特定 DNS 服务器查询
```bash
dig @8.8.8.8 google.com
```
默认情况下，`dig` 命令查询 `/etc/resolv.conf` 中列出的名称服务器。您可以使用 `@` 符号后跟名称服务器的主机名或 IP 地址来更改此设置。

### 5. 跟踪完整的 DNS 解析路径
```bash
dig +trace google.com
```
`+trace` 命令用于跟踪 DNS 查找路径。此选项执行迭代查询来解析名称查找，从根开始查询名称服务器，并使用迭代查询遍历命名空间树，沿途跟随引荐。

### 6. 反向 DNS 查找（IP 到主机名）
```bash
dig -x 8.8.8.8
```
使用 `-x` 选项和 IP 地址来查找关联的域名。反向 DNS 查找仅在存在 PTR 记录时有效。

### 7. 仅查询回答部分（干净输出）
```bash
dig +noall +answer google.com
```
`+noall` 抑制除明确请求的所有输出部分。`+answer` 仅显示输出的回答部分，通常与 `+noall` 一起使用。

### 8. 从文件批量查询
```bash
dig -f domains.txt +short
```
可以一次性查询域名列表，而不是为每个域名逐一执行 `dig` 查询。将域名输入文件（每行一个域名）并对文件执行 `dig` 查询。

### 9. 检查 DNSSEC 信息
```bash
dig +dnssec google.com
```
此命令查询带有 DNSSEC（域名系统安全扩展）信息的 DNS 记录。

### 10. 获取统计信息
```bash
dig +stats google.com
```
`+stats` 选项用于查看统计部分。

---

## 关键选项总结

| 选项 | 描述 |
|------|------|
| `+short` | 仅显示基本结果 |
| `+noall` | 抑制所有输出部分 |
| `+answer` | 仅显示回答部分 |
| `+trace` | 从根跟踪完整解析 |
| `+nocmd` | 省略初始命令行 |
| `+stats` | 显示查询统计 |
| `+dnssec` | 包含 DNSSEC 数据 |
| `@server` | 查询特定 DNS 服务器 |
| `-x` | 反向 DNS 查找 |
| `-f file` | 从文件批量查找 |

---

## `dig` 与 `nslookup`

`dig` 提供更详细的输出和高级查询选项，而 `nslookup` 更简单但在 DNS 故障排除方面功能较弱。大多数 DNS 管理员和系统管理员更喜欢 `dig`，因为其可脚本化和全面输出。

---

## 常见用例

您可以使用 `dig` 命令来：诊断您的名称服务器；检查所有服务器或每个单独服务器及其响应；检查所有可用 DNS 记录或单个 DNS 记录及其参数；跟踪 IP 地址并查看对应的主机名；通过特定端口执行查询；查看 DNS 记录的 TTL 值；以及跟踪 DNS 查询的路由。

---

**参考资料：**

- [phoenixnap.com — dig Command in Linux with Examples](https://phoenixnap.com/kb/linux-dig-command-examples)
- [geeksforgeeks.org — dig command in Linux with Examples](https://www.geeksforgeeks.org/linux-unix/dig-command-in-linux-with-examples/)
- [linuxize.com — How to Use dig Command to Query DNS](https://linuxize.com/post/how-to-use-dig-command-to-query-dns-in-linux/)
- [cloudns.net — 10 Most Used DIG Commands](https://www.cloudns.net/blog/10-most-used-dig-commands/)
- [ditig.com — Dig Cheat Sheet](https://www.ditig.com/dig-cheat-sheet)
- [cyberciti.biz — Linux and Unix dig Command Examples](https://www.cyberciti.biz/faq/linux-unix-dig-command-examples-usage-syntax/)
- [howtouselinux.com — Dig Command in Linux: A Comprehensive Guide](https://www.howtouselinux.com/post/linux-dig-dns)