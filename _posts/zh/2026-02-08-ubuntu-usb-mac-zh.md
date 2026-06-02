---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Mac 上创建 Ubuntu 启动盘
translated: true
type: note
---

Question: 如何在 macOS 上使用 dd 命令将 ubuntu-24.04.3-desktop-amd64.iso 制作成 Ubuntu 启动盘？

Answer:

以下是在 macOS 上使用 `dd` 命令为 **Ubuntu 24.04.3 Desktop (amd64)** 创建启动 USB 驱动器的分步指南。该方法适用于 Intel 和 Apple Silicon 架构的 Mac，生成的启动盘可用于标准 PC 硬件（BIOS 或 UEFI）。

**重要警告**
- 此过程将**擦除**所选 USB 驱动器上的所有内容。
- 输入错误的磁盘标识符会**擦除你的 Mac 内置硬盘**。请务必仔细检查每一步。
- 请使用至少 8 GB 的 USB 驱动器（建议 16 GB 以上）。

### 分步操作指南

1. **插入 USB 驱动器**并关闭所有弹出的窗口。

2. **打开 Terminal**（在 Applications → Utilities 中找到，或通过 Spotlight 搜索）。

3. **确定正确的磁盘编号**
   运行以下命令：
   ```
   diskutil list
   ```
   查找你的 USB 驱动器。它通常显示为 `/dev/disk2`、`/dev/disk3` 等（不要选择内置硬盘，内置硬盘通常是 `/dev/disk0` 或 `/dev/disk1`）。

   输出示例片段：
   ```
   /dev/disk2 (external, physical):
      #:                       TYPE NAME                    SIZE       IDENTIFIER
      0:      GUID_partition_scheme                        *31.9 GB    disk2
      1:                        EFI EFI                     209.7 MB   disk2s1
      2:                  Apple_HFS Untitled                31.7 GB    disk2s2
   ```
   → 在此示例中，整个 USB 设备是 **disk2**。

4. **卸载 USB 驱动器**（将 `diskN` 替换为你的编号，例如 `disk2`）
   ```
   diskutil unmountDisk /dev/diskN
   ```
   示例：
   ```
   diskutil unmountDisk /dev/disk2
   ```

   在 macOS 上建议使用速度更快的 raw device 路径：
   ```
   diskutil unmountDisk /dev/disk2
   ```

5. **使用 `dd` 将 ISO 写入 USB 驱动器**
   使用 `/dev/rdiskN`（raw device — 比 `/dev/diskN` 快得多）。

   基础安全命令（推荐）：
   ```
   sudo dd if=~/Downloads/ubuntu-24.04.3-desktop-amd64.iso of=/dev/rdiskN bs=4m status=progress
   ```

   示例（假设 ISO 在 Downloads 文件夹中，且 USB 是 disk2）：
   ```
   sudo dd if=~/Downloads/ubuntu-24.04.3-desktop-amd64.iso of=/dev/rdisk2 bs=4m status=progress
   ```

   - 系统会要求你输入管理员密码（输入时字符不会显示，这是正常现象）。
   - `status=progress` 会显示传输速度和已写入的字节数（macOS Ventura 及更高版本支持良好）。
   - 如果在旧版 macOS 上无法识别 `status=progress`，请将其删除。

   其他常用的替代方案：
   ```
   sudo dd if=~/Downloads/ubuntu-24.04.3-desktop-amd64.iso of=/dev/rdisk2 bs=1m
   ```
   或
   ```
   sudo dd if=~/Downloads/ubuntu-24.04.3-desktop-amd64.iso of=/dev/rdisk2 bs=8m conv=fsync
   ```

6. **等待完成**
   - 取决于 USB 速度，通常需要 3–15 分钟。
   - 完成后，你会看到类似以下的输出：
     ```
     6123+0 records in
     6123+0 records out
     6426255360 bytes transferred in 421.248711 secs (15257012 bytes/sec)
     ```

7. **确保所有数据已写入**并安全弹出：
   ```
   sync
   diskutil eject /dev/diskN
   ```
   示例：
   ```
   sync
   diskutil eject /dev/disk2
   ```

8. **拔出 USB 驱动器** — 它现在已经是可启动盘了。

### 快速验证技巧（可选）
写入完成后，再次运行 `diskutil list` — USB 现在应该显示与 Ubuntu ISO 布局匹配的分区（通常是一个 ISO9660 分区及其他分区）。

你现在可以使用此 USB 进行：
- 在标准 PC 上启动（UEFI 或 legacy BIOS）
- 体验 Ubuntu live 模式
- 安装 Ubuntu

祝你好运，并在按下 `dd` 命令的 Enter 键之前务必三连检查磁盘编号！

参考资料：

- [https://documentation.ubuntu.com/desktop/en/latest/how-to/create-a-bootable-usb-stick](https://documentation.ubuntu.com/desktop/en/latest/how-to/create-a-bootable-usb-stick)
- [https://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command](https://osxdaily.com/2015/06/05/copy-iso-to-usb-drive-mac-os-x-command)
- [https://www.cyberciti.biz/faq/creating-a-bootable-ubuntu-usb-stick-on-a-debian-linux](https://www.cyberciti.biz/faq/creating-a-bootable-ubuntu-usb-stick-on-a-debian-linux)
