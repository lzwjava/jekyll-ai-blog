---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Mac上创建Windows USB
translated: true
type: note
---

问题：如何在Mac上制作Windows安装U盘，用于在联想小新上安装Windows？

回答：

由于你只有一台 **MacBook**，可以使用 macOS 工具来制作 Windows U盘。最简单的方法**不是使用 Media Creation Tool**（该工具仅限 Windows），而是下载 ISO 并将其写入 U盘。

## 方法 1（推荐）：在 macOS 上使用 `diskutil` + `wimlib`

### 1. 下载 Windows ISO

下载官方 ISO：

* Windows 11 ISO：
  [下载 Windows 11 磁盘映像 (ISO)](https://www.microsoft.com/software-download/windows11?utm_source=chatgpt.com)

* Windows 10 ISO：
  [下载 Windows 10 磁盘映像 (ISO)](https://www.microsoft.com/software-download/windows10ISO?utm_source=chatgpt.com)

选择：

* Windows 11 x64 ISO
* 根据个人偏好选择英文或中文版本

---

### 2. 准备 U盘

插入 U盘（建议 16GB）。

查找磁盘：

```bash
diskutil list
```

示例：

```
/dev/disk2 (external, physical)
```

卸载它：

```bash
diskutil unmountDisk /dev/disk2
```

---

### 3. 安装 `wimlib`

Windows ISO 包含一个文件：

```
sources/install.wim
```

该文件通常大于 4GB。

FAT32 无法存储大于 4GB 的文件，因此需要拆分它。

安装：

```bash
brew install wimlib
```

如果你没有 Homebrew：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### 4. 将 U盘格式化为 FAT32 + GPT

将 `disk2` 替换为你的 U盘：

```bash
diskutil eraseDisk MS-DOS WIN11 GPT /dev/disk2
```

现在挂载 U盘。

---

### 5. 挂载 Windows ISO

双击 ISO 文件。

macOS 会将其挂载，例如：

```
/Volumes/CCCOMA_X64FRE_EN-US_DV9
```

---

### 6. 复制 Windows 文件

复制所有内容：

```bash
cp -av /Volumes/CCCOMA_X64FRE_EN-US_DV9/* /Volumes/WIN11/
```

如果失败于：

```
install.wim too large
```

删除它：

```bash
rm /Volumes/WIN11/sources/install.wim
```

然后拆分它：

```bash
wimlib-imagex split \
/Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim \
/Volumes/WIN11/sources/install.swm \
3800
```

你将得到：

```
install.swm
install2.swm
...
```

Windows 安装程序能够识别这些文件。

---

### 7. 弹出 U盘

```bash
diskutil eject /dev/disk2
```

现在 U盘已制作完成。

---

## 在联想小新上安装

1. 将 U盘插入联想小新
2. 开机
3. 按下：

```
F12
```

（有时是 Fn+F12）

4. 选择：

```
UEFI USB Device
```

5. Windows 安装程序启动。

---

## 联想小新 BIOS 设置

如果 U盘无法启动：

进入 BIOS：

```
F2
```

检查：

```
Boot Mode:
UEFI

Secure Boot:
Disable
```

然后重试。

---

## 另一种更简单的 GUI 方法

你可以使用：

* [balenaEtcher 官方网站](https://etcher.balena.io?utm_source=chatgpt.com)

步骤：

1. 下载 ISO
2. 打开 Etcher
3. 选择 ISO
4. 选择 U盘
5. 开始刷写

不过，对于现代 Windows 10/11 安装 U盘，`wimlib` 方法更可靠，因为它能处理 4GB 的 `install.wim` 文件问题。

对于联想小新（UEFI 笔记本电脑），我建议使用 **GPT + FAT32 + wimlib 拆分**，这与微软的 UEFI 安装路径一致。
