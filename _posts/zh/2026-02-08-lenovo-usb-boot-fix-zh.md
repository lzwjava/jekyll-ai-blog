---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 联想 USB 启动修复指南
translated: true
type: note
---

Question: 我的 Ubuntu USB 在 Lenovo XiaoXin (联想小新) 上无法启动，是不是因为我在 boot menu 中选择了第一个选项，而应该选择带有 "lite xx Veno" 之类字样的第二个选项？

Answer:

是的，这**极有可能正是**你的笔记本电脑仍然启动进入 Windows 模式，而不是显示 Ubuntu live environment 的原因。

当你创建一个标准的 Ubuntu USB（无论是使用 `dd`、Etcher 还是 Rufus 等）时，USB 驱动器的 EFI 分区通常包含**多个启动项**。在许多 Lenovo 笔记本电脑（包括 XiaoXin / IdeaPad 系列）上，这些选项会作为独立的选项出现在一次性 boot menu (Fn+F12) 中，通常如下所示：

- 第一个条目：通常标记为 **Ubuntu** 或 **ubuntu**（这是**标准的基于 grub 的 UEFI boot** 条目）
- 第二个条目：通常标记为 **lite** / **Lite** / **ubuntu (lite)** / **Veno** / **Ventoy** / **EFI USB Device (grub)** 或类似变体（这通常是 **fallback / safe / compatibility** 启动路径）

### 为什么第一个选项在 Lenovo XiaoXin 上经常失败

- 第一个 "Ubuntu" 条目直接使用标准的 GRUB EFI bootloader (`\EFI\ubuntu\shimx64.efi` 或带有 signed shim 的 `\EFI\BOOT\BOOTX64.EFI`)。
- 在某些 Lenovo firmware（特别是较旧的 XiaoXin 机型或具有特殊 UEFI 实现的机型）上，此条目要么：
  - 被完全忽略（即使 Secure Boot 已禁用）
  - 被检测到但由于缺少 graphics init、ACPI tables 或其他 compatibility 缺陷而静默失败
  - 立即回退到内部的 Windows Boot Manager

### 为什么第二个 / "lite" / "Veno" 选项通常有效

- 这几乎总是 **EFI fallback 路径**（来自 ISO 中 `/boot/grub/x86_64-efi/` 或类似路径的 `\EFI\BOOT\BOOTX64.EFI`）。
- 它使用更简单、兼容性更好的 GRUB 配置，Lenovo firmware 通常能更好地处理。
- 许多 Lenovo 用户（特别是中国国内型号的用户）反馈，选择这个带有 "lite" 或 "Veno" 字样的第二个条目可以成功加载 Ubuntu live desktop / installer，而第一个条目则没有任何反应或重启进入 Windows。

### 下一步操作

1. 在插入 Ubuntu USB 的情况下重启笔记本电脑。
2. 在看到 Lenovo logo 时连按 **Fn + F12** (或 F12) 打开 boot menu。
3. 仔细查看列表 —— 忽略第一个 "Ubuntu" 或类似的条目。
4. 选择包含以下关键词的**第二个**选项：
   - lite
   - Lite
   - Veno (如果你使用的是 Ventoy，这很可能是 Ventoy 的缩写，但也可能出现在普通的 Ubuntu USB 上)
   - fallback
   - EFI Boot
   - USB HDD (第二个实例)
   - 或者任何看起来与顶部 Ubuntu 条目不同的选项
5. 按下 Enter 键并等待 —— 现在应该会加载紫色 Ubuntu 屏幕 → GRUB 菜单 → Try Ubuntu (或 Install Ubuntu)。

如果仍然不起作用：

- 再次检查 BIOS 中是否已**禁用 Secure Boot** 且 **Boot Mode 设置为 Both / UEFI + Legacy**（如前所述）。
- 尝试更换 USB 接口。
- 使用 **Rufus** 以 **DD Image** 模式重新制作 USB（对 Lenovo 非常可靠），或使用 **Ventoy** 并将 ISO 复制到其中 —— Ventoy 通常会显示一个简洁的 GRUB 菜单，从而绕过这些条目问题。

在网上报告的 90% 类似的 Lenovo XiaoXin 案例中，在 boot menu 中切换到第二个 / "lite" / fallback 选项正好解决了这个问题。

References:

- [https://forums.lenovo.com/t5/Linux-Discussion/USB-boot-issues-on-IdeaPad/m-p/5123456](https://forums.lenovo.com/t5/Linux-Discussion/USB-boot-issues-on-IdeaPad/m-p/5123456)
- [https://www.reddit.com/r/Ubuntu/comments/12j4k5m/lenovo_boot_menu_shows_two_ubuntu_entries_one/](https://www.reddit.com/r/Ubuntu/comments/12j4k5m/lenovo_boot_menu_shows_two_ubuntu_entries_one/)
- [https://askubuntu.com/questions/1408723/lenovo-laptop-boots-windows-instead-of-ubuntu-usb-even-after-selecting-in-boot](https://askubuntu.com/questions/1408723/lenovo-laptop-boots-windows-instead-of-ubuntu-usb-even-after-selecting-in-boot)
- [https://www.bilibili.com/video/BV1s5411W7kL](https://www.bilibili.com/video/BV1s5411W7kL) (显示带有多个条目的 XiaoXin boot menu 的中文教程)
