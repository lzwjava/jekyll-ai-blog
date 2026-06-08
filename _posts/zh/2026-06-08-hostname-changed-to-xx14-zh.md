---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 主机名改为xx14
translated: true
type: note
---

以下是您所做更改及其影响的摘要：

## 主机名更改摘要

### 已完成的操作
```
旧名称：  xiaoxin-XiaoXin-14-IAH8
新名称：  xx14
```

共修改了两个文件：
- `/etc/hostname` — 通过 `hostnamectl set-hostname xx14` 修改
- `/etc/hosts` — 将旧主机名替换为 `xx14`，确保本地解析仍然有效

### 影响范围
- 终端提示符：现在显示为 `xiaoxin@xx14`，而非 `xiaoxin@xiaoxin-XiaoXin-14-IAH8`
- `hostname` 命令返回 `xx14`
- 所有广播主机名的网络服务（SSH、mDNS/Bonjour、Samba）将使用 `xx14`
- 若从其他设备连接本机，指向旧名称的 SSH known_hosts 条目可能需要更新

### 未改变的内容
- 用户名（仍为 `xiaoxin`）
- 主目录（`/home/xiaoxin`）
- WiFi/网络连接
- 硬件识别信息（MAC 地址、序列号等）

### 小提示
- 此更改是永久性的 — 重启后仍生效
- 如需还原：`sudo hostnamectl set-hostname xiaoxin-XiaoXin-14-IAH8`
- 打开新的终端标签页或 Shell 即可看到更新后的提示符（当前会话仍显示旧名称）