---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Etcher 在 Windows USB 上失败的问题
translated: true
type: note
---

问题：Etcher在Mac上烧录Windows 11 ISO时卡住了。如何恢复并创建启动U盘？

回答：

由于你正在烧录：

```text
Win11_25H2_English_x64_v2.iso
```

Etcher卡住是预期行为，因为**Windows ISO并非Etcher适用的磁盘映像**。它可能卡在以下状态：

* "Starting..."
* "Validating..."
* "Flash failed"
* "Preparing..."

请勿长时间等待，直接停止即可。

---

## 1. 退出Etcher

按下：

```text
Cmd + Q
```

如果无法关闭，执行：

```bash
killall balenaEtcher
```

或：

```bash
pkill -f balena
```

---

## 2. 重置U盘

查找你的U盘：

```bash
diskutil list
```

示例：

```text
/dev/disk2 (external, physical)
```

卸载：

```bash
diskutil unmountDisk /dev/disk2
```

擦除：

```bash
diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk2
```

现在U盘已清理干净。

---

## 3. 使用正确的Windows U盘创建方法

在Mac上处理Windows ISO需使用`wimlib`。

安装：

```bash
brew install wimlib
```

挂载ISO：

双击：

```text
Win11_25H2_English_x64_v2.iso
```

检查：

```bash
ls /Volumes
```

你会看到类似：

```text
/Volumes/CCCOMA_X64FRE_EN-US_DV9
```

---

## 4. 复制文件

假设U盘路径为：

```text
/Volumes/WIN11
```

复制：

```bash
cp -av /Volumes/CCCOMA_X64FRE_EN-US_DV9/* /Volumes/WIN11/
```

如果遇到：

```text
File too large
install.wim
```

删除该文件：

```bash
rm /Volumes/WIN11/sources/install.wim
```

然后拆分：

```bash
wimlib-imagex split \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
/Volumes/WIN11/sources/install.swm \
3800
```

---

## 5. 启动联想小新

插入U盘。

开机时按：

```text
F12
```

选择：

```text
UEFI USB
```

Windows安装程序应正常启动。

---

## Etcher失败的原因

Etcher期望的格式：

```
磁盘映像
 |
 +-- GPT
 +-- EFI分区
 +-- 文件系统
```

示例：

```
Ubuntu.iso
      |
      +-- 分区表
      +-- 引导加载程序
```

Windows ISO的格式：

```
Windows.iso
      |
      +-- DVD文件系统
      +-- 安装文件
      +-- install.wim
```

结构不同。

因此对于Windows：

```
Mac
 |
 | wimlib
 v
FAT32 GPT U盘
 |
 v
联想UEFI引导
 |
 v
Windows安装程序
```

是可靠的操作路径。
