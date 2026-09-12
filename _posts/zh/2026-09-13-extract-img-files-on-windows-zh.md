---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Windows上提取.img文件
translated: true
type: note
---

Question: 如何在 Windows 中提取/检查 `.img` 文件？

Answer:

`.img` 文件类似于 ISO，但种类更多——它们可以是原始磁盘映像、Raspberry Pi 映像或 Android 映像。以下是处理方法：

---

## 方法一：7-Zip —— 最简单的方式
适用于许多 `.img` 文件：
1. 右键点击 `.img` 文件
2. 悬停在 **"7-Zip"** → **"提取到此处"**
3. ✅ 完成——如果格式受支持

> ⚠️ 7-Zip 可能 **无法** 处理原始磁盘映像（例如 Raspberry Pi `.img`）

---

## 方法二：OSFMount —— 原始磁盘映像的最佳选择
将 `.img` 挂载为虚拟驱动器，如同挂载 ISO 一样：
1. 从 [osforensics.com](https://www.osforensics.com/tools/mount-disk-images.html) 下载 **OSFMount**
2. 打开 OSFMount → **"Mount New"**
3. 选择你的 `.img` 文件
4. 挑选映像中的 **分区**
5. 文件资源管理器中出现驱动器盘符——自由浏览

---

## 方法三：PowerShell（Windows 10/11）
适用于标准磁盘映像的 `.img` 文件：
```powershell
# 与挂载 ISO 相同
Mount-DiskImage -ImagePath "C:\path\to\yourfile.img"

# 完成后卸载
Dismount-DiskImage -ImagePath "C:\path\to\yourfile.img"
```

---

## 方法四：WSL（适用于 Linux 的 Windows 子系统）
非常适合基于 Linux 的 `.img` 文件（如 Raspberry Pi）：
```bash
# 在 WSL 终端中
sudo mkdir /mnt/imgfile
sudo mount -o loop yourfile.img /mnt/imgfile
ls /mnt/imgfile
```

---

## 该使用哪个工具？

| `.img` 类型 | 最佳工具 |
|---|---|
| 通用存档 | 7-Zip |
| 原始磁盘 / Raspberry Pi | OSFMount 或 WSL |
| Windows 磁盘映像 | PowerShell `Mount-DiskImage` |
| Android 系统映像 | Android SDK 工具 |

对于 **Raspberry Pi** 或 **Linux** 的 `.img` 文件，**OSFMount** 是 Windows 上最用户友好的选择。