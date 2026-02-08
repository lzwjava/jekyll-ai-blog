---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Windows 11 驱动程序缺失修复指南
translated: true
type: note
---

Question: 我在 macOS 上成功使用 dd 创建了启动 USB，将其插入目标机器，但在 Windows 11 安装过程中卡在了“安装驱动程序以显示硬件”界面。该界面有两个选项：第一个是 C，第二个是 X，我不知道该选哪个，所以无法继续。

Answer:

你看到的屏幕（“安装驱动程序以显示硬件”）是 Windows Setup 提示的中文版本，当安装程序无法检测到你的存储驱动器（SSD, NVMe, SATA HDD 等）时就会出现这种情况。这是 Windows 11 安装过程中的常见问题，尤其是在较新的硬件上，例如近期的 Intel/AMD 平台、启用了 Intel VMD (Volume Management Device) 的笔记本电脑、RAID 配置或某些 NVMe 控制器。

### 按钮的含义（基于标准 Windows Setup 行为）：

- **第一个选项 (C)** → 通常是“继续”或“取消”/“跳过”（跳过或在不加载驱动程序的情况下继续）。
  选择此项通常会导致不显示任何驱动器 → 你无法选择安装 Windows 的位置 → 安装失败或循环。

- **第二个选项 (X)** → 通常是“加载驱动程序”/“浏览”/“安装驱动程序”（浏览以加载驱动程序）。
  在驱动器不可见的情况下，这几乎总是正确的选择。

**你现在应该做的是**：
1. 选择**第二个选项 (X)** —— 用于加载/浏览驱动程序的选项。
2. Windows Setup 将打开一个文件浏览器对话框，要求你选择驱动程序（.inf 文件）。
   - 如果你**没有准备额外的驱动程序**，它可能不会显示任何有用的内容或提示失败 → 你需要准备它们（见下文）。
   - 如果你已经插入了存有驱动程序的独立 USB → 浏览到该 USB，导航到解压驱动程序的文件夹，选择合适的 .inf 文件（对于 Intel RST 通常命名为 "iaStorAC.inf" 或 AMD 的类似文件），然后点击确定/下一步。

### 如何正确修复（准备存储驱动程序）

此提示几乎总是意味着缺少 **storage controller driver** (SATA/AHCI/NVMe/RAID)。dd 方法创建的是原生的 ISO 副本，因此 USB 本身没有问题 —— 问题出在特定硬件上。

**解决步骤**：
1. **在另一台电脑上**（你的 Mac 或任何可以运行的 PC）：
   - 前往目标机器的制造商网站（Dell, HP, Lenovo, ASUS, MSI, Gigabyte 等）或主板型号页面。
   - 下载适用于 Windows 11 (64-bit) 的 **chipset** + **storage** / **IRST** / **RAID** 驱动程序。
     - Intel 平台：查找 "Intel Rapid Storage Technology" (IRST) 或 "Intel VMD" 驱动。
     - AMD 平台：AMD RAID 驱动程序或标准 chipset 驱动。
     - 笔记本品牌通常将它们归类在 "Chipset" 或 "Storage" 类别中。
   - 解压缩下载的文件（如果是 .exe 文件，请使用 7-Zip 或类似工具）以获取包含 .inf 文件的原始驱动程序文件夹。

2. **将它们放入第二个 USB 驱动器**（格式化为 FAT32，与你的 Windows 安装 USB 分开）：
   - 将解压后的驱动程序文件夹复制到这第二个 USB 的根目录或子文件夹中。

3. **安装过程中**（当你再次看到提示时）：
   - 同时插上 **两个** USB（Windows 安装盘 + 驱动程序盘）。
   - 选择第二个选项 (X / 加载驱动程序 / 浏览)。
   - 在浏览器中，选择第二个 USB，进入驱动程序文件夹，选中正确的 .inf（先尝试主要的存储驱动程序），点击确定。
   - Windows 随后应检测并显示你的驱动器 → 你可以继续选择分区并进行安装。

### 如果不想寻找驱动程序的快速备选方案

- 如果你的 PC 较旧或属于标准配置（2020 年之前的 Intel/AMD），请尝试在 BIOS 中禁用 **Intel VMD** 或 **RAID mode** → 将其设置为 **AHCI** → 很多时候这能让内置的 Windows 驱动程序在无需额外加载的情况下工作。
- 在 Windows PC 上使用 Microsoft 官方的 Media Creation Tool 重新制作 USB 而不是使用 dd —— 有时它会注入更多的兼容性驱动，但理论上 dd 应该是等效的。
- 对于非常新的硬件（例如搭载 VMD 的 Intel 12 代及以上，AMD Ryzen 7000/8000/9000），通常必须加载驱动程序 —— 除非更改 BIOS 设置，否则无法绕过。

一旦加载了正确的驱动程序，驱动器就会出现，安装将正常进行。这**不是**你用 dd 创建的 USB 的问题；这是许多现代系统的预期行为。

References:  

- [https://learn.microsoft.com/en-us/answers/questions/5488804/windows-11-installation-error-install-driver-to-sh](https://learn.microsoft.com/en-us/answers/questions/5488804/windows-11-installation-error-install-driver-to-sh)
- [https://www.elevenforum.com/t/install-driver-to-show-hardware-issue-on-ryzen-cpus-using-bootable-usb-from-win11-media-creation-tool.29536](https://www.elevenforum.com/t/install-driver-to-show-hardware-issue-on-ryzen-cpus-using-bootable-usb-from-win11-media-creation-tool.29536)
- [https://forums.lenovo.com/t/Lenovo-IdeaPad-1xx-3xx-5xx-7xx-Edge-LaVie-Z-Flex-Laptops/Installation-Windows-11-Install-driver-to-show-hardware/m-p/10002482](https://forums.lenovo.com/t/Lenovo-IdeaPad-1xx-3xx-5xx-7xx-Edge-LaVie-Z-Flex-Laptops/Installation-Windows-11-Install-driver-to-show-hardware/m-p/10002482)
- Various Reddit threads on r/buildapc and Microsoft communities describing the "install driver to show hardware" prompt and load driver solution