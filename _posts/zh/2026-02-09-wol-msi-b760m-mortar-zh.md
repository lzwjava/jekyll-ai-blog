---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在微星 B760M 迫击炮主板上开启网络唤醒 (WoL)
translated: true
type: note
---

Question: 在这台配有 MSI MAG B760M Mortar WiFi 主板的电脑中，如何进入 BIOS/UEFI 并在电源管理设置下启用 “Wake-on-LAN” 或 “PCIe/PCI Wake”？

Answer: 

对于使用 **MSI MAG B760M Mortar WiFi** 主板（MSI B760 系列）的 PC，请按照以下具体步骤进入 BIOS 并启用 Wake-on-LAN (WoL)。此过程适用于像您这样近期生产的 MSI Gaming 主板。

### Step 1: 进入 BIOS/UEFI
1. 将电脑完全 **power off**（彻底关机，而非睡眠或休眠）。
2. 按下 **power button** 启动系统。
3. 在按下电源键后，立即 **重复按 Delete (Del) 键**（在屏幕亮起之前就开始连按）。
   - 快速连按 Del 键，直到出现 BIOS 设置程序（MSI logo 或带有选项的黑屏）。
   - 这是您主板的正确按键（已在 MSI B760 型号和官方指南中确认）。
4. 如果尝试几次后 Del 键无效（极少见），请在同样的启动阶段重复按 **F2**。
5. **Tips**:
   - 使用连接到后置 USB 端口的 **有线 USB 键盘**（初次进入时避免使用无线键盘或前置面板端口）。
   - 如果启用了 Windows Fast Startup，可能会导致启动速度过快而无法捕捉按键 —— 如果需要，请先使用下方的 Windows 备选方法。

**从 Windows 内部进入的备选方法**（如果您可以进入 OS）：
1. 打开 **Settings** → **System** → **Recovery**。
2. 在 **Advanced startup** 下，点击 **Restart now**。
3. 重启后选择：**Troubleshoot** → **Advanced options** → **UEFI Firmware Settings** → **Restart**。
4. 电脑将直接进入 BIOS。

### Step 2: 在 BIOS 中启用 Wake-on-LAN
进入 BIOS 后（可能会以 EZ Mode 启动 —— 如果需要，请按 **F7** 切换到 Advanced Mode）：

1. 使用鼠标或方向键选择 **SETTINGS**（通常在顶部/左侧菜单）。
2. 进入 **Advanced** → **Power Management Setup**（有时直接在 **Advanced** 下）。
3. 找到 **ErP Ready**（或 **EuP 2013** / **ERP Ready**）并将其设置为 **Disabled**。  
   - 这非常重要 —— 启用 ErP 会在关机期间切断 PCIe 设备（包括网络控制器）的电源，从而导致 WoL 无法工作。
4. 返回（或导航至） **SETTINGS** → **Advanced** → **Wake Up Event Setup**（有时称为 **Wake Event Setup** 或类似名称）。
5. 找到 **Resume By PCI-E Device**、**Resume By PCI-E/Networking Device**、**Resume By PCIe Device** 或 **Power On By PCI-E Device**。
   - 将其设置为 **Enabled**。
   - 这是主要的 Wake-on-LAN / PCIe wake 设置（您的主板使用连接到 PCIe 的 2.5Gbps Realtek LAN 控制器，因此该选项涵盖了此功能）。
6. （可选但推荐）寻找类似 **Wake Up Event By** 的选项，并将其设置为 **BIOS**（而非 OS），以便在某些情况下获得更可靠的表现。
7. 按下 **F10** 保存 **Save Changes and Exit**，然后确认 **Yes**。
8. 系统将重新启动进入 Windows。

### 后续重要步骤（BIOS 设置之后）
为了让 WoL 在关机后完全正常工作：
- 在 Windows 中：打开 **Device Manager** → **Network adapters** → 右键点击您的 Ethernet 控制器（通常为 Realtek Gaming 2.5GbE Family Controller） → **Properties** → **Power Management** 选项卡：
  - 勾选 **Allow this device to wake the computer**。
  - 勾选 **Only allow a magic packet to wake the computer**（可选，但更安全）。
- 同时在 Windows 中禁用 **Fast Startup**（Control Panel → Power Options → Choose what the power buttons do → Change settings that are currently unavailable → 取消勾选 Turn on fast startup）。
- 确保连接了网线（此主板的 WoL 通常需要有线 LAN，不支持通过 Wi-Fi 唤醒）。

此配置符合官方 MSI WoL 指南以及 B760 系列 Mortar 主板的用户反馈。请通过完全关闭 PC 并从另一台设备发送 magic packet（使用 WakeMeOnLan 等工具或 App）来进行测试。

References:  

- [MSI Official Wake-On-LAN Setup Guide](https://www.msi.com/support/technical_details/MB_Wake_On_LAN)
- [MSI Forum and Reddit threads confirming "Resume By PCI-E Device" and ErP Disabled for B760/B560/MAG Mortar series](https://forum-en.msi.com/index.php?threads/wake-on-lan-mag-b560-mortar.375270/)
- [MSI USA FAQ on Wake on LAN settings](https://us.msi.com/faq/motherboard-503)