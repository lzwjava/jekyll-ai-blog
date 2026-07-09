---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 权限拒绝拨出组修复
translated: true
type: note
---

以下是完整情况：

---

## ✅ 问题已发现：权限被拒绝 — 不在 `dialout` 用户组

**修复已应用**，但以下是发生的情况以及你需要了解的内容：

### 根本原因
- `/dev/ttyUSB0` 存在，且你的 Arduino（通过 **CH340** USB 串口芯片，ID `1a86:7523`）已被检测到
- 端口的所有者为 `root:dialout`，权限为 `rw-rw----`（660）
- 你的用户不在 `dialout` 组中 → **没有读写权限**

### 我已执行的操作
- 通过 `usermod -aG dialout xiaoxin` 将你添加到了 `dialout` 组
- 使用 `newgrp dialout` 验证了端口现在可访问

### 你仍需执行的操作
**注销并重新登录**（或重启），以便组更改在终端模拟器中永久生效，或者执行：

```bash
exec su - $USER
```

在当前终端中获取一个新的登录 shell，使 `dialout` 组生效。

### 组生效后的快速测试
```bash
screen /dev/ttyUSB0 9600
```
或者使用你的 Arduino IDE / 应用 — 现在应该可以正常连接。

### 总结

| 项目 | 状态 |
|------|------|
| 设备已检测到 | ✅ `/dev/ttyUSB0` 上的 CH340 |
| 驱动已加载（`ch341-uart`） | ✅ |
| 权限 | ✅ 已修复（之前缺少 `dialout` 组） |
| 端口被其他进程占用 | ❌ 否 — 可以连接 |
| 应用可连接 | ⏳ 重新登录 / 执行 `exec su - $USER` 后 |