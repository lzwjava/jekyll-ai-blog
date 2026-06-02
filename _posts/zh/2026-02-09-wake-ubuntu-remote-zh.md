---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 远程开启无电源连接的 Ubuntu
translated: true
type: note
---

问题：在不保持电脑常开的情况下，远程访问 Ubuntu 的解决方案有哪些？

回答：

要在不让 Ubuntu 电脑始终保持开机状态（为了省电）的情况下，从您的 MacBook Air M2 远程访问它，核心挑战在于实现按需唤醒并确保连接的安全性。这通常需要将 Wake-on-LAN (WoL) 与 SSH、RDP 或 VNC 等远程访问协议相结合。WoL 允许您通过网络发送“魔法封包 (magic packet)”来将处于睡眠或关机状态的 PC 唤醒，但这需要 PC 的主板支持该功能（大多数现代主板都支持）并进行正确配置。

下面，我将根据可靠的方法概述详细的步骤方案。这些方案假设您的 Ubuntu 电脑最初在同一个家庭网络中进行设置，并且您是进行远程访问（例如从外部通过互联网）。对于外部访问，您需要通过端口转发、VPN 或第三方服务来安全地触达您的家庭网络。请务必通过使用强密码、Firewalls 并避免不必要的端口暴露来优先保证安全性。

### 1. **Wake-on-LAN (WoL) 结合 SSH 进行命令行访问**
这是最轻量且省电的选项，因为 SSH 是基于文本的，不需要图形会话。如果您主要需要通过终端在 Ubuntu 上运行命令或脚本，这是理想之选。

**步骤设置：**
- **在 Ubuntu 电脑上启用 WoL：**
  1. 进入 BIOS/UEFI（通常在启动时按 Del、F2 或 F10），并在电源管理设置下启用 "Wake-on-LAN" 或 "PCIe/PCI Wake"。保存并退出。
  2. 在 Ubuntu 上安装 ethtool 包：`sudo apt update && sudo apt install ethtool`。
  3. 识别您的网络接口（例如 enp0s3）：`ip link show`。
  4. 启用 WoL：`sudo ethtool -s <interface> wol g`（将 <interface> 替换为您的接口名称，如 enp0s3）。
  5. 设为持久化：创建一个脚本或使用 systemd。例如，编辑 `/etc/network/interfaces` 或在 `/etc/systemd/system/` 中创建一个服务文件，包含 `[Service] ExecStart=/usr/bin/ethtool -s enp0s3 wol g`。
  6. 本地测试：关闭 PC，然后在同一网络中的另一台设备上，使用 `wakeonlan` 工具（在测试机上通过 `sudo apt install wakeonlan` 安装）发送魔法封包，命令为：`wakeonlan <MAC address>`。通过 `ip link show` 获取 MAC 地址。
- **在 Ubuntu 上设置 SSH：**
  1. 安装 OpenSSH server：`sudo apt install openssh-server`。
  2. 启用并启动：`sudo systemctl enable --now ssh`。
  3. 配置 Firewall：`sudo ufw allow ssh`。
  4. 使用秘钥认证（更安全）：在 MacBook 上生成秘钥 (`ssh-keygen`)，并复制到 Ubuntu (`ssh-copy-id user@ubuntu-ip`)。
- **远程唤醒与访问：**
  - 对于远程 WoL（在家庭网络外），您无法直接通过互联网发送魔法封包。解决方案包括：
    - 使用一个低功耗的常开设备，如 Raspberry Pi（成本约 $35-50，功耗极低）作为“网关”。通过端口转发或 VPN 设置对 Pi 的 SSH 访问，然后从您的 MacBook SSH 登录 Pi 并运行 wakeonlan 命令来唤醒 Ubuntu 电脑。
    - 在路由器上设置端口转发：将 UDP 端口 9（或自定义端口）转发到 Ubuntu 电脑的广播地址（例如 192.168.1.255）。然后在您的 iPhone 上使用“WoL - Wake on Lan”之类的移动 App（因为 MacBook Air 可以根据需要通过手机热点连接）远程发送封包。注意：这会暴露您的网络，请谨慎使用。
    - 使用 WireGuard 等 VPN（免费且开销低）：在 Ubuntu、路由器（如果支持，如 OpenWRT）和 MacBook 上安装 WireGuard。先通过 VPN 连接，然后像在本地网络一样发送 WoL 封包。
  - 唤醒后：从 MacBook 终端，使用 `ssh user@ubuntu-external-ip` 连接（如果 IP 经常变动，请使用 No-IP 等动态 DNS）。
- **优点：** 资源占用极低，命令行操作安全。**缺点：** 需要初始唤醒步骤；图形访问需要额外工具如 X forwarding（例如 `ssh -X`）。

### 2. **WoL 结合 TeamViewer 或类似 GUI 工具进行完整桌面访问**
如果您需要图形化远程控制（例如使用 Ubuntu 的桌面环境），请使用集成了 WoL 功能的工具。

