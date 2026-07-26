---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 专业版与家庭版非安装问题
translated: true
type: note
---

问题：**选择 Windows 11 专业版而非 Windows 11 家庭版是否会导致 Windows 11 安装失败？**

答案：**几乎可以肯定地说不会。** 选择 **Windows 11 专业版** 而非 **Windows 11 家庭版** 并不是安装失败的原因。

版本选择发生在安装程序已经完成以下步骤**之后**：

1. 从 USB 启动
2. 加载 Windows PE（`boot.wim`）
3. 检测 CPU/内存/UEFI
4. 检测到 SSD
5. 开始分区/复制文件

如果版本选择是问题所在，失败通常会发生在稍后的**激活**阶段，而不是在磁盘选择或安装过程中。

针对你的联想小新案例，根据之前的症状：

* ✅ USB 可启动
* ✅ EFI 引导加载器存在
* ✅ 安装程序能识别 512GB SSD
* ❌ 磁盘/分区/脱机/无法识别卷方面出现问题

可能的原因如下：

### 1. Intel VMD / RST 存储模式（最可能的原因）

许多联想笔记本默认启用 Intel VMD。

Windows 安装程序可能能看到 SSD，但由于缺少 Intel 存储驱动程序而无法正常安装。

检查 BIOS：

```
BIOS
 └── Configuration
      └── Intel VMD Controller
```

如果可用：

```
Intel VMD Controller: Disabled
```

然后重新安装。

---

### 2. 现有 GPT/分区元数据损坏

在 Windows 安装程序中，按：

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

然后点击：

```
刷新
→ 选择未分配空间
→ 下一步
```

⚠️ `clean` 命令会销毁 SSD 上的所有数据。

---

### 3. Windows 11 硬件要求问题

可能性较小，因为安装程序已经加载。

检查：

* TPM 2.0
* 安全启动
* UEFI 模式

---

### 版本对比测试

如果你想排除这个因素，可以创建一个包含相同 ISO 的新 USB 并强制安装家庭版：

```bash
dism /Get-WimInfo /WimFile:sources/install.wim
```

你会看到：

```
索引 1 Windows 11 家庭版
索引 6 Windows 11 专业版
```

但我不会在这里浪费时间。版本不是你的障碍。

对于联想小新，我建议重点关注 **VMD/RST 驱动或清除 SSD 的 GPT 布局**。