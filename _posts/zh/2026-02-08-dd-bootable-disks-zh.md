---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 掌握用于制作启动盘的 dd 命令
translated: true
type: note
---

**Question: 请全面介绍 dd 命令的选项，以及用于创建启动盘的命令。**

**Answer:**

### 什么是 `dd`？

`dd` 是一个非常强大的底层 Unix/Linux 工具，用于 **copying and converting data**。它以 block 的形式从输入文件（或设备）读取并写入到输出文件（或设备），通常用于：

- 从 ISO images 创建启动 USB 驱动器
- Disk/partition 克隆和镜像（imaging）
- 创建/还原 disk images
- 安全擦除磁盘数据
- 在格式之间转换（endianness, block size 等）

**基本语法**

```bash
dd if=INPUT of=OUTPUT [options]
```

- `if` = input file（或设备）
- `of` = output file（或设备）

**最重要且常用的选项**

| 选项 | 含义 | 示例值 | 对启动 USB 非常有用？ |
|---------------------|----------------------------------------------|--------------------------|-------------------------------|
| `if=`               | input file / device                          | `/dev/sdb`, `ubuntu.iso` | 是 |
| `of=`               | output file / device                         | `/dev/sdc`, `backup.img` | 是 |
| `bs=`               | block size (一次性 read + write 的大小)       | `4M`, `1M`, `64K`        | 是 – 强烈推荐 |
| `status=progress`   | 在拷贝时显示进度                              | `status=progress`        | 是 – 非常方便 |
| `conv=notrunc`      | 不要阶段输出文件                              | —                        | 有时 |
| `conv=fsync`        | 在退出前物理刷新数据到磁盘                     | —                        | 推荐用于 USB |
| `conv=noerror,sync` | 遇到读取错误时继续，用零填充                   | —                        | 对损坏的介质有用 |
| `count=`            | 仅拷贝指定数量的 blocks                       | `1000`                   | 很少 |
| `skip=`             | 在 **input** 开始处跳过指定数量的 blocks       | `2048`                   | 有时 (高级用法) |
| `seek=`             | 在 **output** 开始处跳过指定数量的 blocks      | `2048`                   | 很少 |

### 创建启动 USB 的推荐安全方法 (2024–2026 实践)

**现代推荐命令（最可靠的组合）：**

```bash
sudo dd if=ubuntu-24.04-desktop-amd64.iso \
        of=/dev/sdX \
        bs=4M \
        status=progress \
        conv=fsync
```

或者更谨慎的变体：

```bash
sudo dd if=ubuntu-24.04-desktop-amd64.iso \
        of=/dev/sdX \
        bs=4M \
        status=progress \
        oflag=direct,sync \
        conv=fsync
```

**推荐命令中的参数解释**

- `bs=4M`           → 比默认的 512 bytes 快得多
- `status=progress` → 显示已传输的字节数和速度
- `conv=fsync`      → 强制刷新 write cache（对 USB 的可靠性至关重要）
- `oflag=direct`    → 绕过操作系统缓存（有时有助于解决 USB 的异常问题）

### 快速参考 – 最常见的真实场景 `dd` 用法

| 任务 | 命令 (2025 年最流行变体) |
|----------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| 从 ISO 创建启动 USB | `sudo dd if=windows11.iso of=/dev/sdX bs=4M status=progress conv=fsync` |
| 创建 disk image | `sudo dd if=/dev/nvme0n1 of=full-disk-$(date +%F).img bs=128M status=progress` |
| 将镜像还原至磁盘 | `sudo dd if=backup.img of=/dev/sdX bs=4M status=progress conv=fsync` |
| 克隆一个磁盘 → 另一个磁盘 | `sudo dd if=/dev/sda of=/dev/sdb bs=128M status=progress conv=fsync` |
| 安全擦除磁盘 (填零) | `sudo dd if=/dev/zero of=/dev/sdX bs=4M status=progress` |
| 使用随机数据安全擦除 (慢) | `sudo dd if=/dev/urandom of=/dev/sdX bs=4M status=progress` |
| 快速创建 4 GiB 随机文件 | `dd if=/dev/urandom of=trashfile bs=1M count=4096 status=progress` |
| 仅备份设备的前 1 GB | `sudo dd if=/dev/nvme0n1 of=header_backup.img bs=1M count=1024 status=progress` |

### 安全准则 – 运行 `dd` 前必读

1. **反复检查 `of=` 设备**
   → 一个拼写错误 → 你可能会摧毁你的系统 SSD/NVMe

2. 每次执行 `dd` 前的最佳安全序列：

   ```bash
   lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
   # 或者
   sudo fdisk -l
   ```

3. 永远不要在未检查的情况下使用 `/dev/sda`, `/dev/nvme0n1` 等设备名

4. 先卸载目标 USB：

   ```bash
   sudo umount /dev/sdX* 2>/dev/null
   ```

5. 使用 `bs=1M`–`bs=8M` — 在现代 USB 3.0/3.1 驱动器上，数值越大通常越快

### 快速速查表 – 流行 block sizes

- `bs=512`     ← 非常慢 (默认值)
- `bs=4k`      ← 依然很慢
- `bs=1M`      ← 2020–2023 年间不错的默认值
- `bs=4M`      ← 2024–2026 年最流行的选择
- `bs=8M`–`bs=128M` ← 适用于非常快的 USB/SSD → NVMe 克隆

**总结 – 你应该记住的命令模式**

```bash
sudo dd if=input.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

**祝（安全地）dd 愉快！** 😄

**References:**

- 本说明无需外部引用（基于截至 2025–2026 年的标准 Linux 知识和当前最佳实践）