**使用 TeamViewer（个人免费版）的步骤设置：**
- **在 Ubuntu 上安装：**
  1. 从官方网站下载：`wget https://download.teamviewer.com/download/linux/teamviewer_amd64.deb`。
  2. 安装：`sudo dpkg -i teamviewer_amd64.deb`（使用 `sudo apt install -f` 修复依赖项）。
  3. 运行并设置无人值守访问账号。
- **在 TeamViewer 中启用 WoL：**
  1. 在 Ubuntu 的 TeamViewer 设置中，转到 Extras > Options > General > Wake-on-LAN。
  2. 配置其使用“公共地址”或网络中的另一台 PC（例如您有一台常开设备）。
  3. 确保 BIOS 中的 WoL 已按方法 1 启用。
- **在 MacBook 上安装：**
  1. 下载 macOS 版 TeamViewer 并使用同一账号登录。
- **远程访问：**
  - 在 MacBook 的 TeamViewer 中，选择 Ubuntu 设备（显示为离线），然后选择“唤醒 (Wake up)”。
  - 唤醒后，即可连接进行完整的远程桌面控制。
  - TeamViewer 自动处理 NAT/Firewalls，不需要端口转发。
- **替代方案：**
  - **AnyDesk：** 与 TeamViewer 类似，支持通过配置实现 WoL。对某些用户来说速度更快。
  - **RustDesk 结合 Tailscale：** 开源且免费。在两台机器上安装 RustDesk，使用 Tailscale（一种 Mesh VPN）进行安全的直接连接。对于 WoL，结合脚本或 App 先行唤醒（Tailscale 会让设备在虚拟层面保持“连接”）。
- **优点：** 图形界面易用，跨平台，处理远程唤醒。**缺点：** 第三方服务；潜在的隐私顾虑（尽管是端到端加密的）。

### 3. **使用 RDP/VNC 结合 Gnome 扩展进行锁定访问**
如果您更倾向于使用 Ubuntu 原生工具进行图形访问，可以设置 RDP 或 VNC，然后配合 WoL 进行唤醒。

**步骤：**
- **在 Ubuntu 上启用远程桌面 (Ubuntu 22.04+)：**
  1. 转到 Settings > Sharing > Remote Desktop > Enable。
  2. 设置用户名/密码。
  3. 实现锁定屏幕访问：安装 Gnome Extension Manager (`sudo apt install gnome-shell-extension-manager`)，然后添加 "Allow Locked Remote Desktop" 扩展。
- **MacBook 客户端：** 使用 Microsoft Remote Desktop 应用（App Store 免费提供）进行 RDP 连接。
- **使用 WoL 唤醒：** 与方法 1 相同，先唤醒，后连接。
- **对于 VNC：** 安装 vino (`sudo apt install vino`)，在设置中启用，在 MacBook 上使用 Remmina 或 Vinagre 连接。
- **优点：** 内置功能，无需额外软件。**缺点：** 安全性低于 SSH；需要手动唤醒步骤。

### 附加建议
- **电源管理：** 将 Ubuntu 配置为在闲置一段时间后挂起 (`Settings > Power`)，但要确保 WoL 在挂起状态下能正常工作（需进行测试）。
- **安全性：** 所有的远程访问都建议使用 VPN（如 WireGuard），以避免端口暴露。开启 Ubuntu Firewall (`sudo ufw enable`)。
- **节能效果：** 使用 WoL 后，PC 仅在需要时运行。Raspberry Pi 网关的功耗约为 3-5W，而 PC 待机功耗约为 50-100W。
- **测试：** 在尝试远程访问之前，先在本地网络中进行测试。
- **如果 WoL 不可行：** 考虑迁移到云端虚拟机（如使用 Ubuntu 的 AWS Lightsail，每月约 $5），但这就不属于利用您的本地硬件了。

这些方法应该能让您在床上通过 MacBook 舒适地访问电脑，同时将电费降到最低。

参考资料：

- [https://medium.com/@ryanym/cloud-is-not-free-wakeup-and-ssh-to-your-home-computer-remotely-7d4f3b37ce0](https://medium.com/@ryanym/cloud-is-not-free-wakeup-and-ssh-to-your-home-computer-remotely-7d4f3b37ce0)
- [https://www.youtube.com/watch?v=pXXzWkNkKuQ](https://www.youtube.com/watch?v=pXXzWkNkKuQ)
- [https://forums.lawrencesystems.com/t/different-ubuntu-remote-desktop-question/22472](https://forums.lawrencesystems.com/t/different-ubuntu-remote-desktop-question/22472)
- [https://tailscale.com/blog/tailscale-rustdesk-remote-desktop-access](https://tailscale.com/blog/tailscale-rustdesk-remote-desktop-access)
- [https://www.itpro.com/mobile/remote-access/368102/how-to-remote-desktop-into-ubuntu](https://www.itpro.com/mobile/remote-access/368102/how-to-remote-desktop-into-ubuntu)
