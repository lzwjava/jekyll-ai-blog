---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MODS支持的操作系统
translated: true
type: note
---

以下是 MODS 运行环境的完整说明：

## MODS 支持的操作系统

根据文档（第 1.0 节）：

| OS | 状态 |
| --- | --- |
| **Linux**（内核 ≥ 2.6.18） | ✅ 主要平台 |
| **Microsoft Windows 7** | ✅ 支持 |
| **Mac OS X**（仅 x86，不包含 PowerPC） | ✅ 支持 |
| **DOS** | ❌ 自 R290 起已停止支持 |

## 针对 Linux 的两种方法

### 选项 1：NVIDIA 的 Turnkey Tiny Linux 镜像（推荐）

NVIDIA 分发一个**自定义 Linux 磁盘镜像**（可放入**64 MB USB 驱动器**）。这是预期的生产环境方法：

- 从 U 盘启动，进入极简 Linux 环境
- 启动时自动运行 MODS
- 无需编译内核模块或配置驱动程序
- 使用 **squashfs 压缩文件系统**，所有内容均已预打包
- 通过 `/mods/args` 和 `/syslinux/commands` 文件进行配置

这就是你提到的 **“tinylinux”** 方案 —— 这是 NVIDIA 提供的在生产环境中运行 MODS 的官方方式。

### 选项 2：在现有 Linux 发行版上运行（例如 Ubuntu）

是的，**Ubuntu 可以运行**，但有一些重要的注意事项：

**要求：**

- 64 位（x86_64）Intel 或 AMD CPU
- **4 GB 及以上系统内存**
- 内核 ≥ **2.6.18**（建议 2.6.29+）
- **glibc 2.5+**
- 内核源码 + 开发工具（`make`、`gcc`）以编译内核模块

**运行前的关键前提条件：**

1. **NVIDIA GPU 必须处于其原始的 VBIOS 初始化状态**
2. **X server 绝对不能运行** —— 你需要先将其停止
3. **nvidia 内核模块必须已卸载** —— `nouveau` 驱动同样如此（将其加入黑名单）
4. **应禁用 Framebuffer 控制台**（在内核参数中设置 `vga=normal`）

**在 Ubuntu/Debian 上的步骤：**

```bash
# 停止 X server
sudo service gdm stop   # 或根据你的 DM 使用 lightdm/kdm

# 卸载 nvidia 驱动
sudo rmmod nvidia

# 将 nouveau 加入黑名单（如果存在）
echo "blacklist nouveau" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf

# 安装 MODS 内核模块
sudo ./install_module.sh --install

# 运行 MODS
sudo ./mods gputest.js -mfg
```

**⚠️ 文档中的警告：**

> *“如果你在已由 nvidia 驱动初始化的 GPU 上运行 MODS，系统可能会变得不稳定”*

## 要点总结

- **用于生产/测试**：使用 NVIDIA 的**自定义 Linux 磁盘镜像**（tinylinux）—— 这是一个干净、最小的启动环境，没有驱动冲突。
- **用于开发/调试**：Ubuntu 也可以正常工作，但你必须确保**没有任何显示驱动先接触 GPU** —— 即没有 X、没有 nvidia.ko、没有 nouveau。MODS 包含其自身的嵌入式 OpenGL/CUDA 驱动和资源管理器，因此它不需要 NVIDIA 显示驱动。

该环境基本上是一个 **“裸机” Linux 系统**，MODS 对 GPU 具有独占访问权。
