---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 合并多部分RAR文件
translated: true
type: note
---

**问题：如何将多部分RAR文件（part1.rar、part2.rar）合并成一个单个存档？**

**答案：**

多部分RAR文件在设计上会自动一起解压——您无需事先手动"合并"它们。具体操作如下：

**方法一：直接解压（推荐）**
只需打开或解压 `part1.rar`——RAR工具会自动拉取 `part2.rar` 并重组原始文件。

```bash
# 使用 unrar（Linux/macOS）
unrar x part1.rar

# 使用 rar
rar e part1.rar
```

**方法二：通过 CLI 合并为单个 RAR**
```bash
# 步骤1：解压
unrar x part1.rar ./output/

# 步骤2：重新打包成一个存档
rar a combined.rar ./output/*
```

**方法三：使用 WinRAR（Windows 图形界面）**
1. 右键点击 `part1.rar`
2. 选择 **"解压到当前文件夹"** 或 **"解压到指定文件夹"**
3. WinRAR 会自动读取所有分卷

> ⚠️ **重要提示：** 所有分卷（`part1.rar`、`part2.rar` 等）在解压前必须位于 **同一文件夹** 中。

**需注意的命名约定：**

| 旧格式 | 新格式 |
|---|---|
| `archive.part1.rar` | `archive.part1.rar` |
| `archive.r00`、`archive.r01` | `archive.part2.rar` |

参考链接：
- [RAR 和 WinRAR 官方文档](https://www.win-rar.com/documentation.html)
- [unrar 手册页](https://linux.die.net/man/1/unrar)