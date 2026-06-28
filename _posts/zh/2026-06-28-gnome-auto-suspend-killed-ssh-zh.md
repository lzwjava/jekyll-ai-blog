---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GNOME自动挂起导致SSH终止
translated: true
type: note
---

所有问题都已解决。以下是发生的情况及修复内容：

**根本原因：** GNOME 在空闲 15 分钟后自动挂起机器（`sleep-inactive-ac-type: suspend`），导致 SSH 连接断开，所有正在运行的进程（包括 mihomo）被终止。

**已应用的修复：**

- 在交流电和电池供电模式下均禁用自动挂起（`sleep-inactive-*-type: nothing`）
- 重新启动 mihomo（由于使用 `nohup` 而非 systemd 运行，重启后不会自动恢复）

**已验证：**

- Hermes v0.17.0 在 Fedora 上运行正常 ✅
- Mihomo 代理正常工作（出口 IP 69.63.219.52）✅
- `hermes chat -q` 端到端可用 ✅

**注意：** mihomo 仍然不会在重启后自动启动。是否需要我为其创建一个 systemd 服务，使其在重启后持续运行？
