---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 设备组访问需要修复
translated: true
type: note
---

已确认 — 以下是当前状态：

### `/dev/ttyUSB0` 存在
```
crw-rw---- 1 root dialout 188, 0 7月  8 19:21 /dev/ttyUSB0
```
该设备存在且 CH340 驱动已激活。

### 用户 `xiaoxin` **尚未**加入当前会话的 `dialout` 组
```
groups: xiaoxin adm cdrom sudo dip plugdev users lpadmin sambashare
```
`dialout` **缺失** — 之前已执行过 `usermod`（这是好的），但当前 shell 会话仍沿用旧的组设置。因此从该终端**无法访问**端口。

### 你需要做什么

**选项 A — 当前终端快速修复（无需注销）：**
```bash
exec su - $USER
```
这会启动一个带有 `dialout` 组的新登录 shell。之后用 `groups` 验证 — 你应该能看到 `dialout` 在列表中。

**选项 B — 注销并重新登录 / 重启**（对所有新终端永久生效）。

### 完成任一选项后快速测试
```bash
ls -l /dev/ttyUSB0 && screen /dev/ttyUSB0 9600
```
或者直接打开 Arduino IDE — 现在应该能够检测并连接到该端口。

需要我在这里为你执行 `exec su - $USER`，还是你更愿意自己操作？