---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Etcher创建Windows启动U盘
translated: true
type: note
---

问题：如何通过balenaEtcher图形界面方法在Mac上制作Windows安装U盘？

回答：

[balenaEtcher官方网站](https://etcher.balena.io?utm_source=chatgpt.com) 是一款简单易用的图形化工具，可直接将ISO镜像写入U盘。

其原理如下：

```
Windows ISO文件
        |
        v
   balenaEtcher
        |
        v
 USB闪存盘（可启动）
        |
        v
 联想小新启动Windows安装程序
```

无需手动格式化U盘、复制文件、拆分`install.wim`等操作，Etcher直接执行原始镜像写入。

---

## 1. 在macOS上安装balenaEtcher

下载地址：

[balenaEtcher下载页面](https://etcher.balena.io/?utm_source=chatgpt.com)

选择：

```
macOS Intel
```

适用于MacBook Pro 2017。

安装：

```
balenaEtcher.app
```

将其移至：

```
应用程序
```

---

## 2. 下载Windows ISO

示例：

Windows 11 ISO：

[下载Windows 11磁盘映像（ISO）](https://www.microsoft.com/software-download/windows11?utm_source=chatgpt.com)

获取文件：

```
Win11_24H2_English_x64.iso
```

大小：

```
约6GB
```

---

## 3. 插入U盘

要求：

```
USB容量 >= 8GB
建议16GB
```

检查磁盘：

```bash
diskutil list
```

示例：

```
/dev/disk2
   外部物理磁盘
   16GB USB
```

---

## 4. 打开Etcher

您将看到三个步骤：

```
+-----------------------+
| 从文件烧录            |
|                       |
|  Win11.iso            |
+-----------------------+

          ↓

+-----------------------+
| 选择目标              |
|                       |
| USB 16GB              |
+-----------------------+

          ↓

+-----------------------+
| 开始烧录              |
+-----------------------+
```

点击：

```
从文件烧录
```

选择：

```
Win11_24H2_English_x64.iso
```

---

选择U盘：

```
SanDisk 16GB USB
```

然后点击：

```
开始烧录！
```

---

## 5. Etcher的实际操作

在图形界面背后，执行以下流程：

```
打开ISO
       |
       |
       v
写入ISO数据块
       |
       |
       v
USB扇区
```

大致相当于以下命令：

```bash
dd if=windows.iso of=/dev/disk2 bs=4m
```

这会创建一个可启动的U盘布局。

---

## 6. 启动联想小新

插入U盘。

开机时按：

```
Fn + F12
```

或：

```
F12
```

进入启动菜单：

```
UEFI:
   USB存储设备
```

选择该选项。

Windows安装程序将启动。

---

## 重要注意事项：Windows ISO + Etcher

对于Linux ISO，Etcher几乎完美适配。

但对于Windows ISO，存在一个历史问题：

```
Windows ISO
    |
    +-- install.wim
          |
          +-- 有时 >4GB
```

UEFI固件通常要求：

```
FAT32
```

但FAT32无法存储：

```
单个文件 >4GB
```

因此，某些通过Etcher写入的Windows ISO可能无法在某些机器上启动。

对于联想小新（现代UEFI），成功率通常较高，但如果失败，可能出现以下情况：

* 黑屏
* 显示"无启动设备"
* U盘可见但安装程序无法启动

此时请改用`wimlib` FAT32方法。

---

针对您的具体情况：

```
MacBook Pro 2017
        |
        | 制作U盘
        v
联想小新
        |
        v
Windows 11
```

我建议**先尝试Etcher**，因为只需约10分钟。如果联想小新无法启动，再改用`wimlib`方法。
