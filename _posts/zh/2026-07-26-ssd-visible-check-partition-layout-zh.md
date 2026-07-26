---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSD可见，检查分区布局
translated: true
type: note
---

问题：`diskpart list disk` 显示磁盘 0（476GB）和 USB 磁盘 1（14GB）。这能确认 VMD/RST 问题吗？

回答：

这个结果实际上很有用：

```
Disk ###  Status   Size
------------------------
Disk 0   Online    476 GB
Disk 1   Online     14 GB
```

结论：

✅ NVMe SSD 在 Windows PE 中可见  
✅ USB 安装盘可见  
✅ 存储控制器并未完全隐藏磁盘  

因此，**这不是经典的“Windows 安装程序无法识别 SSD 因 VMD 驱动缺失”的情况**。

VMD 理论的可能性降低。

---

下一步需要检查分区布局。

运行以下命令：

```cmd
diskpart

select disk 0

list partition

list volume
```

发送截图。

---

结合你之前的日志：

```
Setup Phase: [4]
0xC19001F4
```

以及现在：

```
Disk 0 可见
```

我的怀疑转向：

### 1. 旧的 GPT/EFI 分区元数据（可能性最高）

你之前的错误：

```
partition is of an unrecognized type
volume is offline
```

强烈指向此问题。

如果是全新安装且不需要保留现有数据，请执行：

```cmd
diskpart

select disk 0

clean

convert gpt

exit
```

然后在 Windows 安装程序中点击刷新并安装。

这将重新创建以下分区：

```
EFI       FAT32    ~100MB
MSR       16MB
Windows   NTFS
Recovery  ~1GB
```

---

### 2. 检查 BIOS 启动模式

在 BIOS 中：

```
Boot Mode: UEFI
Legacy Boot: Disabled
CSM: Disabled
Secure Boot: 临时禁用
```

Windows 11 要求 UEFI + GPT。

---

### 3. 另一个有用的检查

运行：

```cmd
diskpart

select disk 0

detail disk
```

查看以下信息：

```
Partition Style : GPT
```

或：

```
Dynamic Disk : Yes
```

如果显示为动态磁盘，即可解释之前的“无法识别的类型”问题。

---

目前我**不再建议追究 VMD 问题**。SSD 的可见性证明安装程序能够与存储设备通信。我会先检查 `list partition`，然后很可能执行 GPT 全新安装。