---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FreeBSD 笔记本电脑安装指南 2026
translated: true
type: note
---

问题：如何在笔记本电脑上安装 FreeBSD？

回答：

这里是一个在现代笔记本电脑上安装 **FreeBSD** 的实用分步指南（截至 2026 年初，涵盖 FreeBSD 14.3 或 FreeBSD 15.0）。

### 开始前 – 重要的笔记本电脑注意事项

FreeBSD 在许多 ThinkPads、一些 Dell Latitudes/Precisions 和 Framework 笔记本电脑上运行得非常好。在许多其他现代笔记本电脑上，您可能会遇到这些常见挑战：

- Wi-Fi 通常需要额外配置（尤其是 Intel AX2xx / BE2xx 系列）
- Function keys / brightness / touchpad 有时需要调整
- Hybrid GPU 笔记本电脑（Intel + NVIDIA/AMD）需要仔细选择驱动程序
- 电池续航通常比 Linux/Windows 差

首先检查兼容性：

- 查询您的确切 Wi-Fi 芯片 → 搜索 "FreeBSD [您的 Wi-Fi 型号] iwlwifi OR iwm OR ath10k"
- 查看 FreeBSD 14.2 / 14.3 / 15.0 的 Hardware Notes
- Framework 笔记本电脑和许多 ThinkPads 具有最佳的社区支持

### 分步安装

1. **下载正确的镜像**  
   前往 → https://www.freebsd.org/where/  
   2026 年笔记本电脑的推荐选择：

   - **memstick.img**（最常见）→ 写入 ≥8 GB USB
   - FreeBSD-15.0-RELEASE-amd64-memstick.img     （如果 15.0 已发布）
   - 或 FreeBSD-14.3-RELEASE-amd64-memstick.img

   同时下载 **CHECKSUM.SHA256** 文件并验证。

2. **创建可引导 USB**  
   - **Linux / FreeBSD / macOS**：`dd if=FreeBSD-*.img of=/dev/sdX bs=1M status=progress`
   - **Windows**：使用 Rufus（DD Image 模式）或 balenaEtcher

3. **准备笔记本电脑 BIOS/UEFI**  
   - 进入 BIOS（通常是 F2、Del、F12、Esc）
   - **禁用** Secure Boot
   - 设置 **UEFI** 模式（在 2025 年后几乎总是更好）
   - 将 USB 设置为首选启动设备，或使用一次性启动菜单（F12 / F11 / Esc）

4. **启动安装程序**  
   插入 USB → 重启 → 从启动菜单选择 USB  
   您应该看到 FreeBSD loader → 按 Enter（或等待）→ 选择 **Install**

5. **跟随 bsdinstall 菜单**（基于文本的安装程序）

   | 菜单                     | 笔记本电脑的推荐选择                                 | 备注 |
   |--------------------------|-----------------------------------------------------|------|
   | Keymap                   | Belgian / Spanish / Swedish / ... 或默认 US         |      |
   | Hostname                 | mylaptop / thinkpad / etc.                          |      |
   | Distribution Set         | **ports** + **src**（以后非常有用）                 | 至少 base + kernel + lib32 |
   | Partitioning             | **Auto (ZFS)** 或 **Auto (UFS)**                    | 如果 ≥16 GB RAM，则 ZFS 更好 |
   | Pool Type (ZFS)          | stripe（单盘）或 mirror（如果 2+ 盘）                |      |
   | Encryption               | 通常 **Yes**（GELI）– 现在在安装程序中非常容易      | 强烈推荐在笔记本电脑上使用 |
   | Root password            | 强密码                                             |      |
   | Network (during install) | 如果可能，尝试有线 Ethernet                         | Wi-Fi 通常尚未就绪 |
   | Time Zone                | 您的地区 / 城市                                     |      |
   | System Configuration     | 如果需要远程访问，则启用 **sshd**                   |      |
   | Final Configuration      | 通常对所有默认值选择 **Yes**                        |      |

6. **完成并重启**  
   在提示时移除 USB → 系统应启动到 FreeBSD 控制台（黑色屏幕带文本登录）

### 首次启动后 – 使笔记本电脑可用

1. **立即更新系统**

   ```shell
   freebsd-update fetch install
   shutdown -r now
   ```

   （或如果使用 git src：`pkg install git` → 遵循手册进行 src 更新）

2. **安装二进制包管理器 (pkg)**

   ```shell
   pkg update && pkg upgrade
   ```

3. **安装桌面环境**（流行选择之一）

   ```shell
   # KDE Plasma（2025–2026 年最精致）
   pkg install kde5 sddm
   sysrc sddm_enable="YES"
   sysrc dbus_enable="YES"

   # 或 GNOME
   pkg install gnome gdm
   sysrc gdm_enable="YES"
   sysrc dbus_enable="YES"

   # 或轻量级 XFCE
   pkg install xfce xfce4-goodies slim
   sysrc slim_enable="YES"
   ```

4. **启用图形**（最常见情况）

   - Intel → 通常自动检测（`drm-kmod`）
   - AMD   → `pkg install drm-kmod`
   - NVIDIA → `pkg install nvidia-driver` 或 `nvidia-driver-libs`

   ```shell
   sysrc kld_list+="i915kms"      # Intel 新芯片
   # 或
   sysrc kld_list+="amdgpu"       # AMD
   ```

5. **Wi-Fi – 许多笔记本电脑上最难的部分**

   2025–2026 年最常见的驱动程序：

   - `iwlwifi`   Intel AX/BE 系列（FreeBSD 15 中成功几率最高）
   - `iwm`       较旧的 Intel AC
   - `ath10k` / `rtw88` / `rge`   各种 Realtek & Atheros

   示例（Intel AX210/AX211）：

   ```shell
   pkg install wpa_supplicant
   sysrc wlans_iwlwifi0="wlan0"
   sysrc ifconfig_wlan0="WPA SYNCDHCP"
   ```

   然后创建/编辑 `/etc/wpa_supplicant.conf`

6. **电源管理和笔记本电脑特定调整**

   ```shell
   sysrc powerd_enable="YES"
   sysrc powerd_flags="-a adaptive -b adaptive -i 85"
   pkg install acpi-thinkpad   # ThinkPad 用户
   ```

### 快速总结 – 2026 年的推荐路径

- ThinkPad 或 Framework → FreeBSD 15 memstick + ZFS + KDE Plasma
- 现代 Intel Wi-Fi 笔记本电脑 → 希望 15.0 中有良好的 iwlwifi 支持
- 没有良好 Wi-Fi 支持 → 计划在头几天使用 USB-C Ethernet / 手机共享网络

祝好运！

参考资料：  

- [FreeBSD Handbook – Installing FreeBSD](https://docs.freebsd.org/en/books/handbook/bsdinstall)
- [FreeBSD download page](https://www.freebsd.org/where)
- [FreeBSD Foundation – Getting Started](https://freebsdfoundation.org/resource/getting-started-with-freebsd)
- [FreeBSD on Framework guide (community repo)](https://github.com/FrameworkComputer/freebsd-on-framework)