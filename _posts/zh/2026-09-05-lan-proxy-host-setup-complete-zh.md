---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 局域网代理主机设置完成
translated: true
type: note
---

完成！✅ 位于 `192.168.1.42` 的笔记本电脑现在已经是一个可用的代理主机（无需 OpenWrt）。

## 已配置的内容

| 项目 | 详情 |
|---|---|
| **二进制文件** | mihomo v1.19.30 (linux-amd64-v1) → `/usr/local/bin/mihomo` |
| **配置文件** | 从 Mac 的 `~/.config/mihomo/` 复制 → `/etc/mihomo/`（包含 `Rules/` 提供者 + geoip） |
| **服务** | `mihomo.service` systemd 单元，`enabled`（开机启动），以 root 身份运行并启用 TUN |
| **端口** | HTTP `7890`、SOCKS `7891`、Mixed `7892`、API `9090` — 通过 ufw 开放给局域网 |

## 途中发现并修复的两个问题

1. **系统时钟错误** — 笔记本电脑的 RTC 电池耗尽（BIOS 时钟显示 2003 年），导致系统时间停留在 2026-05-25。代理服务器的 TLS 证书（有效期从 8 月 26 日开始）被拒绝 → 所有代理连接失败。从 Mac 手动设置时钟；NTP（`ntp.ubuntu.com`）现在保持同步（偏移约 1ms）。
2. **ufw 阻止局域网** — 之前尝试 OpenWrt 时的遗留问题，INPUT 策略为 DROP。添加了允许规则，针对 `192.168.1.0/24` 网段的 7890–7892 和 9090 端口。

## 已验证

- 在笔记本电脑本机上：TUN 模式正常工作（流量自动代理），Google/GitHub 返回 200，百度走 DIRECT
- 从你的 Mac：`http://192.168.1.42:7892` 可作为全局域网代理使用（出口 IP `69.63.219.52`，你的 dmit VPS）

因此，局域网中的任何设备现在只需将代理设置为 `192.168.1.42:7892`（或者笔记本电脑本身通过 TUN 透明代理所有流量）。如果你想要 Web 界面，还可以从局域网访问 `http://192.168.1.42:9090` 的仪表盘 API。