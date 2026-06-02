---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 适用于 Win11 USB 启动的 Mac dd 命令指南
translated: true
type: note
---

问题：假设我下载了 ISO 镜像 `Win11_25H2_China_GGK_Chinese_Simplified_x64.iso`，如何通过 Terminal 命令（`dd`）在 Mac 上制作一个可启动的 USB 启动盘？

回答：

**开始前的核心警告：**
`dd` 命令非常强大但也极其危险 —— 输入错误的磁盘标识符将**抹除你 Mac 的内置硬盘或其他重要的存储设备**。请务必核对所有信息。
对于现代 Windows 11 ISO（包括中国家庭版），简单的 `dd` 方法通常可以可靠地创建一个可供大多数 UEFI PC 启动的 USB，尤其是在 2025–2026 年的报告中。虽然过去曾有因 `install.wim` 文件过大或 Hybrid ISO 特性导致问题的记录，但最近的用户体验（包括 25H2 版本）确认了直接使用 `dd` 的成功率。

### 使用 Terminal（dd 方法）的详细步骤

1. **插入你的 USB 闪存盘**
   - 请使用容量至少为 8 GB 的驱动器（建议 16 GB 以上）。
   - **USB 上的所有数据将被完全抹除。**

2. **打开 Terminal**
   - 前往 Applications → Utilities → Terminal。

3. **识别 USB 的正确磁盘编号**
   运行此命令：

   ```
   diskutil list
   ```

   在列表中寻找你的 USB 驱动器。它通常显示为 `/dev/disk2`、`/dev/disk3` 等（通常不是 `/dev/disk0` 或 `/dev/disk1`，因为这些通常是你的 Mac 内置硬盘）。
   通过容量和名称确认（例如：external, ~16 GB）。
   示例输出片段：

   ```
   /dev/disk3 (external, physical):
      #:                       TYPE NAME                    SIZE       IDENTIFIER
      0:      GUID_partition_scheme                        *15.9 GB    disk3
   ```

   → 在此例中，应使用 `/dev/disk3`（或与你实际情况匹配的编号）。

4. **卸载（Unmount）USB 驱动器**（重要 —— 请勿跳过）
   将 `disk3` 替换为你实际的编号：

   ```
   diskutil unmountDisk /dev/disk3
   ```

5. **使用 dd 将 ISO 写入 USB**
   在 macOS 上使用 `/dev/rdiskX`（Raw Disk）可以获得更快的速度。替换路径和磁盘编号：

   ```
   sudo dd if=~/Downloads/Win11_25H2_China_GGK_Chinese_Simplified_x64.iso of=/dev/rdisk3 bs=1m
   ```

   - `if=` → 输入文件：ISO 的路径（可将文件直接拖入 Terminal 窗口以自动填充路径，或使用 `~/Downloads/...`）。
   - `of=` → 输出：`/dev/rdisk3`（使用 rdisk 以提高速度；rdiskX 是 diskX 的原始版本）。
   - `bs=1m` → 块大小 1 MB（更快；有些人使用 `bs=4m` 或 `bs=8m`）。
   - 系统会要求你输入 Mac 密码（sudo）。

   该命令默认不会显示进度。如需查看状态，可以偶尔按下 **Ctrl + T**。
   根据 USB 速度和 Mac 型号，通常需要 10–30 分钟。

6. **等待完成**
   完成后，你将看到如下输出：

   ```
   XXXX+0 records in
   XXXX+0 records out
   XXXXXXXX bytes transferred in XXX.XXX secs (XX bytes/sec)
   ```

7. **安全弹出 USB**

   ```
   diskutil eject /dev/disk3
   ```

   （使用原始磁盘编号，而不是 rdisk。）
   然后从物理上拔掉 USB。

8. **进行测试**
   将 USB 插入目标 PC，进入 BIOS/UEFI（通常按 F2, Del, F12, Esc），将 USB 设置为第一启动设备，启用 UEFI 模式（如果需要，禁用 Legacy/CSM），然后启动。
   中国版 ISO 应该会启动进入简体中文安装界面。

**注意事项与故障排除**

- 如果 PC 未能识别 USB 为可启动盘：尝试用 `bs=4m` 重新制作，确保使用 UEFI 启动（而非 Legacy），暂时禁用 Secure Boot，或尝试不同的 USB 接口/驱动器。
- 中国版 ISO（GGK 版本）在启动方面的表现与标准 Windows 11 x64 ISO 相同 —— 目前没有发现特别的差异。
- **如果你担心 dd 的风险，可以选择更安全的替代方案**（图形界面，无 Terminal 误操作风险）：
  - balenaEtcher（免费、流行，对 Windows ISO 支持良好）
  - WinDiskWriter 或近期指南中提到的类似专用工具。
- 对于 Apple Silicon（M 系列芯片）的 Mac，Boot Camp Assistant 不可用 —— dd 或第三方工具是主要选择。

这种 dd 方法直接克隆了 Hybrid ISO 结构，保留了 Windows 11 所需的 EFI 启动文件。

参考资料：

- [https://www.microsoft.com/zh-cn/software-download/windows11](https://www.microsoft.com/zh-cn/software-download/windows11)
- [https://superuser.com/questions/1885142/how-to-use-macos-to-create-a-windows-11-usb-installer-flash-drive](https://superuser.com/questions/1885142/how-to-use-macos-to-create-a-windows-11-usb-installer-flash-drive)
- [https://gist.github.com/acarril/8c15f600cf0397dd61161a470f50f669](https://gist.github.com/acarril/8c15f600cf0397dd61161a470f50f669)
- [https://www.pugetsystems.com/support/guides/w11-usb-macos](https://www.pugetsystems.com/support/guides/w11-usb-macos)
