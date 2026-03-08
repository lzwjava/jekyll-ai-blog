---
audio: false
generated: true
image: false
lang: en
layout: post
title: Xz Command Guide for Linux
translated: false
type: note
---

Question: How do I use the `xz` command in Linux?

Answer:

## Overview

`xz` is one of the popular compression tools for Linux. It only compresses a single file. `xz` is considered to be faster than `bzip2` and `gzip` compression tools. The native file format is `.xz`.

---

## Basic Syntax

```
xz [options] [file(s)]
```

---

## Common Operations

### 1. Compress a File

```bash
xz filename.txt
```

This compresses the file and replaces it with the `.xz` version (e.g., `filename.txt.xz`).

You can also use the explicit compress flag:

```bash
xz -z filename.txt
```

---

### 2. Decompress a File

```bash
xz -d filename.txt.xz
```

This produces the original file (e.g., `filename.txt`) in the current working directory.

You can also use the `unxz` command, which is equivalent:

```bash
unxz filename.txt.xz
```

---

### 3. Keep the Original File

By default, `xz` deletes the original after compression. To retain the original file, use the `-k` (keep) option.

```bash
xz -k filename.txt
```

---

### 4. Set Compression Level

`xz` has different levels of compression, numbered 0 through 9. The higher the number, the more compression and space savings you will receive, but at the cost of increased memory and CPU usage.

```bash
xz -1 filename.txt   # fastest, least compression
xz -6 filename.txt   # default level
xz -9 filename.txt   # best compression, slowest
```

Level 0 (`--fast`) provides the fastest compression with a lower ratio. Level 9 (`--best`) produces maximum compression but requires more time and system resources.

---

### 5. View Compression Info

```bash
xz -l filename.txt.xz
```

You can retrieve information about any compressed file using the `-l` option, which shows the original size, compressed size, and compression ratio.

---

### 6. Test Integrity of a Compressed File

```bash
xz -t filename.txt.xz
```

The `-t` or `--test` option tests the integrity of a compressed file. It displays an error if the file is not a valid `.xz` file. If the file is valid, it prints no output (unless `-v` is also used).

---

### 7. Verbose Output / Progress

```bash
xz -v filename.txt
```

The verbose mode monitors the progress of compression or decompression operations and can be enabled using the `-v` option.

---

### 8. View File Contents Without Decompressing

```bash
xzcat filename.txt.xz
```

The `xzcat` command displays the content of a compressed file but does not actually decompress the file on disk.

---

### 9. Compress Multiple Files into a `.tar.xz` Archive

Since `xz` compresses only a single file, to compress multiple files into a single `.xz` archive, you must use the `tar` command with the `-J` option.

```bash
tar -cJf archive.tar.xz file1.txt file2.txt
```

To decompress:

```bash
tar -xJf archive.tar.xz
```

---

### 10. Multithreaded Compression

Unlike gzip, `xz` supports multithreading directly, which speeds up compression.

```bash
xz -T4 filename.txt    # use 4 threads
xz -T0 filename.txt    # use all available CPU cores
```

---

## Quick Reference Table

| Option | Description |
|--------|-------------|
| `-z` | Compress (default) |
| `-d` | Decompress |
| `-k` | Keep original file |
| `-t` | Test integrity |
| `-v` | Verbose/progress |
| `-l` | List archive info |
| `-0` to `-9` | Compression level |
| `-T[n]` | Use n threads |
| `-c` | Write to stdout |

---

## Limitations

One major limitation of `xz` is that it can only compress files, not folders. It also cannot create password-protected compressed files. Use `tar` for directories and `rar` or `zip` for password protection.

References:

- [GoLinuxCloud – xz command examples](https://www.golinuxcloud.com/xz-commandin-linux/)
- [HowtoForge – Linux xz Command Tutorial](https://www.howtoforge.com/linux-xz-command/)
- [Baeldung – Using xz Compression in Linux](https://www.baeldung.com/linux/xz-compression)
- [GeeksforGeeks – XZ Tool in Linux](https://www.geeksforgeeks.org/linux-unix/xz-lossless-data-compression-tool-in-linux-with-examples/)
- [LinuxConfig – Beginner's Guide to xz](https://linuxconfig.org/beginner-s-guide-to-compression-with-xz-on-linux)