---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ventoy Windows 11 常规模式选择
translated: true
type: note
---

问题：**在Ventoy中选择Windows 11 ISO后，应选择哪个选项：正常模式、WIMBOOT模式还是文件校验？**

回答：

对于正常的Windows 11安装U盘，请选择：

```
正常模式启动
```

这是默认且推荐的选项。

### Ventoy菜单说明

#### 1. 正常模式启动 ✅（选择此项）

流程：

```
UEFI BIOS
    ↓
Ventoy
    ↓
Windows 11 ISO
    ↓
Windows 安装程序
```

Ventoy将ISO映射为虚拟DVD光驱。Windows安装程序正常读取：

```
boot.wim
install.wim
```

适用于：

* 联想小新
* Windows 11纯净安装
* 大多数UEFI电脑

---

#### 2. WIMBOOT模式启动

请**不要**优先选择此项。

WIMBOOT模式是一种兼容性回退方案。它以不同方式提取/启动Windows WIM文件。

仅当以下情况时使用：

* 正常模式失败
* Windows安装程序无法找到文件
* 部分旧固件存在ISO加载问题

对于现代UEFI笔记本，正常模式效果更佳。

---

#### 3. 文件校验

这仅是一个验证工具。

它会计算类似：

```
SHA256：
xxxxxxxxxxxxxxxx
```

的内容，用于检查ISO文件是否损坏。

如果您怀疑以下情况，可在安装前使用：

* 下载中断
* ISO拷贝损坏
* ISO被修改

此模式不会启动Windows。

---

针对您的联想小新：

请选择：

```
Ventoy
 └── Win11_25H2_English_x64_v2.iso
       └── 正常模式启动  ← 选择此项
```

随后Windows安装程序应正常显示。

若进入磁盘选择界面时看到：

```
驱动器0 512GB
```

则表示SSD已被正常识别。剩余问题通常涉及分区/删除/安装操作，而非U盘制作环节。
