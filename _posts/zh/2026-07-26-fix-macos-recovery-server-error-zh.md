---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 macOS 恢复服务器错误
translated: true
type: note
---

问题：**在 2017 款 MacBook Pro 上重新安装 macOS 时，macOS 恢复显示“无法联系恢复服务器”。如何解决？**

答案：

此错误在使用互联网恢复时对 Intel Mac 很常见。通常意味着 **网络/日期/Apple 服务器证书验证** 问题，而非 SSD 损坏。

请按顺序尝试以下方法。

---

## 1. 检查恢复模式下的日期/时间（最常见）

启动进入恢复模式：

```
Command (⌘) + R
```

打开：

```
实用工具 → 终端
```

检查：

```bash
date
```

如果日期错误（例如 2020/2010），请手动设置。

示例：

```bash
date 072609302026
```

格式：

```
MMDDhhmmYYYY
```

上方示例：

```
07/26 09:30 2026
```

然后重试：

```
重新安装 macOS
```

---

## 2. 使用互联网恢复替代本地恢复

对于 2017 款 MacBook Pro：

关机。

按住：

```
Option + Command + R
```

持续按住直到出现地球图标。

这会下载兼容的最新版 macOS。

不要使用：

```
Command + R
```

因为那可能会加载旧版恢复分区。

---

## 3. 尝试其他网络

恢复模式对网络要求较高。

避免：

* 公司 WiFi
* 需要登录的公共网络（Captive Portal）
* VPN
* 受过滤的网络

尝试：

* 手机热点
* 家用路由器的 2.4GHz WiFi

---

## 4. 如果你已抹掉磁盘，检查 GPT/APFS

在恢复模式的终端中：

```bash
diskutil list
```

你应该看到类似：

```
/dev/disk0
   GUID_partition_scheme
   Apple_APFS Container
```

如果没有：

```bash
diskutil eraseDisk APFS "Macintosh HD" GPT /dev/disk0
```

然后重新安装。

---

## 5. 针对你的情况的最佳方法：制作 macOS USB 安装器

既然你已经拥有 Linux/Ubuntu 并且可以写入 USB，这或许更简单。

从 Apple 下载 macOS 安装器：

示例：

```
安装 macOS Monterey.app
```

创建 USB：

```bash
sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia \
--volume /Volumes/MyUSB
```

启动时按住：

```
Option (⌥)
```

选择 USB 安装器。

---

对于你的具体情况：

* 2017 款 MacBook Pro
* 已安装 Ubuntu
* 希望通过 Boot Camp 安装 Windows 10

我会建议：

```
1. 修复 macOS 恢复
        |
        v
2. 安装 macOS
        |
        v
3. Boot Camp 助理
        |
        v
4. Windows 10 22H2
```

不要直接安装 Windows。如果先恢复 macOS，通过 Apple 固件 + Boot Camp 驱动的路径会简单得多。
