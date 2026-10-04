---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 未连接USB驱动器
translated: true
type: note
---

**不——那不是你的 U 盘。** ❌

`/dev/disk10` 是一个名为“iOS 26.3.1 Simulator”（17.8 GB）的**虚拟磁盘映像**。这是一个模拟器文件，并非硬件。disk4、disk6、disk8 同理。

当前这台机器上的物理磁盘：

| 设备 | 类型 |
|---|---|
| `/dev/disk0` | 内置、物理（500 GB SSD）⛔ 切勿触碰 |
| disk4/6/8/10 | 磁盘映像（iOS 模拟器）🎭 非真实设备 |

**你的 U 盘仍未接入。** 自上次检查以来，没有出现新设备。

如需自行确认，请运行：

```bash
diskutil list
```

真正的 U 盘会显示为如下格式：

```
/dev/diskX (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     GUID_partition_scheme                        *7.9 GB     diskX
   1:       Microsoft Basic Data Untitled                7.9 GB     diskXs1
```

📌 注意：`diskutil list | grep -i external` 未显示任何结果，因为唯一的物理磁盘是内置的——`diskutil list external` 也并未输出硬件行。

**操作步骤：**
1. 将 U 盘物理插入 Mac
2. 再次运行 `diskutil list` 并将输出粘贴至此
3. 然后我们使用 `dd` 进行烧录

如果 U 盘已插入，请尝试其他端口，或通过 `ioreg`/系统信息 → USB 检查 macOS 是否能检测到它。