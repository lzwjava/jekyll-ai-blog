---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ventoy USB安装与ISO复制
translated: true
type: note
---

## 计划 — Ventoy + 烧录 Windows ISO

### 已找到 ISO 文件
```
/home/lzw/Downloads/Win11_25H2_English_x64_v2.iso   (7.9G)
```

### USB 目标
```
/dev/sdb  (14.6G USB)  ← 当前包含旧版 Windows 安装程序
```

### ⚠️ 重要警告

将 Ventoy 安装到 `/dev/sdb` 会**擦除其上的所有内容** — 当前的 EFI 和 WIN11 分区将被销毁。你的旧 USB 内容将全部丢失。

### 分步操作指南

| 步骤 | 操作 | 命令 |
|---|---|---|
| **1** | 下载 Ventoy | `wget https://github.com/ventoy/Ventoy/releases/latest/download/ventoy-1.1.05-linux.tar.gz` |
| **2** | 解压 | `tar xzf ventoy-*.tar.gz && cd ventoy-*` |
| **3** | 确认 USB 为 `/dev/sdb` | `lsblk` |
| **4** | 将 Ventoy 安装到 USB | `sudo ./Ventoy2Disk.sh -i /dev/sdb` |
| **5** | 复制 ISO 文件 | `cp ~/Downloads/Win11_25H2_English_x64_v2.iso /media/$USER/Ventoy/` |
| **6** | 同步并弹出 | `sync` 然后拔下 USB |

执行步骤 4 后，USB 将变为 Ventoy 磁盘。你只需将 ISO 文件复制进去即可 — 无需解压，也无需调整分区。多个 ISO 文件可以共存。

---

**确认要继续吗？** 当前 USB 数据将被清空。