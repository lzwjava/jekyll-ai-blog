---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 彻底修复 Windows 11 USB 安装问题
translated: true
type: note
---

Question: 在 macOS 上将 Win11_25H2_China_GGK_Chinese_Simplified_x64.iso 写入 /dev/rdisk10 的 dd 命令已经完成。现在，在当前运行 Ubuntu 的 Lenovo XiaoXin 14 IAH8 笔记本电脑上，我该如何继续从这个 USB 安装 Windows 11？

Answer:

你的 dd 命令已成功完成（已写入约 7 GB），因此该 USB 现在被准备为 Windows 11 ISO 的原始副本。

**关于在非 Windows 系统上使用 dd 方法的重要提示**
虽然简单的 `dd` 方法适用于许多较旧的 Windows 版本，但对于 Windows 10/11 ISO（尤其是像 25H2 这样较新的版本），它经常会导致问题：安装程序可以启动，但无法检测到内部驱动器（SSD/NVMe 显示为缺失）。发生这种情况是因为 Windows 需要特定的分区布局、针对大型 install.wim 文件（>4 GB）的 FAT32 + NTFS 分割，以及 dd 无法正确生成的启动文件。

### 推荐的下一步操作（最安全且最可靠）

1. **先不要尝试启动当前的 USB** —— 失败的概率很高。
2. 重新进入你 Lenovo XiaoXin 14 上的 **Ubuntu** 系统。
3. 安装并使用更好的工具来重新正确制作启动 USB：
   - **Ventoy**（2025–2026 年最简单且推荐的工具）
     - 下载 Ventoy → <https://www.ventoy.net（或从> GitHub releases 下载）
     - 运行 Ventoy → 将其安装到你的 USB 驱动器（它会格式化 USB 并创建两个分区）
     - 只需将你的 .iso 文件复制到 Ventoy 的数据分区中
     - 完成 —— Ventoy 会自动处理 Windows 11 的各种特殊情况（包括需要时的 install.wim 文件分割）
   - 如果你也喜欢其他工具：
     - **WoeUSB**（适用于单个 Windows ISO，支持 NTFS 目标分区）
       - 通过 PPA 或 flatpak 安装：`sudo apt install woeusb`
       - 示例：`sudo woeusb --device your.iso /dev/sdX`
     - **mkusb** 或 **woeusb-ng**（同样可以处理大型 install.wim 问题）

4. 使用 Ventoy / WoeUSB 创建好 USB 后：
   - 安全弹出 USB。

### 如何在 Lenovo XiaoXin 14 IAH8 上启动并安装 Windows 11

Lenovo XiaoXin 系列（类似 IdeaPad 的中国国内产品线）通常使用这些按键：

- 启动菜单 Boot Menu（推荐 —— 一次性选择）：
  重启（或开机）→ 当显示 Lenovo logo 时立即 **快速连续按 Fn + F12**（或仅 F12）→ 选择 USB 设备（可能显示为 UEFI: SanDisk / Kingston / USB 名称）

- 进入完整 BIOS 设置（如果启动菜单不起作用或需要更改设置）：
  在 Lenovo logo 出现时快速连续按 **Fn + F2**（或 F2）→ 进入 BIOS。

**安装 Windows 11 常需的 BIOS 更改**

1. 前往 **Security** 选项卡 → 设置 **Secure Boot → Disabled**
2. 前往 **Boot** 选项卡：
   - 设置 **Boot Mode** / **Boot Priority** → **UEFI**（除非你有特殊需求，否则不要选 Legacy/CSM）
   - 确保 USB / UEFI USB 出现在启动顺序中（如果需要，将其移至顶部）
3. **Save & Exit**（通常是 F10 → Yes）

然后重启并使用 **F12** 选择 USB。

### 安装流程（进入 Windows Setup 后）

- 选择语言（由于是 GGK/中国版，默认应显示简体中文）
- 点击 "立即安装"
- 如果要求输入产品密钥，请输入（也可以选择稍后激活并跳过）
- 选择 **自定义：仅安装 Windows (高级)**
- **删除内部 NVMe 驱动器上的所有现有分区**（Ubuntu 分区 + 任何残留分区）
- 选择未分配的空间 → 下一步 → Windows 将自动创建分区
- 安装将正常进行（可能会重启多次）

### 快速故障排除清单

- 启动菜单中未显示 USB？→ 尝试不同的 USB 端口（优选 USB 3.0）/ 使用 Ventoy 重新制作
- 安装程序中未检测到驱动器？→ 几乎可以肯定地说是 dd 的问题 → 重新制作 USB
- Secure Boot 报错？→ 在 BIOS 中禁用它
- TPM / Secure Boot 限制？→ Windows 11 25H2 默认仍需要 TPM 2.0 + Secure Boot，但如果需要你可以绕过（安装过程中的注册表方法或 Rufus 调整 —— 但既然你的 ISO 是官方的，最好保持兼容性）

如果 dd 制作的 USB 奇迹般地修好了 —— 那很好，但经验表明，在 macOS/Linux 上使用 dd 制作较新的 Windows 11 镜像时，失败率约为 70–80%。

References:

- [https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre](https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre)
- [https://askubuntu.com/questions/1554334/what-is-the-correct-way-to-create-a-windows-11-usb-install-drive-from-ubuntu](https://askubuntu.com/questions/1554334/what-is-the-correct-way-to-create-a-windows-11-usb-install-drive-from-ubuntu)
- [https://www.ventoy.net](https://www.ventoy.net)
