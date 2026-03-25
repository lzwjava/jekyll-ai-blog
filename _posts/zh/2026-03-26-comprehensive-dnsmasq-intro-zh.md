---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Dnsmasq 软件全面介绍
translated: true
type: note
---

问题：dnsmasq 的全面介绍是什么？

回答：

## 什么是 dnsmasq？

Dnsmasq 是一款免费软件，为小型计算机网络提供 Domain Name System (DNS) 缓存、Dynamic Host Configuration Protocol (DHCP) 服务器、Router Advertisement 和网络启动 (Network Boot) 功能。它对系统资源的要求极低，可以在 Linux、BSDs、Android 和 macOS 上运行，并被大多数 Linux 发行版所包含。因此，它存在于许多家用路由器和 IoT 设备中，也被内置于 Android 系统中。

它被设计为轻量级且占用空间小，适用于资源受限的路由器和防火墙。它还被广泛用于智能手机的热点共享、便携式热点，以及在虚拟化框架中支持虚拟网络。

---

## 核心组件与功能

### 1. DNS 子系统

DNS 子系统为网络提供本地 DNS server，将所有查询类型转发到上游的递归 DNS server，并缓存常见的记录类型（A、AAAA、CNAME 和 PTR，以及启用 DNSSEC 时的 DNSKEY 和 DS）。本地 DNS 名称可以通过读取 `/etc/hosts`、从 DHCP 子系统导入名称或配置各种实用的记录类型来定义。

Dnsmasq 接收 DNS 查询，要么从较小的本地 cache 中回答，要么将其转发到真实的递归 DNS server。它会加载 `/etc/hosts` 的内容，以便解析全球 DNS 中未出现的本地 hostname，并为 DHCP 配置的主机回答 DNS 查询。

**重要区别：** Dnsmasq 是一个 *forwarding/stub* 解析器，而不是 *recursive*（递归）解析器。这意味着 dnsmasq 始终需要一个可以转发查询的递归 DNS 解析器。

### 2. DHCP 子系统

DHCP 子系统支持 DHCPv4、DHCPv6、BOOTP 和 PXE。支持静态和动态 DHCP lease，以及 DHCPv6 中的 stateless 模式。

Dnsmasq 的 DHCP server 支持静态和动态 DHCP lease、多网络和 IP 地址范围。DHCP server 与 DNS server 集成，允许拥有 DHCP 分配地址的本地机器出现在 DNS 中。

### 3. TFTP 服务器

Dnsmasq 包含一个安全的、只读的 TFTP server，允许 DHCP 主机进行网络/PXE boot，并且支持 BOOTP。它提供完整的 PXE 支持。

### 4. Router Advertisement (IPv6)

Router Advertisement 子系统为 IPv6 主机提供基础的自动配置。它可以独立使用，也可以与 DHCPv6 配合使用。M 位和 O 位是可配置的，用于控制主机对 DHCPv6 的使用。Router Advertisement 可以包含 RDNSS 选项。

---

## 安装

**Debian / Ubuntu:**

```bash
sudo apt-get install dnsmasq
```

**CentOS / RHEL:**

```bash
sudo yum install dnsmasq
```

**Arch Linux:**

```bash
sudo pacman -S dnsmasq
```

安装后，启用并启动服务：

```bash
sudo systemctl enable --now dnsmasq
```

---

## 配置文件

主要配置文件是 `/etc/dnsmasq.conf`。该文件包含解释各选项的注释。附加配置文件可以放置在 `/etc/dnsmasq.d/` 目录中，并以 `.conf` 为后缀。

在应用配置前验证语法：

```bash
dnsmasq --test
```

---

## 关键配置示例

### DNS 转发 (上游服务器)

```ini
# /etc/dnsmasq.conf
server=8.8.8.8
server=1.1.1.1
```

### DNS 缓存 (本地解析)

```ini
listen-address=127.0.0.1
cache-size=1000
```

### DHCP 服务器

```ini
# 在指定范围内启用 DHCP，租期为 12 小时
dhcp-range=192.168.1.50,192.168.1.150,12h
```

### 通过 MAC 地址分配静态 IP

```ini
dhcp-host=00:11:22:33:44:55,192.168.1.100
```

### 限制在特定接口

```ini
interface=eth0
bind-interfaces
```

### 调试日志

```ini
log-queries
log-facility=/var/log/dnsmasq.log
```

---

## DNSSEC 验证

当启用 DNSSEC 时，dnsmasq 会验证 DNS 响应并缓存 DNSSEC 数据。在转发 DNS 查询时，dnsmasq 会请求验证响应所需的 DNSSEC 记录。响应经过验证后，结果将作为 DNS 数据包中的 Authenticated Data 位返回。

在 Arch Linux / Debian 上启用 DNSSEC：

