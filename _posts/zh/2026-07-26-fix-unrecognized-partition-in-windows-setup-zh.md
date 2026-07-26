---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Windows安装中无法识别的分区
translated: true
type: note
---

**问题：Windows 11 安装程序显示“分区类型无法识别”/“所选卷处于脱机状态”——该怎么办？**

这通常是因为目标 SSD 存在旧分区布局、RAID 元数据、动态磁盘状态或残留的 OEM/Linux 分区。如果**不需要保留此磁盘上的任何数据**，最干净的解决方法是擦除并重新创建 Windows 分区。

### 方法 1（推荐用于全新 Windows 安装）

⚠️ 此操作会删除目标磁盘上的所有内容。

在 Windows 安装界面：

1. 按下：

```
Shift + F10
```

2. 打开 diskpart：

```cmd
diskpart
```

3. 找到你的磁盘：

```cmd
list disk
```

示例：

```
Disk 0   1000 GB
Disk 1    512 GB
```

识别你的 Lenovo SSD。

4. 选择它：

```cmd
select disk 1
```

验证：

```cmd
detail disk
```

确保这是正确的 SSD。

5. 擦除分区信息：

```cmd
clean
```

6. 创建 GPT 分区：

```cmd
convert gpt
exit
```

关闭命令提示符。

7. 回到 Windows 安装界面：

* 点击**刷新**
* 选择未分配空间
* 点击**下一步**

Windows 将自动创建：

```
EFI 系统分区
MSR 分区
Windows 分区
恢复分区
```

---

### 如果 `clean` 因磁盘脱机而失败

运行：

```cmd
diskpart

list disk
select disk 1

attributes disk
```

如果看到：

```
Current Read-only State: Yes
```

则执行：

```cmd
attributes disk clear readonly
online disk
```

重试：

```cmd
clean
```

---

### 如果磁盘未被正确识别

首先检查 BIOS。

对于 Lenovo 小新：

进入 BIOS：

```
F2
```

查找：

```
Storage Controller Mode
```

可能选项：

```
RAID
AHCI
```

对于简单的 Windows 安装：

```
AHCI
```

更简单。

但是，如果现有 Windows 安装重要，请**不要**随意切换 RAID/AHCI。对于全新安装，AHCI 通常没问题。

---

### 如果磁盘上有重要数据

**不要**运行：

```cmd
clean
```

而应：

```cmd
diskpart

list disk
select disk X
detail disk
```

检查其中是否包含你的文件。

你可以启动 Linux live USB 并检查：

```bash
lsblk
sudo fdisk -l
```

---

针对你的情况（Lenovo 小新全新安装 Windows），我会这样做：

```
Shift + F10
↓
diskpart
↓
list disk
↓
选择 SSD
↓
clean
↓
convert gpt
↓
安装 Windows 11 Pro
```

这是最快且最可靠的路径。