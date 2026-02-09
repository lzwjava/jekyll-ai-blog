---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 如何在微星 B760M 迫击炮主板上进入 BIOS
translated: true
type: note
---

Question: 如何在搭载 MSI MAG B760M Mortar WiFi 主板的电脑上进入 BIOS？

Answer: 

要在使用 **MSI MAG B760M Mortar WiFi** 主板（MSI B760 系列主板）的电脑上进入 **BIOS/UEFI** 设置，请按照以下步骤操作：

### 主要方法（开机过程中）：
1. 完全 **关闭电脑**（关机，而不仅仅是睡眠或休眠）。
2. **按下电源按钮** 开机。
3. 系统启动后（甚至在屏幕出现 Logo 之前），立即 **连续狂按 Delete (Del) 键**。  
   - 快速敲击直到 BIOS 设置界面加载完毕。  
   - 这是几乎所有现代 MSI 主板（包括您的 MAG B760M Mortar WiFi 等 B760 系列）的标准按键。
4. 如果尝试几次后 Del 键无效，也可以在开机时尝试连续敲击 **F2** 键（部分 MSI 主板会将两者都列为备选，但台式机主板通常以 Del 键为主）。

**操作技巧**：
- 使用直接插在主板背面 USB 端口上的 **有线 USB 键盘**（在首次启动时避免使用前置面板端口或无线键盘，因为 USB 初始化有时会有延迟）。
- 如果 BIOS 中已启用 Fast Boot 或 Ultra Fast Boot（或者开启了 Windows Fast Startup），启动过程可能太快而无法捕捉到按键 —— 在这种情况下，请先使用下方的 Windows 备选方法。
- 仔细观察屏幕：许多 MSI 主板在 POST 过程中会简短显示 "Press DEL to enter Setup"（或类似提示）。

### 备选方法（从 Windows 进入，若电脑已进入操作系统）：
如果您无法在开机时捕捉到按键：
1. 正常启动进入 Windows。
2. 前往 **Settings** → **System** → **Recovery**（或搜索“高级启动”）。
3. 在 **Advanced startup** 下，点击 **Restart now**。
4. 重启后，依次选择 **Troubleshoot** → **Advanced options** → **UEFI Firmware Settings** → **Restart**。
5. 系统将直接重启并进入 BIOS 设置界面。

进入 BIOS 后：
- 导航至 **Power Management**（或类似名称）部分。
- 寻找 **Wake-on-LAN**、**Wake on PCIe**、**PCIe Wake Up**、**Power On By PCI-E** 或 **ErP Ready**（如有必要请禁用 ErP，因为它会阻止唤醒功能）等选项。
- 开启 Wake-on-LAN 相关设置。
- 保存更改（通常是 **F10** → Yes）并退出。

这些步骤应该适用于您的这款 MSI 主板。

References:  

- MAG B760M MORTAR WIFI 官方支持页面: [https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/support](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/support)
- 多个 YouTube 教程和 MSI 论坛贴确认 B760 系列和 Mortar 型号使用 **Del** 键。