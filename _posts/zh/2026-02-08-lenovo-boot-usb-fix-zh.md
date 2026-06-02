---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复联想电脑启动时忽略 Ubuntu USB 启动盘的问题
translated: true
type: note
---

Question: 我的 Ubuntu USB 是通过 `dd` 命令而不是 Etcher 制作的。在我的 Lenovo XiaoXin 笔记本上，当我在 Boot Menu 中选择 Ubuntu 选项时，它仍然会进入正常模式 (Windows) 而不是 Ubuntu。我该怎么办？

Answer:

使用 `dd` 命令创建 Ubuntu USB **不是**问题所在 —— `dd` 是一种完全有效且常用的制作引导 Ubuntu USB 的方法（它会创建 ISO 的精确副本）。在大多数情况下，它产生的结果与 Etcher 或 Rufus 相同，通过 `dd` 写入的 Ubuntu ISO 通常可以正常启动。问题几乎肯定出在你的 Lenovo XiaoXin 笔记本的 BIOS/UEFI 设置上，而不是 USB 的制作方法。

Lenovo XiaoXin 笔记本（中国国内的 IdeaPad 系列）使用的 UEFI 固件默认开启了 **Secure Boot**。虽然 Ubuntu 支持 Secure Boot，但有时会出现兼容性问题（特别是对于某些 ISO、内核，或者 USB 未被识别为有效的已签名 EFI 启动项）。在 Lenovo 笔记本上，当你在 **One-time Boot Menu** (Fn+F12) 中选择了 USB，但系统忽略它并仍然启动 Windows 时，更常见的原因是：

1. **Secure Boot** 仍处于开启状态并阻止了引导（即使 Ubuntu 理论上应该支持它）。
2. **Boot Mode** 设置为 "UEFI Only" 且未正确识别 USB，或者需要开启 "UEFI/Legacy (CSM)" 或 "Both"。
3. USB 出现在 Boot Menu 中但优先级排序不正确，或者固件跳过了它。

### 建议的修复步骤（按顺序执行）

1. **进入 BIOS Setup**（不仅仅是引导菜单）：
   - 完全关闭笔记本电脑。
   - 开机并在出现 Lenovo Logo 时**立即连续敲击 F2**（或 Fn+F2）。
     （某些 XiaoXin 型号使用 Fn+F2、Novo 按钮，或者 F1/Fn+F1 —— 请尝试不同组合。）
   - 这应该会进入完整的 BIOS/UEFI 设置界面。

2. **禁用 Secure Boot**：
   - 切换到 **Security** 选项卡（或 Boot → Secure Boot）。
   - 将 **Secure Boot** 设置为 **Disabled**。
   - 如果询问是否清除密钥或切换到 "Setup Mode"，请执行此操作。
   - 保存并退出（通常是 F10 → Yes）。

3. **检查/更改 Boot Mode**（对许多 Lenovo 型号非常重要）：
   - 切换到 **Boot** 或 **Startup** 选项卡。
   - 查找 **Boot Mode**、**UEFI/Legacy Boot** 或 **CSM** (Compatibility Support Module)。
   - 将其更改为 **Both** (UEFI + Legacy/CSM) 或 **Legacy First**（如果 "Both" 不可用）。
     （虽然 Ubuntu 在 UEFI 模式下运行效果最好，但启用 CSM 通常有助于挑剔的 Lenovo 固件识别设备。）
   - 确保 **USB Boot** 或 **External Device Boot** 选项已开启（如果存在该选项）。

4. **设置引导顺序 / USB 优先级**（可选但有帮助）：
   - 在 Boot 选项卡中，如果 USB 设备（或 "USB HDD"、"Removable Device"）出现在列表中，请将其向上移动。
   - 某些型号针对 UEFI 和 Legacy 有分开的 "Boot Priority" 设置。

5. **保存、退出并再次测试 Boot Menu**：
   - 保存更改 (F10 → Yes) 并重启。
   - 插上你的 Ubuntu USB。
   - 在出现 Lenovo Logo 时连续敲击 **Fn + F12**（或仅 F12）打开 Boot Menu。
   - 选择类似于以下的条目：
     - UEFI: [USB 品牌/型号] (例如: UEFI: SanDisk)
     - 或者如果没有 UEFI 前缀，选择 USB 名称。
   - 尽可能避免选择非 UEFI 条目（除非你已切换到 Legacy 模式）。

6. **如果仍然失败**：
   - 使用 **Ventoy** 重新制作 USB（强烈推荐给 Lenovo 笔记本用户）—— 将 Ubuntu ISO 拷贝到 Ventoy USB 中并从 Ventoy 菜单启动。Ventoy 能更好地处理许多 UEFI/Secure Boot 的特殊兼容性问题。
   - 或者在 Windows 上使用 **Rufus** 重新制作，并选择 **DD Image** 模式（而非 ISO 模式）以获得最大兼容性。
   - 尝试更换 USB 端口（某些 Lenovo 型号对 USB 3.0 和 2.0 端口的选择较挑剔）。
   - 从 Lenovo 中国官网更新 BIOS（如果你的 XiaoXin 具体型号有更新）—— 较新的固件有时会修复 USB 引导问题。
   - 在另一台电脑上测试该 USB，确认它可以正常进入 Ubuntu Live 环境。

在禁用 Secure Boot 并启用 CSM/Both 模式后，大多数用户反映 USB 可以正确引导进入 Ubuntu 安装程序/Live 会话。Ubuntu 安装完成后，如果你愿意，可以重新开启 Secure Boot（Ubuntu 会对其 Bootloader 进行签名）。

References:

- [https://support.lenovo.com/us/en/solutions/ht500207-how-to-boot-from-usb-disk-in-the-bios-boot-menu-windows-8-windows-10-ideapadlenovo-laptops](https://support.lenovo.com/us/en/solutions/ht500207-how-to-boot-from-usb-disk-in-the-bios-boot-menu-windows-8-windows-10-ideapadlenovo-laptops)
- [https://askubuntu.com/questions/891248/ubuntu-16-04-how-can-i-disable-secure-boot](https://askubuntu.com/questions/891248/ubuntu-16-04-how-can-i-disable-secure-boot)
- [https://www.reddit.com/r/Lenovo/comments/wwkstm/new_laptop_cannot_boot_to_usb_it_always_jumps](https://www.reddit.com/r/Lenovo/comments/wwkstm/new_laptop_cannot_boot_to_usb_it_always_jumps)
- [https://forums.lenovo.com/t5/Other-Linux-Discussions/BIOS-does-not-recognize-USB-boot-media/m-p/5304674](https://forums.lenovo.com/t5/Other-Linux-Discussions/BIOS-does-not-recognize-USB-boot-media/m-p/5304674)
