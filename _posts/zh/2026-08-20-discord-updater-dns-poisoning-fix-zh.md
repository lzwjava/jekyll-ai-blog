---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Discord更新程序DNS污染修复
translated: true
type: note
---

一切正常。最终确认：

- 通过原始 TUN（无代理环境，完全模拟 Discord 更新器行为）获取 **Manifest**：`HTTP 200`，来自假 IP `198.18.0.4`
- 从 Discord 的 CDN（`stable.dl2.discordapp.net` → `198.18.0.13`）下载完整的 **171 MB 更新包**：`HTTP 200`

更新日志中仅显示旧的失败记录（时间戳 **20:39–20:40**，在 DNS 修复之前）。它已不再重试——但请注意，这些条目均为 *修复前* 的记录。

## 问题所在（涉及两个层面）

1. **根本原因：** Discord 的更新器（`updater.node`）是一个 **原始套接字**，会忽略 macOS 的代理设置 → 因此需要 TUN。
2. **第二个层面（开启 TUN 后发现）：** 系统路由器 DNS（`192.168.1.1`）**投毒**了 `updates.discord.com` → 返回 **Meta IP `157.240.6.35`**。由于 mihomo 获取的是 *真实* 的被污染 IP，而非自身的假 IP，TUN 无法将该连接映射回主机名，因此流量从未经过你的 Hysteria2 节点。连接因 `-9806（连接因错误关闭）` 而终止。

## 已应用的修复

1. 在 `~/.config/mihomo/config.yaml` 中 **启用 TUN**（`tun.enable: true`，`stack: gvisor`，`any:53` DNS 劫持）——你已重启 mihomo，现在 `utun4` 上显示 **`enable: True`**，流量正确命中你的 **`My Hysteria2 2`** 节点。
2. 在 **Wi-Fi** 服务上将系统 DNS 设置为 **`127.0.0.1`**（mihomo）（之前由路由器处理 DNS）：

   ```
   networksetup -setdnsservers Wi-Fi 127.0.0.1
   ```

   现在 `updates.discord.com` 解析为 mihomo 的 **假 IP**（`198.18.0.4`），而非被污染的 Meta IP。

## 你的下一步操作

那些 `-9806` 错误全部来自 **DNS 修复之前**。既然现在域名解析走 mihomo，**完全退出 Discord 并重新启动**（⌘Q，不要只关闭窗口），让更新器发起新的检查。现在它应该能完成并下载更新。

注意：将 Wi-Fi DNS 指向 `127.0.0.1` 意味着 **所有名称解析都依赖 mihomo 正常运行**。这是为了实现可靠代理所付出的权衡；使用网络前请确保 mihomo 已启动。如果你希望限定范围，我可以保持当前设置（推荐你的配置）——重启 Discord 后请告诉我更新是否完成。
