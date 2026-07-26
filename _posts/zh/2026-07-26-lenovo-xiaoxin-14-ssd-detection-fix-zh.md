---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想小新14 SSD检测修复
translated: true
type: note
---

问题：**联想小新14在安装Windows 11时是否存在Intel VMD/RST SSD检测问题？**

回答：

是的，**联想小新14（小新 14）** 是可能出现此问题的型号之一，尤其是较新的Intel CPU版本（12代/13代/14代）。你的U盘准备工作很可能没问题——接下来要检查的是**存储控制器模式**。

典型流程：

1. 以UEFI模式启动U盘：

```
EFI/BOOT/BOOTX64.EFI
```

正确 ✅

2. 启动Windows 11安装程序。

3. 在磁盘选择页面：

### 情况A — SSD出现

```
Drive 0 Unallocated Space
```

然后正常继续。

### 情况B — “我们找不到任何驱动器”

或仅显示U盘：

这通常是Intel VMD/RST问题。

你需要Intel存储驱动程序：

```
Intel Rapid Storage Technology (Intel RST)
F6 Driver
```

解压后放到另一个U盘上：

示例：

```
USB/
 └── f6vmdflpy-x64/
      ├── iaStorVD.inf
      ├── iaStorAC.inf
      └── drivers...
```

Windows安装程序：

```
你想将Windows安装在哪里？
        ↓
加载驱动程序
        ↓
浏览U盘
        ↓
选择 iaStorVD.inf
```

然后SSD应该就会出现。

---

对于联想小新14，还可以检查BIOS：

进入BIOS：

```
关机
反复按F2
```

查找：

```
Configuration
  └── Storage Controller Mode
```

可能的选项：

```
[AHCI]
[RAID / RST]
```

如果可用：

```
RAID/RST → AHCI
```

这样更简单，因为Windows自带NVMe驱动程序。

但部分联想消费级BIOS会隐藏此选项，此时F6驱动程序才是正确的解决方案。

---

你也可以在安装前确认：

在Windows安装界面按：

```
Shift + F10
```

然后：

```cmd
diskpart

list disk
```

如果看到：

```
Disk 0  512 GB
```

或

```
Disk 0  1 TB
```

则SSD已被检测到。

如果仅显示：

```
Disk 1  USB
```

则肯定是VMD/RST问题。

---

针对你的具体情况：

* USB EFI：✅ 正常
* FAT32 + 拆分install.wim：✅ 正常
* 联想小新14：如果SSD缺失，很可能是VMD/RST问题
* 无需重新制作U盘

下一步诊断只需：**启动U盘，然后告诉我“你想将Windows安装在哪里？”屏幕上显示的内容。**