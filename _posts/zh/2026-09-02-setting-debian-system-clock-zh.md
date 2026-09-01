---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 设置Debian系统时钟
translated: true
type: note
---

问题：如何在 Debian 13 上设置系统时钟。

答案：

### 检查当前时间

```bash
date
timedatectl
```

### 推荐：设置时区

如果你想使用 **中国时间**：

```bash
sudo timedatectl set-timezone Asia/Shanghai
```

检查：

```bash
timedatectl
```

你应该会看到：

```text
Time zone: Asia/Shanghai (CST, +0800)
```

### 如果实际时钟有误

启用 NTP 时间同步：

```bash
sudo timedatectl set-ntp true
```

然后：

```bash
timedatectl
```

查找：

```text
System clock synchronized: yes
NTP service: active
```

这比手动设置时钟更可取。

### 手动设置

如果没有网络/NTP 可用：

```bash
sudo timedatectl set-time '2026-09-02 03:15:00'
```

然后验证：

```bash
date
```

**对于你的 Debian Live 安装，我会执行：**

```bash
sudo timedatectl set-timezone Asia/Shanghai
sudo timedatectl set-ntp true
timedatectl
```

如果你在双系统启动 **Windows + Debian**，还有一个额外的时钟问题值得注意：Linux 通常将硬件 RTC 视为 UTC，而 Windows 通常将其视为本地时间。
