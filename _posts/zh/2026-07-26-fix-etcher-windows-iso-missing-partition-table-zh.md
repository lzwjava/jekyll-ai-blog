---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Etcher中Windows ISO缺少分区表的问题
translated: true
type: note
---

问题：为什么在 Mac 上使用 balenaEtcher 刷写 `Win11_25H2_English_x64_v2.iso` 时显示“缺少分区表”，应该怎么办？

答案：

这是因为 **Windows ISO 文件不是混合启动镜像**。

Etcher 主要针对以下类型的镜像设计：

* Ubuntu ISO
* Debian ISO
* Raspberry Pi 镜像

这些镜像内部包含分区表：

```
ISO
 |
 +-- GPT/MBR 分区表
 |
 +-- EFI 分区
 |
 +-- 文件系统
```

Windows ISO 则不同：

```
Windows ISO
 |
 +-- 启动文件
 +-- sources/install.wim
 +-- setup.exe
```

它是一个安装 DVD 镜像，而不是原始磁盘镜像。

因此 Etcher 会看到：

```
未找到分区表
```

并给出警告。

---

## 能否继续刷写？

你可以点击：

```
继续
```

但对于 Windows 安装 U 盘来说，**这不是推荐的做法**。

结果可能是：

* U 盘在 BIOS 中可见但无法启动
* 联想小新显示：

```
没有可启动设备
```

* UEFI 无法找到 Windows 安装程序

---

## 在 Mac 上更好的方法：使用 `wimlib`（推荐）

对于 Windows 11 25H2 ISO：

```
Win11_25H2_English_x64_v2.iso
```

请按以下步骤操作：

### 1. 安装工具

```bash
brew install wimlib
```

---

### 2. 格式化 U 盘

查找 U 盘：

```bash
diskutil list
```

示例：

```
/dev/disk2
```

擦除：

```bash
diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk2
```

---

### 3. 挂载 ISO

双击：

```
Win11_25H2_English_x64_v2.iso
```

示例：

```
/Volumes/CCCOMA_X64FRE_EN-US_DV9
```

---

### 4. 复制文件

复制除 `install.wim` 以外的所有内容：

```bash
cp -av /Volumes/CCCOMA_X64FRE_EN-US_DV9/* /Volumes/WIN11/
```

删除大文件：

```bash
rm /Volumes/WIN11/sources/install.wim
```

---

### 5. 拆分 install.wim

```bash
wimlib-imagex split \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
/Volumes/WIN11/sources/install.swm \
3800
```

结果：

```
install.swm
install2.swm
install3.swm
```

---

现在 U 盘结构如下：

```
USB
 |
 +-- EFI
 |
 +-- boot
 |
 +-- setup.exe
 |
 +-- sources
       |
       +-- install.swm
       +-- install2.swm
```

这正是 Windows 安装程序所期望的。

---

## 另一个更简单的 GUI 选项

使用：

[Rufus 官方网站](https://rufus.ie/?utm_source=chatgpt.com)

但 Rufus 只能在 Windows 上运行。

如果你能访问自己的 Ubuntu/MacBook 并运行 Windows 虚拟机，Rufus 可能是最简单的方法。

---

针对你的配置：

```
MacBook Pro 2017
        |
        | 制作 U 盘
        v
联想小新 UEFI 笔记本
        |
        v
Windows 11 25H2
```

我**不建议使用 Etcher 处理这个 ISO**。请使用 `wimlib` 方法。这与微软为 UEFI Windows 安装介质所采用的方式相同。