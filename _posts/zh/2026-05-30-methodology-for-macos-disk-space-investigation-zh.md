---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS磁盘空间调查方法论
translated: true
type: note
---

以下是该方法的步骤说明：

## 1. 从宏观入手 — 查看磁盘空间状况

```bash
df -h /
```

显示总磁盘、已用和可用空间。这能告诉你问题的紧急程度，并建立一个衡量基准。

## 2. 扫描主目录顶层

```bash
du -sh ~/* ~/.* 2>/dev/null | sort -rh | head -20
```

`du -sh` = 磁盘用量，汇总显示，人类可读格式。这能揭示哪些顶层目录占用最大——通常是 `~/Library`、`~/projects`、`~/.cargo` 等。接下来你需要深入分析这些最大的目录。

## 3. 已知的 macOS 热点区域

这些是 macOS 上通常堆积垃圾文件的位置。逐一检查：

```bash
# 应用缓存（可安全删除，应用会自动重建）
du -sh ~/Library/Caches/* 2>/dev/null | sort -rh | head -20

# 应用日志
du -sh ~/Library/Logs/* 2>/dev/null | sort -rh | head -10

# Docker 虚拟机镜像（即使 Docker 未运行也可能占用巨大空间）
du -sh ~/Library/Containers/com.docker.docker 2>/dev/null

# Homebrew 已安装包及缓存下载
du -sh /opt/homebrew 2>/dev/null
du -sh /opt/homebrew/Cellar/* 2>/dev/null | sort -rh | head -10
du -sh ~/Library/Caches/Homebrew/downloads/* 2>/dev/null | sort -rh | head -5

# 编程语言相关缓存
du -sh ~/.npm ~/.yarn ~/.bun ~/.cargo ~/.rustup 2>/dev/null | sort -rh
du -sh ~/Library/Caches/pip 2>/dev/null

# JetBrains IDE（缓存及应用支持文件）
du -sh ~/Library/Caches/JetBrains 2>/dev/null
du -sh ~/Library/Application\ Support/JetBrains 2>/dev/null

# Xcode
du -sh ~/Library/Developer/Xcode/* 2>/dev/null | sort -rh
```

核心模式：`du -sh <路径>/* | sort -rh | head -N` — 列出所有子项，按大小降序排列，显示前 N 个。

## 4. 项目构建产物（通常占用最大）

```bash
# Rust target 目录 — 体积巨大，可重建
du -sh ~/projects/*/target 2>/dev/null | sort -rh

# Node modules
du -sh ~/projects/*/node_modules 2>/dev/null | sort -rh
```

这些是开发者的头号空间占用大户。一次 `cargo build` 就能在 `target/` 目录产生 5-27GB 的数据。

## 5. 查找近期修改的大文件

```bash
find ~ -type f -size +100M -mtime -7 2>/dev/null
```

这能捕获正在持续增长的文件——体积超过 100MB 且在最近 7 天内被修改过。如果磁盘空间持续增长，运行此命令并观察规律（同一文件不断变大，或同一目录不断出现新文件）。

## 6. 监控实时写入（如果空间仍在增长）

```bash
sudo fs_usage -w -f disk 2>/dev/null | head -50
```

这是 macOS 特有的工具，可实时监控文件系统活动。能精确显示是哪个进程在写入哪个文件。当你无法确定是什么在吞噬空间时特别有用。

## 操作模式总结

```
df -h                          # 情况有多严重？
du -sh ~/* | sort -rh          # 大目录在哪里？
du -sh <大目录>/* | sort -rh   # 深入分析每个大目录
find ~ -size +100M -mtime -7   # 最近什么东西在增长？
fs_usage                       # 当前正在写入什么？
```

核心就是反复执行 `du -sh | sort -rh`，从最大目录逐层向下分析，结合对 macOS 和开发工具垃圾存储位置的领域知识。
