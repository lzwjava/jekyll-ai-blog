---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 联想笔记本安装 OpenWrt 路由器指南
translated: true
type: note
---

问题：如何将近期能运行 Linux Mint Cinnamon 的旧款 Lenovo 笔记本（i5 处理器，8GB RAM，500GB 硬盘）安装 OpenWrt，以将其转变为软路由？（可能包括 ImmortalWrt 选项）

回答：

是的 —— 您的 Lenovo 笔记本（i5 + 8GB RAM + 500GB 硬盘）**非常适合**运行 OpenWrt 作为高性能软路由。它的性能将超越几乎所有消费级路由器，特别是在处理 VPN/proxy (Clash/OpenClash)、SQM QoS、多吉比特路由、运行大量 packages 等任务时。

**2026 年的两个主要选择：**
- **官方 OpenWrt** → 更稳定、上游支持、非常可靠（推荐大多数人使用）
- **ImmortalWrt** → 在中国非常流行的 fork，默认包含更多 proxy 相关的 packages，有一些额外的优化，但不够“原生”

对于初学者，建议从 **官方 OpenWrt 24.10.x** (stable) 开始，或者如果您想要最新特性，可以使用最新的 snapshot。

### 分步安装指南（最常用且推荐的方法）

#### 1. 下载正确的镜像
- 访问：https://downloads.openwrt.org/
- 选择 stable → releases → 24.10.5（或最新的 24.10.x）→ targets → x86 → 64
- 推荐文件：**openwrt-x86-64-generic-ext4-combined-efi.img.gz**  
  （这是 EFI 版本 —— 几乎所有 2010 年以后的笔记本都使用 UEFI。您最近安装过 Linux Mint 证明 UEFI 是可以工作的。）

如果您 BIOS 仅支持 legacy/CSM（在 i5 笔记本上非常罕见），请改用 non-efi 版本。

对于 ImmortalWrt（如果您偏好内置更多 proxy 插件的针对中文环境优化的版本）：
- 访问：https://immortalwrt.org/ 或其下载页面
- 选择 x86_64 target → 类似的 ext4-combined-efi 镜像

#### 2. 准备 USB 闪存盘（≥4GB，8GB+ 更好）
您需要将镜像直接写入 USB —— 这将成为“live/install”介质。

工具（任选其一）：
- **Windows**: 使用 Rufus (https://rufus.ie/) — 选择 DD Image 模式
- **Linux**（您已经有 Linux Mint）：使用 balenaEtcher、GNOME Disks 或命令行 `dd`
- **任何操作系统**: 如果您只是复制 .img 文件，Ventoy（多启动 USB）也行

Linux Mint 中的命令行示例：
```bash
# 如果需要，先解压
gunzip openwrt-....img.gz

# 查找您的 USB 设备（务必小心！！）
lsblk   # 例如 /dev/sdb（绝对不要选 /dev/sda，那是你的笔记本硬盘！）

# 写入镜像（将 sdb 替换为您的 USB 设备名）
sudo dd if=openwrt-x86-64-generic-ext4-combined-efi.img of=/dev/sdb bs=4M status=progress conv=fsync
```

#### 3. 在 Lenovo 笔记本上从 USB 启动
- 插入 USB
- 重启笔记本
- 进入 BIOS/BOOT 菜单（通常是 F2, F12, Fn+F2, Del, 或某些 Lenovo 上的 Novo 按钮）
- 将 USB 设置为第一启动项（或选择一次性启动菜单）
- 如果 Secure Boot 导致无法启动，请将其禁用（大多数 OpenWrt 镜像未签名 —— 这在 x86 上很常见）
- 保存并退出 → 应该会进入 OpenWrt console（黑屏白字）

#### 4. 安装到内部 500GB 硬盘
从 USB 启动后（你会看到 OpenWrt 登录提示 —— 以 root 身份登录，无密码）：

识别您的内部硬盘：
```bash
lsblk   # 通常是 /dev/sda（500GB 大小）
# 或者使用 fdisk -l
```

将 OpenWrt 写入（安装）到内部硬盘 —— 这将**清除 500GB 驱动器上的所有内容**！
```bash
# 选项 A：简单的一行指令（最常用）
zcat /dev/sr0/openwrt-*.img.gz | dd of=/dev/sda bs=4M status=progress   # 如果镜像在 USB 上仍为压缩格式

# 选项 B：如果已经在 USB 上解压
dd if=/path/to/openwrt-....img of=/dev/sda bs=4M status=progress conv=fsync
```

dd 完成后：
```bash
sync
reboot
```

重启前移除 USB。

#### 5. 首次启动与基础设置
- 笔记本从内部硬盘启动进入 OpenWrt
- 将网线从笔记本的 LAN 端口连接到您的主路由器/调制解调器（这将成为 WAN）
- 将您的 PC/手机连接到**另一个**以太网端口（如果有的话），或者使用 Wi-Fi（如果您的笔记本 Wi-Fi 网卡受支持）
- 从另一台设备访问：http://192.168.1.1
- 立即设置 root 密码（LuCI/web GUI 必需）
- 如果缺少 LuCI，请安装它（OpenWrt x86 镜像通常已包含，但请确认）：
  ```bash
  opkg update
  opkg install luci
  ```
- 现在可以通过 http://192.168.1.1 访问完整的 Web 界面

#### 6. 配置为路由器
- Network → Interfaces
  - WAN: 设置为 DHCP client（或者如果您的 ISP 需要，则设置为 PPPoE）
  - LAN: 保持 192.168.1.1/24
- Firewall: 初始保持默认即可
- 对于 Wi-Fi: 如果需要，请安装 wireless driver（大多数 Intel Wi-Fi 网卡配合 iwlwifi 即可工作）
  ```bash
  opkg update
  opkg install kmod-iwlwifi luci-app-statistics  # 示例
  ```
- 然后安装您喜欢的 packages (OpenClash, PassWall, AdGuard Home, SQM 等)

### 提示与警告
- 备份重要数据 —— 安装过程会清空 500GB 硬盘！
- 初始设置建议使用以太网（比 Wi-Fi 更可靠）
- 笔记本 Wi-Fi 通常可以作为您的 2.4/5GHz AP —— 覆盖能力非常强
- 功耗比真正的路由器高（约 15-40W 对比 5-12W），但如果不在意的话，24/7 运行也没问题
- 为了更好的 I/O，如果需要，可以通过 mini-PCIe 或 USB 添加多端口以太网卡
- ImmortalWrt 的安装过程几乎完全相同 —— 只是下载链接不同

您的 i5 + 8GB 配置可以轻松处理千兆以上的速度、全屋全量的 VPN/proxy 流量以及多种 services。

参考资料：

- [OpenWrt Wiki - OpenWrt on x86 hardware (PC / VM / server)](https://openwrt.org/docs/guide-user/installation/openwrt_x86)
- [OpenWrt Downloads page](https://downloads.openwrt.org/)
- [Example guide using dd on x86](https://gist.github.com/pjobson/3584f36dadc8c349fac9abf1db22b5dc)
- [ImmortalWrt official site (for alternative builds)](https://immortalwrt.org/)