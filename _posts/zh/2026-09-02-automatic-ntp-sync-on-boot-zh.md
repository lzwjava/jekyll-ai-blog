---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 启动时自动NTP同步
translated: true
type: note
---

已修复。以下是总结：

- 安装了 `systemd-timesyncd`
- 已启用开机自启动
- 已激活 NTP 同步

当前状态：
- `NTP service: active`
- `System clock synchronized: yes`
- `RTC time` 也已更新为正确的同步时间

从现在开始，每次系统启动时都会自动联系 NTP 服务器并校正时钟，即使硬件 RTC 不可靠。