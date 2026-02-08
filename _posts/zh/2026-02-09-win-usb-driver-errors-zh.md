---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5.2
title: Windows USB 驱动程序加载错误
translated: true
type: note
---

Question: 为什么在 Lenovo Xiaoxin 14 IAH8 上安装系统时，即使 BIOS 已经设置为 AHCI，Windows 仍然无法从我的 FAT32 USB 中找到/加载驱动程序？

Answer:

这是一个很好的检查点 —— 如果 **AHCI 已经启用**，那么我们可以排除 Intel VMD/RST 作为阻碍因素。在这种情况下，问题**不是 BIOS 存储模式问题**，而是对 **Windows Setup 可以加载什么样的“驱动程序”存在误解**。

以下是针对您情况的**正确根本原因分析**。

---

## 1. Windows Setup 完全不加载 `.exe` 文件

这是关键点。

在安装过程中，Windows Setup：

* **无法执行 `.exe` 安装程序**
* **仅扫描 `.inf` 驱动定义文件**
* 静默忽略所有其他文件

因此，当您插入一个仅包含如下文件的 USB 时：

* `chipset-KZSC030FLWDYANE0.exe`
* `intelVGA-KZSG0A0FT22GJNE0.exe`
* `audio-*.exe`
* `RTKwlan-*.exe`

Windows Setup 将显示：

* **空列表**
* 或 “未找到已签名的驱动程序”

这是**预期行为**，而不是故障。

> 即使 SSD 是可见的，*Load Driver* 对话框也永远不会显示 `.exe` 文件。

---

## 2. 启用 AHCI 后，通常根本不需要任何驱动程序

重要说明：

* **Windows 10 / 11 已经内置了通用的 NVMe + AHCI 驱动程序**
* 如果 BIOS = **AHCI**
* 且 SSD = **标准 NVMe**
* 那么 **Windows Setup 应该会自动检测到磁盘**

如果磁盘**确实出现了**，那么：

* 您**不需要**加载任何驱动程序
* 直接删除分区并继续安装即可

如果磁盘**没有出现**，那么以下情况之一可能是真实的。

---

## 3. 为什么 SSD 仍可能不出现（即使在 AHCI 模式下）

### 情况 A — Windows 安装程序版本太旧

如果您使用的是：

* Windows 10 **1809 或更早版本**
* 或者经过深度修改的 ISO

那么 NVMe 支持可能不完整。

**修复方案**

* 使用 **Windows 10 22H2** 或 **Windows 11 23H2+**
* 使用 **Microsoft Media Creation Tool** 或 **Rufus (GPT + UEFI)** 重新制作 USB

---

### 情况 B — 您混淆了“加载驱动程序”与“缺失磁盘”

许多用户会这样做：

* 磁盘 **是可见的**
* 但 Windows 警告：*“Windows cannot be installed to this disk”*
* 用户点击 **Load driver**，以为是缺少驱动程序

实际上，问题在于：

* 分区形式不匹配 (MBR vs GPT)
* 残留的 Intel RAID 元数据
* 或 Secure Boot 残留信息

**修复方案**
在磁盘选择界面：

1. 按下 **Shift + F10**
2. 运行：

   ```
   diskpart
   list disk
   select disk 0
   clean
   convert gpt
   exit
   ```
3. 关闭 CMD → 刷新 → 安装

---

### 情况 C — Secure Boot + 非官方 ISO

如果：

* Secure Boot 已开启
* ISO 是非官方/修改过的

那么 Windows 可能会阻止磁盘访问。

**修复方案**

* 临时禁用 **Secure Boot**
* 安装 Windows
* 稍后重新启用 Secure Boot

---

## 4. 为什么 Lenovo 驱动程序 `.exe` 文件在安装期间无效

Lenovo 驱动程序是为 **安装后 (post-install)** 使用而设计的：

| Driver type | Purpose         | Setup usable? |
| ----------- | --------------- | ------------- |
| Chipset     | Enables devices | ❌             |
| VGA         | Graphics        | ❌             |
| Audio       | Sound           | ❌             |
| WLAN        | Network         | ❌             |
| Camera / FP | Peripherals     | ❌             |

它们：

* 包含安装程序
* 动态解压文件
* 需要 Windows 服务支持

Windows Setup 环境 (**WinPE**) 无法使用它们。

---

## 5. 您现在应该做什么（检查清单）

既然 AHCI 已经设置正确：

1. ✅ **完全忽略 “Load driver” 选项**
2. ✅ 使用 **最新的 Windows ISO**
3. ✅ 删除所有分区 (`diskpart clean`)
4. ✅ 安装到未分配的空间 (unallocated space)
5. ✅ 首次启动后：

   * 安装 Lenovo Vantage
   * 让 Windows Update 推送驱动
   * 然后根据需要手动安装 Lenovo `.exe` 驱动

---

## 总结

* 您的 USB 没问题
* FAT32 是正确的
* BIOS AHCI 是正确的
* **问题在于 `.exe` 驱动程序在 Windows Setup 的定义中不是驱动程序**
* 您几乎肯定 **根本不需要加载任何驱动程序**

如果您愿意，可以告诉我：

* Windows 版本 (10/11 + build)
* SSD 是可见还是不可见
* 具体的错误文本（如果有）

我可以一步到位地为您定位问题。