---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Tar 命令精华指南
translated: true
type: note
---

`tar` 命令（“tape archive”的缩写）是一个基础的 Unix/Linux 工具，用于将多个文件和目录捆绑成一个单一的归档文件。以下是详细介绍：

## Basic Concept

Tar 创建的归档文件可以保留文件 permissions（权限）、ownership（所有权）、directory structures（目录结构）和 timestamps（时间戳）。与压缩工具不同，tar 本身并不进行压缩——它只是将文件捆绑在一起。然而，它通常与 gzip 或 bzip2 等压缩工具配合使用。

## Common Usage Patterns

**Creating archives:**

```bash
tar -cvf archive.tar files/          # Create archive
tar -czvf archive.tar.gz files/      # Create + gzip compress
tar -cjvf archive.tar.bz2 files/     # Create + bzip2 compress
```

**Extracting archives:**

```bash
tar -xvf archive.tar                 # Extract
tar -xzvf archive.tar.gz             # Extract gzipped
tar -xjvf archive.tar.bz2            # Extract bzip2'd
tar -xvf archive.tar -C /target/dir  # Extract to specific directory
```

**Viewing contents:**

```bash
tar -tvf archive.tar                 # List files without extracting
tar -tzvf archive.tar.gz             # List files in gzipped archive
```

## Key Options

- **-c**: Create 一个新归档
- **-x**: 从归档中 Extract
- **-t**: List 内容
- **-v**: Verbose（显示正在处理的文件）
- **-f**: 指定 filename（必须是文件名之前的最后一个 flag）
- **-z**: 使用 gzip 压缩 (.tar.gz 或 .tgz)
- **-j**: 使用 bzip2 压缩 (.tar.bz2)
- **-J**: 使用 xz 压缩 (.tar.xz)
- **-C**: 在操作前切换到指定 directory
- **--exclude**: 排除特定的文件或 patterns
- **-p**: Preserve permissions（解压时非常有用）

## Practical Examples

**Backup a directory:**

```bash
tar -czvf backup-$(date +%Y%m%d).tar.gz /home/user/documents/
```

**Extract specific files:**

```bash
tar -xzvf archive.tar.gz file1.txt dir/file2.txt
```

**Exclude certain files:**

```bash
tar -czvf archive.tar.gz --exclude='*.log' --exclude='node_modules' project/
```

**Extract to different location:**

```bash
tar -xzvf archive.tar.gz -C /opt/extracted/
```

**View file before extracting:**

```bash
tar -tzvf archive.tar.gz | grep specific-file
```

## Modern Simplification

现代版本的 tar 可以自动检测压缩格式，因此你通常可以省略压缩 flag：

```bash
tar -xvf archive.tar.gz    # Auto-detects gzip
tar -xvf archive.tar.bz2   # Auto-detects bzip2
```

## Common Gotchas

在使用 `-f` 时，选项的顺序非常重要。文件名必须紧跟在 `-f` 之后，因此 `tar -cvzf archive.tar.gz files/` 是有效的，但 `tar -cvfz archive.tar.gz files/` 可能会报错。

解压时，tar 会保留原始的目录结构。如果归档中包含 `folder/file.txt`，它将创建该目录结构，而不仅仅是将 `file.txt` 提取到当前目录。