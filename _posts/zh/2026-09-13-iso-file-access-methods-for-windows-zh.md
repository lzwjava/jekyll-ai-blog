---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows系统的ISO文件访问方法
translated: true
type: note
---

问题：如何在 Windows 中提取/查看 ISO 文件？
答案：

## 方法 1：内置 Mount（Windows 10/11）—— 最简单

无需软件：

1. **右键**点击 `.iso` 文件
2. 点击 **"Mount"**
3. 一个虚拟驱动器出现在 **File Explorer** 中（例如 `D:\`）
4. 自由浏览内容
5. 完成后，右键点击虚拟驱动器 → **"Eject"**

---

## 方法 2：7-Zip —— 提取到文件夹

1. 从 [7-zip.org](https://www.7-zip.org) 下载并安装 **7-Zip**
2. 右键点击 `.iso` 文件
3. 悬停在 **"7-Zip"** → 点击 **"Extract Here"** 或 **"Extract to [folder]"**
4. 完成 —— 所有文件被提取到一个普通文件夹

---

## 方法 3：命令行（PowerShell）

```powershell
# Mount the ISO
Mount-DiskImage -ImagePath "C:\path\to\yourfile.iso"

# Check which drive letter it got
Get-DiskImage -ImagePath "C:\path\to\yourfile.iso" | Get-Volume

# When done, unmount it
Dismount-DiskImage -ImagePath "C:\path\to\yourfile.iso"
```

---

## 选择哪种方法？

| 方法 | 最佳用途 |
| --- | --- |
| Built-in Mount | 快速查看，无需安装 |
| 7-Zip | 永久提取文件到磁盘 |
| PowerShell | 自动化/脚本操作 |

对于大多数用户，推荐使用 **内置 Mount** —— 快速、免费，且无需额外软件。
