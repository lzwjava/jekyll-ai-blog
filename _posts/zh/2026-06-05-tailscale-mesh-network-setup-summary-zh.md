---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tailscale 网状网络设置摘要
translated: true
type: note
---

```
══════════════════════════════════════════════════════════════
  Tailscale 配置 — 完整摘要
══════════════════════════════════════════════════════════════

构建内容
  利用 Tailscale (WireGuard) 在 MacBook Air 和 Ubuntu 工作站之间
  构建了一个安全加密的网状网络。现在您可以从任何地方
  — 家庭局域网、咖啡厅、机场、移动网络 — SSH 访问工作站上的服务，
  无需端口转发或 VPN 服务器。

您的 Tailnet 中的设备
  账户： lzwjava@

  1. lzw-mac  (MacBook Air M2, macOS)
     角色：    日常主力机
     Tailscale IP： 100.x.x.x

  2. to       (Ubuntu 24.04, RTX 4070)
     角色：    GPU/ML 工作站
     运行时间： 45 天
     Tailscale IP： 100.x.x.x

连接状态
  Ping：         ~8ms (通过 WireGuard 直连局域网路径)
  隧道：       端到端加密，点对点网状网络
  SSH：         公钥认证，无需密码
  NAT 穿透：    自动完成 — 适用于任何网络

操作步骤

  1. 工作站 (to)
     - 安装 Tailscale v1.98.4
     - 启用 tailscaled.service (开机自启动)
     - 认证到 lzwjava@ tailnet

  2. MacBook Air (lzw-mac)
     - 从 App Store 安装 Tailscale GUI 应用 (v1.98.5)
     - 安装 Homebrew CLI (v1.96.4) — 导致每次命令都出现版本不匹配警告
     - 认证到同一个 tailnet
     - 修复版本不匹配：
       • 卸载旧的 Homebrew CLI (v1.96.4)
       • 在 /opt/homebrew/bin/tailscale 创建包装脚本，
         委托给 GUI 应用的二进制文件 (v1.98.5)
       • 客户端和服务器现在均报告 v1.98.5
       • 不再有警告

  3. 连接验证
     - tailscale ping: 8ms，直连局域网
     - SSH: 公钥认证正常工作
     - 主机密钥已添加到 ~/.ssh/known_hosts

当前 CLI 工作方式
  /opt/homebrew/bin/tailscale
    ↓ (包装脚本，转发所有参数)
  /Applications/Tailscale.app/Contents/MacOS/Tailscale
    ↓ (与以下通信)
  tailscaled (由 GUI 应用的系统扩展管理，无需 sudo)

  GUI 应用管理守护进程生命周期 — 登录时启动 tailscaled，
  睡眠后重新连接，管理系统扩展。无需 sudo，无需手动服务管理。

实用命令
  tailscale status          — 查看已连接设备
  tailscale ping <主机>     — 测试连接
  tailscale ip              — 显示本机的 Tailscale IP
  tailscale down            — 断开连接
  tailscale up              — 重新连接
  ssh lzw@<工作站 IP>      — 从任何地方 SSH 连接

可选增强功能 (Tailscale 管理控制台)
  MagicDNS      — 通过主机名而非 IP 访问设备
  Exit node     — 在公共 WiFi 上将所有流量路由通过工作站
  Subnet routes — 远程暴露整个 192.168.1.0/24 局域网
  Tailscale SSH — 内置 SSH，无需密钥管理
══════════════════════════════════════════════════════════════
```