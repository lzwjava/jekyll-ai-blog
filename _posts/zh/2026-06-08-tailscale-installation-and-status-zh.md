---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tailscale 安装与状态
translated: true
type: note
---

以下是Tailscale安装总结的翻译（IP已隐藏）：

══════════════════════════════════════════════
  Tailscale 安装总结
══════════════════════════════════════════════

已完成的操作

  1. 为 Ubuntu Noble 添加了 Tailscale 官方 APT 源
     - GPG 密钥：/usr/share/keyrings/tailscale-archive-keyring.gpg
     - 源文件：/etc/apt/sources.list.d/tailscale.list
  2. 通过 apt 安装了 tailscale v1.98.4
  3. 启用并启动了 tailscaled.service（开机自启）
  4. 使用 lzwjava@ 账户完成了身份验证

本机信息
  主机名：   xx
  状态：     已连接，已登录为 lzwjava@

你的 Tailscale 网络（4台设备）
  ┌──────────────────────┬────────┬─────────┐
  │ 设备                 │ 系统   │ 状态    │
  ├──────────────────────┼────────┼─────────┤
  │ xx（本机）           │ Linux  │ 在线    │
  │ to                   │ Linux  │ 在线    │
  │ lzw-mac              │ macOS  │ 离线    │
  │ iphone-14-pro-max    │ iOS    │ 离线    │
  └──────────────────────┴────────┴─────────┘

  “to”与本机建立了直接的 WireGuard 连接。

常用命令
  tailscale status          — 显示所有设备及其状态
  tailscale ping <设备名>   — 测试与另一设备的连接
  tailscale ip              — 显示本机的 Tailscale IP
  tailscale up              — 重新连接（如果断开）
  tailscale down            — 断开网络连接
  tailscale set --operator=$USER  — 允许非 root 用户使用
  tailscale exit-node list  — 列出可用的出口节点
  tailscale up --exit-node=<IP>  — 将所有流量通过另一设备路由

你现在可以做什么

- 通过 Tailscale IP 或主机名访问尾网中的任何设备
- 如果“to”配置了出口节点功能，可将其用作代理
- 当你的 Mac 或手机上线时，访问其上的服务
- 所有设备间的流量均通过加密的 WireGuard 隧道传输

注意：当前 tailscale 命令需要 root 权限。执行以下命令修复：
  sudo tailscale set --operator=$USER
