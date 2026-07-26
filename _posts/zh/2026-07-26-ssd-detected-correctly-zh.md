---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 检测到SSD正确
translated: true
type: note
---

问题：**如果 Windows 安装程序在联想小新 14 上显示“磁盘 0 512 GB”，是否意味着 SSD 被正确检测到？**

答案：**是的。** 如果 Windows 安装程序显示：

```
磁盘 0   512 GB
```

那么 SSD 已经被检测到。✅

这意味着：

* ✅ UEFI 从 USB 启动正常
* ✅ Windows PE 已加载
* ✅ 存储控制器驱动程序已加载
* ✅ NVMe SSD 可见
* ❌ Intel VMD/RST 很可能**不是**问题

该 SSD 很可能是内置的 NVMe 驱动器。

剩余的安装失败通常由以下原因引起：

### 1. 分区布局错误 / 旧元数据

在 Windows 安装程序中打开命令提示符：

```
Shift + F10
```

运行：

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

然后刷新磁盘列表并安装。

⚠️ `clean` 会删除磁盘 0 上的所有分区。

对于全新安装 Windows，这通常是正确的做法。

---

### 2. 错误的 Windows 版本 / 损坏的 ISO

你的 ISO：

```
Win11_25H2_English_x64_v2.iso
```

如果来自微软，则是没问题的。

---

### 3. BIOS 安全启动 / TPM 设置

对于小新 14：

BIOS：

```
Security
  Secure Boot: Enabled

TPM:
  Enabled
```

Windows 11 需要这些设置。

---

由于你的 SSD 显示为**磁盘 0 512GB**，我会停止排查 VMD/RST。下一步我会做的是：

```
diskpart
select disk 0
clean
convert gpt
```

然后重新安装。

现在关键问题是：**在选择磁盘 0 并点击“下一步”后，出现什么具体错误？** 这将告诉我们真正的问题所在。
