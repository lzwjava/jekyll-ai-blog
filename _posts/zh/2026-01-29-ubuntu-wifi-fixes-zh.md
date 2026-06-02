---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ubuntu WiFi 适配器缺失修复
translated: true
type: note
---

**问题：** 在 Ubuntu 中，为什么有时会显示“WiFi adapter not found”，从而 Settings 中没有 WiFi 部分，导致无法连接 WiFi？

**回答：**

这是 Ubuntu（以及其他 Linux 发行版）中非常常见的问题。**"No WiFi adapter found"** 消息出现——并且 Settings 中的 WiFi 部分消失或不可用——是因为 Ubuntu 无法正确检测或使用您的无线网络适配器。以下是主要原因：

### 主要原因
1. **Missing or incorrect WiFi driver**
   许多 WiFi 芯片组（尤其是 Broadcom、Realtek、某些 Qualcomm/Atheros）默认不包含完全开源的驱动程序。
   - 如果驱动程序缺失、未加载或使用了错误的驱动 → 系统看不到可用的无线接口 → NetworkManager 隐藏 WiFi 选项。

2. **Hardware/firmware not detected at all**
   运行 `lspci | grep -i network`（针对内部 PCIe 卡）或 `lsusb`（针对 USB WiFi 适配器）。
   如果您的 WiFi 卡**没有**出现 → 内核看不到硬件（很少见，但可能发生在 suspend 后、内核更新、卡松动或硬件故障时）。

3. **Driver is loaded but NetworkManager does not recognize the interface**
   您在 `lspci` 或 `lshw -C network` 中看到卡，但 Settings 仍显示无适配器。
   这可能由于驱动程序有 bug、rfkill 阻塞或配置错误引起。

4. **Fast Startup / hybrid shutdown from Windows (dual-boot)**
   Windows 的 Fast Startup 会让 WiFi 卡处于奇怪的关电状态 → Linux 无法正确唤醒它。

5. **rfkill hardware or software block**
   WiFi 可能被硬阻塞（物理开关 / Fn 键）或软阻塞。

6. **Kernel regression or incompatible version**
   内核更新后（或安装较新 Ubuntu），之前工作的芯片组停止工作。

### Quick Troubleshooting Steps (in order of priority)
1. **Check if the hardware is seen**
   打开 Terminal 并运行：
   ```
   lspci -nnk | grep -iA3 net
   ```
   或
   ```
   lshw -C network
   ```
   查找 "Wireless"、"WiFi"、"802.11"、"Network controller"。注意 vendor:device ID（例如 14e4:4360 = Broadcom）。

2. **Check rfkill status**
   ```
   rfkill list all
   ```
   如果 "Hard blocked: yes" → 按物理 WiFi 键或 Fn+F 键组合。
   如果 "Soft blocked: yes" → 运行 `rfkill unblock wifi`。

3. **Try to enable WiFi via terminal**
   ```
   nmcli radio wifi on
   nmcli device wifi list
   ```
   如果看到网络 → 驱动程序正常，但 GUI 失败。

4. **Install proprietary drivers (most common fix)**
   - 临时通过 Ethernet、手机 USB tethering 或其他方式连接互联网。
   - 打开 **Software & Updates** → **Additional Drivers** 选项卡。
   - 选择推荐的 WiFi 驱动程序（例如 Broadcom 的 bcmwl-kernel-source，或 Realtek 的相应驱动）。
   - 应用更改 → 重启。

5. **Dual-boot Windows fix**
   启动进入 Windows → 禁用 **Fast Startup**（控制面板 → 电源选项 → “选择电源按钮的功能” → 取消选中“启用快速启动”）→ 完全关机（不要重启）→ 启动 Ubuntu。

6. **Other quick commands people often use**
   ```
   sudo apt update
   sudo apt install --reinstall network-manager
   sudo modprobe -r <driver_name> && sudo modprobe <driver_name>   # e.g. rtl8821ae, rtw89_8852be
   ```

### 总结
在大多数情况下（尤其是配备 Broadcom 或 Realtek 芯片的笔记本电脑），根本原因是**缺少专有驱动程序**。当 NetworkManager 看到零个无线设备时，Ubuntu 会隐藏 Settings 中的 WiFi 部分。一旦通过 Additional Drivers + 互联网安装工作驱动程序，WiFi 部分就会重新出现，您就可以正常连接。

如果您分享 `lspci -nnk | grep -iA3 net` 的输出，或告诉我们您的笔记本型号 / WiFi 芯片组，通常可以给出确切的修复命令。

**参考资料：**

- [Ubuntu Community Wireless Troubleshooting Guide](https://help.ubuntu.com/community/WifiDocs/WirelessTroubleShootingGuide)
- [ItsFOSS: Fix No Wireless Network in Ubuntu](https://itsfoss.com/fix-no-wireless-network-ubuntu)
- [Ask Ubuntu: No Wi-Fi Adapter Found threads](https://askubuntu.com/questions/tagged/wifi+no-wifi-adapter-found)
