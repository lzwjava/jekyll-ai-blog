---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络设备识别技术
translated: true
type: note
---

# 我是如何识别你的网络设备的
=======================================

**方法 1：ARP 表**
  命令：`arp -a`
  作用：显示你的 Air 曾通信过的所有设备的 IP → MAC 映射。
  `.52` 上的 `permanent` 标志 = 本机（你的 Air）。
  `ifscope` = 所有条目均位于 en0（WiFi）。

**方法 2：Ping 扫描**
  命令：`ping -c 1 -W 1000 <ip>`（逐个扫描，或使用网络 IP 扫描工具）
  发现哪些 IP 在线，哪些不可达。
  在 254 个可能地址中找到了 13 个活跃主机。
  “down” 不一定意味着设备已消失——可能是防火墙屏蔽了 ICMP。

**方法 3：OUI 厂商查询**
  MAC 地址的前 3 个字节 = 制造商 ID（OUI）。
  使用 curl 调用 macvendors.com API 识别出：
  `88:e9:fe` → Apple
  `68:ab:bc` → 小米
  `3c:6a:48` → TP-LINK
  `68:c6:ac` → Intel
  `dc:ed:83` → 小米
  `4:7c:16`  → ASRock（你的工作站）

**方法 4：本地管理 MAC 检测**
  当第一个字节的第 1 位被置位时，该 MAC 为“本地管理”。
  这意味着它不是硬件烧录的 MAC——而是随机生成的。
  Apple 在“私有 WiFi 地址”功能中使用此方式（iOS 14+、macOS 12+）。
  17 台设备中有 7 台使用了本地管理 MAC → 很可能是 Apple 设备。

**方法 5：TTL 分析**
  TTL 64  → Linux/macOS（路由器、工作站、MacBook）
  TTL 32  → iPhone/iPad（省电模式、高抖动）
  TTL 128 → Windows
  .49 的 TTL 为 32 + 95ms 延迟 → 手机/平板，而非 MacBook。

**方法 6：延迟模式分析**
  有线设备（.36）：  平均 12ms，低抖动
  WiFi 设备（.1、.49）：平均 20-95ms，高抖动
  省电模式设备：    平均 400ms+，极高抖动（45-1045ms）
  环回地址（.52）：  平均 0.6ms（ping 自身）

**方法 7：mDNS / Bonjour**
  尝试运行 `dns-sd -B _ssh._tcp local.`——未发现任何结果。
  大多数设备不广播服务。

**我无法做到的事：**
  - 访问路由器管理页面（需要登录凭据）
  - 执行 traceroute（本地局域网中跳点屏蔽了 ICMP）
  - 通过 SSH 登录设备（无凭据）
  - 运行 nmap 端口扫描（未安装）

**设备识别总结：**
  .1   = 路由器（根据位置 + 网关路由）
  .36  = 工作站（ARP 主机名 “myapp.loca” + ASRock OUI）
  .52  = 本机 Air（ARP “permanent” 标志 + 本地 IP）
  .49  = Apple 设备（真实 Apple OUI + TTL 32 = 很可能是手机）
  .14, .33 = 小米（OUI 确认）
  .18  = TP-LINK（OUI 确认）
  .20  = Intel（OUI 确认，很可能是有线设备）
  其余 = Apple 私有 WiFi 地址设备