```ini
conf-file=/usr/share/dnsmasq/trust-anchors.conf
dnssec
```

---

## PXE / 网络启动

PXE 需要 DHCP 和 TFTP server；这两者都可以由 dnsmasq 提供。在 `dnsmasq.conf` 中的基础 PXE 设置：

```ini
enable-tftp
tftp-root=/srv/tftp
pxe-service=x86PC,"PXELINUX (BIOS)",bios/lpxelinux
pxe-service=X86-64_EFI,"PXELINUX (EFI)",efi64/syslinux.efi
```

Dnsmasq 也可以设置为 "proxy DHCP" 模式，当网络中已有另一个 DHCP server 运行时，仅向客户端提供 PXE 特定信息。

---

## 广告拦截 / DNS 过滤

添加到本地 `/etc/hosts` 文件中格式为 `0.0.0.0 annoyingsite.com` 的记录，可以阻止浏览器解析该域名。结合广告拦截站点列表，这可以迅速演变为本地广告拦截器。如果在路由器上执行，可以高效地为整个家庭或公司移除广告内容。

某些 ISP 会重写 NXDOMAIN 响应，当域名不存在时强制浏览器跳转到搜索页面。Dnsmasq 可以过滤掉这些“虚假”的 NXDOMAIN 记录，阻止这种可能不被欢迎的行为。

---

## Split DNS (VPN / 内部域名)

指定的子域名可以被定向到它们自己的上游 DNS server，使 VPN 配置变得简单。

```ini
# 将内部域名路由到私有 DNS 服务器
server=/internal.company.com/10.0.0.1
```

---

## Authoritative DNS 模式

Authoritative DNS 模式允许将本地 DNS 名称导出到全球 DNS 的 zone 中。Dnsmasq 充当该 zone 的 authoritative server，并在需要时为该 zone 的 secondary 提供区域传输 (zone transfer)。

---

## 常见用例

| 用例 | dnsmasq 的作用 |
|---|---|
| 家庭/办公室路由器 | 为所有 LAN 设备提供 DNS 转发 + DHCP |
| 开发环境 | 本地域名解析（例如 `myapp.local`） |
| VPN 分流路由 | 将特定域名路由至内部 DNS |
| 网络启动 (PXE) | 为无盘启动提供 DHCP + TFTP |
| 广告拦截 | 通过 `/etc/hosts` 或 `address=` 指令拦截域名 |
| IoT 网络 | 为受限环境提供轻量级 DHCP + DNS |
| 虚拟机网络 | 为 `libvirt`/VirtualBox/VMware 客户机网络提供 DNS/DHCP |

---

## 平台支持

支持的平台包括 Linux（支持 glibc 和 uclibc）、Android、*BSD 和 macOS。Dnsmasq 被包含在大多数 Linux 发行版以及 FreeBSD、OpenBSD 和 NetBSD 的 ports 系统中。Dnsmasq 提供完整的 IPv6 支持。

---

## 须知局限性

- **不建议**将 Dnsmasq 作为面向公网的 DNS server。它旨在私有网络内提供服务。
- 它是一个 stub/forwarding 解析器，**不是**像 Unbound 或 BIND 那样的完整递归解析器。
- 对于具有快速故障转移需求的大型企业级设置，像 KEA DHCP 这样的替代方案可能更合适。

---

## 信号与运行时控制

| 信号 | 效果 |
|---|---|
| `SIGHUP` | 重新加载 `/etc/hosts` 和配置 |
| `SIGUSR1` | 将 cache 统计信息导出到日志 |
| `SIGUSR2` | 轮转日志文件 |

---

## 总结

Dnsmasq 是一款优雅的一体化网络服务守护进程，非常适合中小型网络。它的优势在于将 DNS 缓存/转发、DHCP、TFTP、PXE 启动和 IPv6 Router Advertisement 整合进一个轻量级的二进制文件中，并拥有简单且记录详尽的配置文件。它是全世界嵌入式路由器、家庭实验室、开发环境和 IoT 网络的事实标准。

参考资料：

- [dnsmasq 官方文档](https://thekelleys.org.uk/dnsmasq/doc.html)
- [dnsmasq Man Page](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)
- [dnsmasq - Wikipedia](https://en.wikipedia.org/wiki/Dnsmasq)
- [dnsmasq - ArchWiki](https://wiki.archlinux.org/title/Dnsmasq)
- [dnsmasq - Gentoo Wiki](https://wiki.gentoo.org/wiki/Dnsmasq)
- [dnsmasq Command Guide - TutorialsPoint](https://www.tutorialspoint.com/unix_commands/dnsmasq.htm)
- [OPNsense dnsmasq 文档](https://docs.opnsense.org/manual/dnsmasq.html)