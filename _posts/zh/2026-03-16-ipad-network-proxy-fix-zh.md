---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 iPad 网络和代理问题
translated: true
type: note
---

**iPad 连接问题及修复总结：**

## **1. 初始问题：DHCP 不工作**
- iPad 获取到 `169.254.x.x` (APIPA) 而非 `192.168.201.x`
- **原因：** UFW 防火墙阻塞 DHCP 端口 67/68
- **修复：** `sudo ufw allow in on enx00e04c362f89 to any port 67,68 proto udp`

## **2. 第二个问题：iPad 已连接但无互联网**
- iPad 通过 DHCP 获取到 IP `192.168.201.136` ✓
- 流量到达 Clash（日志中 `192.168.201.136 --> gateway.icloud.com`）✓
- **原因 A：** UFW 阻塞接口间的 FORWARD 流量
- **修复 A：** `sudo ufw default allow routed` + 接口路由规则
- **原因 B：** DNS 绕过 - iPad 使用 `8.8.8.8` 而非 Clash DNS (`192.168.201.1`)
- **修复 B：** 更新 dnsmasq 通过 DHCP 选项 6 推送 Clash DNS

## **3. 关键洞察：防止路由循环**
- **问题：** iPad 针对笔记本 WAN 网络 (`192.168.1.0/24`) 的流量可能循环：
iPad → Clash TUN → `192.168.1.x` → 回 WAN 接口 → 循环
- **解决方案：** 在 Clash 配置中添加明确的 `IP-CIDR,192.168.1.0/24,DIRECT` 规则
- 同时添加 `IP-CIDR,192.168.201.0/24,DIRECT` 用于 USB LAN

## **4. DNS 架构修复**
**之前：** iPad → `8.8.8.8` (绕过 Clash) → 无 fake-IP，代理中断
**之后：** iPad → `192.168.201.1` (Clash DNS) → fake-IP → TUN 拦截 → 代理

## **5. 分流路由配置**
更新 Clash 规则：
- 本地子网 (`192.168.1.0/24`, `192.168.201.0/24`) → DIRECT
- Apple/iCloud 服务 → DIRECT (用于 iPad 功能)
- 中国网站 → DIRECT
- 其他所有 → Hysteria2 代理

## **当前状态：**
- ✅ DHCP 正常工作 (iPad 获取 `192.168.201.136`)
- ✅ 防火墙允许转发
- ✅ NAT 伪装激活
- ✅ Clash 运行分流路由
- ✅ DNS 指向 Clash (`192.168.201.1`)
- ✅ 已设置循环预防规则

**剩余步骤：** iPad 需要续订 DHCP 租约以获取新 DNS 设置，或手动设置 DNS 为 `192.168.201.1`。

**iPad 测试命令：**
```bash
nslookup google.com 192.168.201.1 # 应返回 fake IP (198.18.0.x)
curl https://api.ipify.org # 应显示 69.63.0.0 (US IP)
curl baidu.com # 应正常工作 (DIRECT)
```

架构现已正确。任何剩余问题很可能与 DNS 相关 (iPad 缓存旧 `8.8.8.8` DNS) 或 Hysteria2 代理连接。
