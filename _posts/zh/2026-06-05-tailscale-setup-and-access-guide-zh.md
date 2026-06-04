---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tailscale 设置与访问指南
translated: true
type: note
---

完整情况如下：

## 我们做了什么

在此机器（Ubuntu 24.04 Noble, 192.168.1.36）上安装了 Tailscale v1.98.4，并将其认证到你的 tailnet。

## 当前状态

  机器名称：  to
  账户：       lzwjava@
  状态：        已连接并运行中
  服务：       tailscaled.service（已启用，开机自启）
  版本：       1.98.4

## 这意味着你可以

1. 随时随地访问 — 只要你的其他设备（笔记本电脑、手机）也安装了 Tailscale 并登录同一账户，你就可以从任何网络访问这台机器——咖啡馆、机场、移动网络、NAT 后方，任何地方都行。

2. 加密 Mesh 网络 — Tailscale 会在你的设备之间直接建立 WireGuard 隧道。所有设备间流量均经过端到端加密。无需端口转发，也无需维护 VPN 服务器。

3. SSH 访问 — 从任何地方：
     ssh lzw@<this-machine-tailscale-ip>

4. 服务访问 — 这台机器上运行的所有服务（Web 服务器、数据库、Hermes、Jupyter 等）均可通过 Tailscale IP 从你的其他设备访问。

## 你还需要做（在其他设备上）

- 在你的 MacBook（192.168.1.49）上安装 Tailscale：<https://tailscale.com/download/mac>
- 如需移动端访问，请在手机上安装
- 使用同一账户登录（lzwjava@）
- 然后你就可以从这些设备访问这台机器了

## 常用命令

  tailscale status          — 查看已连接设备及其 IP
  tailscale ping <hostname> — 测试连通性
  tailscale ip              — 显示本机的 Tailscale IP
  sudo tailscale down       — 断开连接
  sudo tailscale up         — 重新连接

## 可选增强功能

- MagicDNS：通过名称而非 IP 访问机器（在 Tailscale 管理控制台中启用）
- Exit node：在公共 WiFi 上时，将所有流量通过此机器路由
- Subnet routes：将整个 192.168.1.0/24 局域网暴露给远程设备
- Tailscale SSH：内置 SSH，无需管理密钥
