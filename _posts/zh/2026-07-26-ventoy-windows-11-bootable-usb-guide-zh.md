---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ventoy Windows 11 可启动U盘指南
translated: true
type: note
---

## 综合总结：Windows 11 可启动 U 盘 — Ventoy 方法

### 1. 环境分析

首先，我扫描了系统以了解当前状态：

| 检查项 | 结果 |
| --- | --- |
| **U 盘设备** | `/dev/sdb` — 检测到 14.6G USB 磁盘 |
| **现有分区** | `/dev/sdb1`（200M，VFAT，EFI）+ `/dev/sdb2`（14.5G，VFAT，WIN11） |
| **现有内容** | 已存在 Windows 11 安装程序 — 通过手动 FAT32 + `wimsplit`（方法 3）制作 |
| **ISO 文件** | `~/Downloads/Win11_25H2_English_x64_v2.iso`（7.9G） |
| **Ventoy 是否已安装？** | **否** — 系统上未安装 |

### 2. 决策：为何仍使用 Ventoy

现有 U 盘已经可启动（EFI 分区 + 分割的 `install.swm` 文件）。然而，用户明确要求使用 Ventoy。使用 Ventoy 重新制作的关键优势：

- **无 4GB FAT32 限制** — Ventoy 使用 exFAT，因此 `install.wim` 保持完整（无需分割）
- **多 ISO 支持** — 后续可同时放入 Linux ISO
- **更易更新** — 只需替换 ISO 文件，无需重新分区
- **兼容性更好** — Ventoy 同时支持 Legacy BIOS 和 UEFI

### 3. 执行步骤

| 步骤 | 操作内容 | 命令 |
| --- | --- | --- |
| **A** | 下载 Ventoy v1.1.17 | `wget https://github.com/ventoy/Ventoy/releases/download/v1.1.17/ventoy-1.1.17-linux.tar.gz` |
| **B** | 解压压缩包 | `tar xzf ventoy-1.1.17-linux.tar.gz` |
| **C** | 卸载旧 U 盘分区 | `sudo umount /dev/sdb1 /dev/sdb2` |
| **D** | 将 Ventoy 安装到 `/dev/sdb` | `printf 'y\ny\n' \| sudo ./Ventoy2Disk.sh -i /dev/sdb` |
| **E** | 挂载新 Ventoy 分区 | 系统自动挂载 `/dev/sdb1` 到 `/mnt` |
| **F** | 复制 Windows 11 ISO | `sudo cp ~/Downloads/Win11_25H2_English_x64_v2.iso /mnt/` |
| **G** | 同步并卸载 | `sync && sudo umount /mnt` |
| **H** | 关闭 U 盘电源 | `udisksctl power-off -b /dev/sdb` |

### 4. Ventoy 内部所做的工作

在步骤 D 中，Ventoy：

1. **擦除**整个磁盘（`dd if=/dev/zero ...`）
2. **创建 2 个分区**：
   - `/dev/sdb1`（14.6G，exFAT，卷标 `Ventoy`）— 用于存储 ISO 文件
   - `/dev/sdb2`（32M，vfat，卷标 `VTOYEFI`）— EFI 启动加载器分区
3. **安装其自定义启动加载器** — 写入 MBR 和 EFI 分区
4. **写入 Ventoy 核心磁盘映像** — 包含启动菜单引擎

### 5. 最终 U 盘布局

| 分区 | 大小 | 文件系统 | 卷标 | 作用 |
| --- | --- | --- | --- | --- |
| `/dev/sdb1` | 14.6G | **exFAT** | `Ventoy` | ISO 存储（存放 `Win11_25H2_English_x64_v2.iso`，占用 7.9G） |
| `/dev/sdb2` | 32M | **vfat** | `VTOYEFI` | EFI 启动加载器 |

**已用空间总计**：7.9G / 15G（53%）— 仍有足够空间存放更多 ISO。

### 6. 启动过程

当从此 U 盘启动时：

1. **UEFI 固件**加载 `VTOYEFI` 分区 → Ventoy 的 EFI 启动加载器启动
2. Ventoy 扫描 `/dev/sdb1` 中的 `.iso` 文件
3. **启动菜单**显示 `Win11_25H2_English_x64_v2.iso`
4. 用户选择该选项 → Ventoy **创建一个虚拟 BIOS/UEFI 环境**，并直接从 ISO 启动 Windows 安装程序
5. Windows 安装程序识别到正常启动环境，继续进行安装

### 7. 联想小新重要提示

如果 Windows 安装程序**无法检测到 NVMe SSD**，那是 Intel VMD/RST 驱动问题，而非 U 盘问题。解决方法：

- 在其他电脑上下载 Intel RST F6 驱动
- 将其放入另一个 U 盘
- 在磁盘选择界面 → 加载驱动程序 → 浏览到驱动文件夹 → SSD 即可出现
