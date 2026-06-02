---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux xz 命令指南
translated: true
type: note
---

问题：如何在 Linux 中使用 `xz` 命令？

答案：

## 概述

`xz` 是 Linux 上流行的压缩工具之一。它只能压缩单个文件。`xz` 被认为比 `bzip2` 和 `gzip` 压缩工具更快。其原生文件格式是 `.xz`。

---

## 基本语法

```
xz [options] [file(s)]
```

---

## 常见操作

### 1. 压缩文件

```bash
xz filename.txt
```

这会压缩文件并用 `.xz` 版本替换它（例如，`filename.txt.xz`）。

您也可以使用显式的压缩标志：

```bash
xz -z filename.txt
```

---

### 2. 解压文件

```bash
xz -d filename.txt.xz
```

这会在当前工作目录中生成原始文件（例如，`filename.txt`）。

您也可以使用 `unxz` 命令，它是等效的：

```bash
unxz filename.txt.xz
```

---

### 3. 保留原始文件

默认情况下，`xz` 在压缩后会删除原始文件。要保留原始文件，请使用 `-k`（keep）选项。

```bash
xz -k filename.txt
```

---

### 4. 设置压缩级别

`xz` 有 0 到 9 的不同压缩级别。数字越高，压缩率越高，节省的空间越多，但会增加内存和 CPU 使用。

```bash
xz -1 filename.txt   # 最快，压缩率最低
xz -6 filename.txt   # 默认级别
xz -9 filename.txt   # 最佳压缩，最慢
```

级别 0 (`--fast`) 提供最快的压缩，但压缩率较低。级别 9 (`--best`) 产生最大压缩，但需要更多时间和系统资源。

---

### 5. 查看压缩信息

```bash
xz -l filename.txt.xz
```

您可以使用 `-l` 选项获取任何压缩文件的详细信息，它会显示原始大小、压缩大小和压缩比率。

---

### 6. 测试压缩文件的完整性

```bash
xz -t filename.txt.xz
```

`-t` 或 `--test` 选项测试压缩文件的完整性。如果文件不是有效的 `.xz` 文件，它会显示错误。如果文件有效，则不会输出（除非同时使用 `-v`）。

---

### 7. 详细输出 / 进度

```bash
xz -v filename.txt
```

详细模式会监控压缩或解压操作的进度，并可以使用 `-v` 选项启用。

---

### 8. 不解压查看文件内容

```bash
xzcat filename.txt.xz
```

`xzcat` 命令显示压缩文件的内容，但不会实际在磁盘上解压文件。

---

### 9. 将多个文件压缩成 `.tar.xz` 存档

由于 `xz` 只能压缩单个文件，要将多个文件压缩成单个 `.xz` 存档，必须使用 `tar` 命令并带 `-J` 选项。

```bash
tar -cJf archive.tar.xz file1.txt file2.txt
```

解压：

```bash
tar -xJf archive.tar.xz
```

---

### 10. 多线程压缩

与 gzip 不同，`xz` 直接支持多线程，可以加速压缩。

```bash
xz -T4 filename.txt    # 使用 4 个线程
xz -T0 filename.txt    # 使用所有可用 CPU 核心
```

---

## 快速参考表

| 选项 | 描述 |
|--------|-------------|
| `-z` | 压缩（默认） |
| `-d` | 解压 |
| `-k` | 保留原始文件 |
| `-t` | 测试完整性 |
| `-v` | 详细输出/进度 |
| `-l` | 列出存档信息 |
| `-0` to `-9` | 压缩级别 |
| `-T[n]` | 使用 n 个线程 |
| `-c` | 写入 stdout |

---

## 限制

`xz` 的一个主要限制是它只能压缩文件，不能压缩文件夹。它也不能创建密码保护的压缩文件。对于目录，请使用 `tar`；对于密码保护，请使用 `rar` 或 `zip`。

参考资料：

- [GoLinuxCloud – xz command examples](https://www.golinuxcloud.com/xz-commandin-linux/)
- [HowtoForge – Linux xz Command Tutorial](https://www.howtoforge.com/linux-xz-command/)
- [Baeldung – Using xz Compression in Linux](https://www.baeldung.com/linux/xz-compression)
- [GeeksforGeeks – XZ Tool in Linux](https://www.geeksforgeeks.org/linux-unix/xz-lossless-data-compression-tool-in-linux-with-examples/)
- [LinuxConfig – Beginner's Guide to xz](https://linuxconfig.org/beginner-s-guide-to-compression-with-xz-on-linux)
