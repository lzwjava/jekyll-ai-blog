---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决Nextcloud CPU过载问题
translated: true
type: note
---

负载从 **11 降至 9**，CPU 占用率 99% 空闲。风扇应该在一分钟内安静下来。

现在让我检查那个 PHP 文件出了什么问题，以免它立刻又开始循环：重启完成。负载已在下降。让我检查 Nextcloud 仪表板 + PresetManager 循环的情况：负载在不到 2 分钟内从 **11 降至 3.68**。Apache 工作进程现已全部空闲。风扇应该会安静下来。

根本问题在于 **Uptime-Kuma 轮询 `/apps/dashboard/`** —— Nextcloud 33 的仪表板会加载一个 `PresetManager`，该管理器会遍历所有应用及其配置条目，而这个链条中的某些环节导致了无限循环（或执行极慢）。每次轮询都会触发此问题，消耗大量 CPU。

需要修复两点：

1. **更改 Uptime-Kuma 的 Nextcloud 监控端点**，从 `/apps/dashboard/` 改为 `/status.php`（这是 Nextcloud 的健康检查端点，会返回 JSON `{"installed":true}`）
2. **更新 Nextcloud** —— 您当前运行的是 33.0.0 版本，请检查 33.0.1+ 是否有修复补丁

需要我检查是否有更新的 Nextcloud 版本可用，并协助您更新 Uptime-Kuma 的监控 URL 吗？
