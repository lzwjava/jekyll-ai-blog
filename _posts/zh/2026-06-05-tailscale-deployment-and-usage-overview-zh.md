---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tailscale 部署与使用概述
translated: true
type: note
---

══════════════════════════════════════════
  Tailscale 设置摘要
══════════════════════════════════════════

账号：        lzwjava@

机器1 — lzw-mac (本机 MacBook Air M2)
  操作系统：           macOS
  Tailscale：    v1.96.4 (Homebrew CLI)
  角色：         日常使用机

机器2 — to (Ubuntu 工作站)
  操作系统：           Ubuntu 24.04 Noble
  Tailscale：    v1.98.4
  角色：         GPU/ML 工作站 (RTX 4070)
  运行时间：       45 天
  服务：       tailscaled.service (已启用，开机自启)

连接性
  Ping：         10ms (直接局域网, WireGuard)
  隧道：       端到端加密，点对点
  SSH：          公钥认证，无需密码
  NAT：          自动穿透 — 可在任何网络中使用

您现在可以做什么
  • 从任何地方通过 SSH 连接到工作站：
      ssh lzw@<workstation-tailscale-ip>
  • 通过 Tailscale IP 访问工作站上的任何服务（Jupyter、Web
    服务器、数据库）
  • 无需端口转发、VPN 服务器或防火墙更改
  • 可在咖啡馆、机场、移动网络、NAT 后使用

可选增强功能（从 Tailscale 管理控制台）
  • MagicDNS — 通过主机名而非 IP 访问机器
  • Exit node — 在公共 WiFi 时将所有流量路由通过工作站
  • Subnet routes — 将整个局域网暴露给远程设备
  • Tailscale SSH — 内置 SSH，无需密钥管理

版本不匹配说明
  客户端 (1.96.4) != 服务器 (1.98.5)。功能正常，
  但建议更新： brew upgrade tailscale
══════════════════════════════════════════
