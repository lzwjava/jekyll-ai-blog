---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 先测试Linux Mint Live USB
translated: true
type: note
---

这是一份总结——留待你准备时使用：

**建议：先从 Live USB 测试开始。**

步骤：
1. 在任何机器上从 linuxmint.com 下载 Linux Mint Cinnamon ISO (22.x)
2. 将 ISO 写入 USB 驱动器（16 GB 以上）：在 macOS 上执行 `sudo dd if=linuxmint.iso of=/dev/rdiskN bs=4m`
3. 插入 MacBook Pro，启动时按住 Option 键，选择 USB
4. 启动进入 Live 会话——测试 Wi-Fi、触控板、键盘、音频、显示
5. 如果一切正常（或你能通过外接网卡/驱动修复 Wi-Fi），再决定安装方式

**为何先测试：** Broadcom Wi-Fi 是主要风险。如果安装后无法联网，你会陷入困境。Live 会话让你在投入之前先确认硬件支持。

如果 Live 会话运行良好，我建议**安装到外部 USB SSD**——这种方式无破坏性，给你一个便携的 Linux 系统，同时保留 macOS 以便恢复。一个 128 GB 的 USB 3.0 SSD 大约花费 15-20 美元。