---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想 B490 BIOS 指南概览
translated: true
type: note
---

**问题：Lenovo G490 产品及其 InsydeH2O Setup Utility BIOS 介绍**

**回答：**

根据现有信息，**Lenovo G490** 似乎不是一个官方或有广泛记录的 Lenovo 笔记本电脑型号。这极有可能是对 **Lenovo B490** 的误写或记忆偏差。Lenovo B490 是联想在 2012–2013 年左右发布的 Essential B Series 系列中的一款面向预算型/商务市场的笔记本电脑（类似于 B480/B490/B590 等型号）。在联想当时的 G 系列产品线中，包含 G400/G500/G40 等型号，但没有与 G490 描述相匹配的产品。因此，以下介绍基于关系密切且有详细记录的 **Lenovo B490**。

### Lenovo B490 (可能指代的 G490) 概览
Lenovo B490 是一款 14 英寸的入门级商务笔记本，专为家庭和办公使用设计，强调性能可靠、安全特性和高性价比。

**主要规格**（因配置而异）：

- **Display**: 14.0 英寸 HD (1366×768 分辨率)，高光面屏幕
- **Processor**: 第三代 Intel 选项，包括：
  - Intel Core i3 或 i5 (HM77 Chipset 型号)
  - Intel Pentium 或 Celeron (HM70 Chipset 型号)
- **Graphics**: 集成 Intel HD Graphics；部分型号通过 NVIDIA Optimus 技术配备可切换的独立显卡 NVIDIA GeForce GT 635M (1GB) 或 GeForce 610M (1GB)
- **Memory**: 最高支持 8GB DDR3-1600 MHz (高端型号为 2 个插槽；低端型号为 1 个插槽/最大 4GB)
- **Storage**: 2.5 英寸 HDD (320GB–1TB, 5400 或 7200 RPM)；部分型号支持性能加速功能
- **Optical Drive**: DVD/CD Multi-burner (大多数型号配备)
- **Connectivity**: USB 3.0 (1–2 个端口), USB 2.0 (2 个端口), HDMI, VGA, RJ-45 Ethernet, 4-in-1 Card Reader, Combo Audio Jack
- **Wireless**: 集成 Wi-Fi (802.11b/g/n)，可选蓝牙组合；Gigabit Ethernet
- **其他特性**: Webcam (0.3MP 或 720p HD), Stereo Speakers, AccuType 键盘, 可选指纹识别器, One-key Recovery 按钮
- **Battery**: 6 芯 Li-Ion (根据配置续航约 5–6 小时)
- **重量与尺寸**: 约 2.2 kg (4.9 lbs), 340 × 234.6 × 33.1 mm
- **Operating systems**: 最初搭载 Windows 7 (各版本), Windows 8, 或在部分地区提供 FreeDOS/Ubuntu

它被定位为一款耐用、实用的机器，具有同级别中良好的做工（例如某些描述中的“磨砂/石纹”表面）和商务友好型特性（如增强的安全性）。

### InsydeH2O Setup Utility (BIOS)
Lenovo B490 (以及该世代的许多其他 Lenovo 笔记本，尤其是 B/E/G/IdeaPad 系列) 使用 **InsydeH2O** 作为其 BIOS/UEFI Firmware。InsydeH2O (Hardware-2-Operating System) 是 2010 年代初期许多笔记本 OEM 厂商常用的 BIOS 提供商，包括联想的许多型号。

**如何进入 BIOS Setup Utility**:

- 开启或重启笔记本电脑。
- 在出现 Lenovo Logo 屏幕期间，立即反复按下 **F2** (或有时是 **Fn + F2**)。
- 对于像 B490 这样的旧款 Lenovo B 系列型号，你也可以使用侧面或电源键附近的 **Novo Button** (一个小插孔/恢复按钮)：在关机状态下按下它调出菜单，然后选择 "BIOS Setup"。

**此类型号典型的 InsydeH2O BIOS 界面**:

- 包含 **Information**, **Configuration**, **Security**, **Boot**, 和 **Exit** 等标签页。
- 你可以查看系统信息 (CPU, Memory 等)，调整 Boot Order，启用/禁用设备 (例如 USB Boot, Webcam)，设置 Supervisor/User 密码，配置日期/时间，以及恢复默认设置。
- 导航使用方向键，Enter 确认选择，Esc 返回，通常 **F9** 加载默认设置，**F10** 保存并退出。
- 某些 Lenovo InsydeH2O 版本包含隐藏的 Advanced 选项，除非通过特定的按键组合解锁（在 B490 时代的型号上并非标配）。

**注意**:

- 此 BIOS 为旧式 BIOS (在许多单元上早于完全的 UEFI 实现)，尽管某些配置支持 UEFI 模式。
- 常见问题包括循环进入 BIOS (通常由于 CMOS 电池没电、Boot Order 错误或 HDD 故障导致)。
- 对于现代用途 (例如安装 Windows 10/11 等较新操作系统)，如果 UEFI 出现兼容性问题，用户通常需要启用 Legacy/CSM Boot，或者将旧的 HDD 更换为 SSD。

如果这与你的笔记本电脑不符（例如，如果它其实是 G400/G410 或 ThinkPad T490 等不同型号），请提供更多细节，如底部贴纸上的确切型号或处理器代数，以便获取更准确的信息。

**参考资料:**

- [Lenovo B490/B590 Datasheet (PDF)](https://marmaxcomputers.com/img/171020014731b490_b590_ds_en-1-.pdf)
- [Lenovo B490 User Guide (PDF)](https://download.lenovo.com/pccbbs/mobiles_pdf/b490_b590_ug_en.pdf)
- [Lenovo Support - B490 产品页面](https://pcsupport.lenovo.com/us/en/products/laptops-and-netbooks/lenovo-b-series-laptops/lenovo-b490-notebook/20205)
