---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在联想小新上通过 USB 启动 Ubuntu
translated: true
type: note
---

问题：如何在 Lenovo XiaoXin 14 IAH8 笔记本上从 Ubuntu live USB 启动？用户已使用 dd 命令通过 ubuntu-24.04.3-desktop-amd64.iso 创建了启动盘。

回答：

你的 dd 命令创建了一个标准的、可启动的 Ubuntu 24.04.3 live USB（默认兼容 UEFI）。以下是在你的 Lenovo XiaoXin 14 IAH8（国内版 XiaoXin 14，类似于 IdeaPad 系列）上从中启动的步骤。

### 启动 Ubuntu live USB 的详细步骤

1. **插入 USB 驱动器**
   将 USB 插入 USB 端口（为了更快的加载速度，建议使用 USB 3.0/3.1 端口）。

2. **完全关闭笔记本电脑电源**
   完全关机（不要选择重启，因为 fast boot / 混合关机可能会产生干扰）。
   如果需要，可以按住电源按钮强制关机。

3. **开机并进入 boot menu**
   - 按下电源按钮。
   - 看到 Lenovo 标志后，**立即反复点按 Fn + F12**（如果你的键盘不需要 Fn 键即可触发功能键，则直接按 F12）。
     - 持续点按直到出现 **Boot Menu** (Startup Menu)。
   - 在 boot menu 中，寻找如下条目：
     - UEFI: [USB 品牌名称，例如 SanDisk, Kingston, USB Flash]
     - 或者仅显示为 USB 的名称
   - 使用方向键选中 **UEFI USB 条目**（如果显示 Legacy/CSM，请避开），然后按 **Enter**。

   如果尝试几次后 Fn + F12 仍不起作用：
   - 尝试单独按 **F12**。
   - 某些 XiaoXin 机型带有一个小的 **Novo button**（位于电源按钮附近或侧边的小针孔）— 在关机状态下用回形针按它 → 在出现的 Novo 菜单中选择 **Boot Menu** → 如果还没插入 USB，请插入。

4. **如果未显示 boot menu 或找不到 USB** → 先进入完整的 BIOS Setup
   - 开机 → 看到 Lenovo 标志时立即反复点按 **Fn + F2**（或 F2）。
   - 在 BIOS 中：
     - 转到 **Security** 选项卡 → **Secure Boot** → 设置为 **Disabled**（这对于大多数 live USB 很重要）。
     - 转到 **Boot** / **Startup** 选项卡：
       - 确保 **Boot Mode** 为 **UEFI**（或 **UEFI Only**；除非 UEFI 失败，否则不要设置为 Legacy）。
       - 如果有 **UEFI/Legacy Boot** 选项 → 设置为 **Both** 或 **UEFI First**。
       - 在 **Boot Priority** 或 **Boot Order** 中，将 **USB HDD** 或 **UEFI: USB** 移至顶部（使用 +/− 或 F5/F6 键）。
     - 按 **F10** → 选择 **Yes** 保存并退出。
   - 笔记本将重启 → 现在重复步骤 3 (Fn + F12) 快速选择 USB。

5. **进入 Ubuntu 后**
   - 你应该会看到 GRUB 菜单（Ubuntu 选项）。
   - 选择 **Try Ubuntu** (live session) — 这将从 USB 运行 Ubuntu，而不会触碰你的硬盘数据。
   - 或者如果你想重新安装或修复，选择 **Install Ubuntu**。

### 如果仍然无法启动的常见修复方法
- **USB 未列出** → 使用不同的工具（如 Ventoy、balenaEtcher 或另一台 Ubuntu 上的 Startup Disk Creator）重新制作 USB — dd 有时在某些 BIOS 上会出现极端情况下的兼容性问题。
- **黑屏 / 卡住** → 在 boot menu 中尝试非 UEFI USB 条目（如果有，虽然很少见）。
- **Secure Boot 错误** → 必须在 BIOS 中禁用（参考步骤 4）。
- **Fast boot 干扰** → 启动前确保始终是完全关机（而非重启）。
- 接口错误 → 尝试更换不同的 USB 端口（某些 Lenovo 机型对 USB-C 和 USB-A 端口的引导支持不同）。

这应该能让你进入 live 环境，以便修复之前损坏的系统（如之前提到的 chown 权限问题）。

参考：

- [https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre](https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre)
- [https://wiki.archlinux.org/title/Lenovo_XiaoXin_15are_2020](https://wiki.archlinux.org/title/Lenovo_XiaoXin_15are_2020)（关于按键的相似 XiaoXin 系列信息）
- [https://support.lenovo.com/us/en/solutions/ht500216-recommended-way-to-enter-bios-ideapad](https://support.lenovo.com/us/en/solutions/ht500216-recommended-way-to-enter-bios-ideapad)
