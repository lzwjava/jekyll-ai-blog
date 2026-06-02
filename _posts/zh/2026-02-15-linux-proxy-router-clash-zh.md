---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 Clash 配置的 Linux 代理路由器
translated: true
type: note
---

Question: 在一台安装了 Linux Mint 的笔记本电脑（可能是 2010-2012 年左右的老旧 ThinkPad）上，我可以使用一个 Ethernet 端口作为 Internet 输入，并使用一个 USB-to-Ethernet adapter 作为输出，来运行 Clash 服务并将其作为家庭网络中的全局 Proxy 路由器吗？

Answer:

是的，这是可行的，而且这是将旧笔记本电脑通过 Clash 变成简单的有线 Proxy 路由器的一种非常常见的方法。

### 典型的工作设置（最可靠的方法）

1. **Network interfaces**
   - eth0 (内置 Ethernet) → 连接到你的主 Modem/Router (获取真实的 Internet)
   - eth1 (USB → Ethernet adapter) → 连接到 Switch 或直接连接到其他需要通过 Proxy 的设备

2. **你想要的流量走向**

   ```
   Modem ── eth0 ── [运行 Clash 的 Linux Mint 笔记本] ── eth1 ── 你的设备 / Switch
   ```

3. **你需要在 Linux Mint 上配置的内容**

   **A. 开启 IP forwarding**

   ```bash
   sudo sysctl -w net.ipv4.ip_forward=1
   # 使其永久生效
   echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
   sudo sysctl -p
   ```

   **B. NAT / Masquerade 出站流量 (以便客户端可以通过你的笔记本访问 Internet)**

   ```bash
   sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   # 或者使用 nftables (较新版本的 Mint)
   sudo nft add rule ip nat postrouting oifname "eth0" masquerade
   ```

   **C. 确保 USB-Ethernet 获取不同网段的 IP**
   两种常见方法：

   **选项 1 – 简单的 Static IP (推荐初学者使用)**

   ```bash
   sudo nmcli con mod "Wired connection 2" ipv4.method manual ipv4.addresses 192.168.201.1/24 ipv4.gateway "" ipv4.dns ""
   sudo nmcli con up "Wired connection 2"
   ```

   (使用 `nmcli connection show` 检查连接名称)

   **选项 2 – 在 eth1 上安装并运行一个微型 DHCP server**
   在 Mint/Ubuntu 上最流行且简单的是：`dnsmasq`

   ```bash
   sudo apt update
   sudo apt install dnsmasq
   ```

   最小化配置 `/etc/dnsmasq.d/custom.conf`：

   ```
   interface=eth1
   dhcp-range=192.168.201.50,192.168.201.150,12h
   dhcp-option=3,192.168.201.1      # gateway = 笔记本自身
   dhcp-option=6,192.168.201.1      # DNS = 笔记本 (稍后会进行转发)
   ```

   然后执行 `sudo systemctl restart dnsmasq`

   **D. 将所有客户端流量路由通过 Clash**
   大多数 Clash 实现 (Clash for Linux, Clash Meta / Mihomo, Clash Verge CLI 等) 支持两种主要模式：

   - **TUN mode** (实现全透明 Proxy 的首选)
     - 启动 Clash 并启用 TUN (`allow-lan: true`, `tun: enable`)
     - 确保 Clash 创建了 `utun` / `clash0` 接口
     - 添加 Policy routing，使来自 eth1 的流量进入 Clash：

       ```bash
       ip rule add from 192.168.201.0/24 table 100
       ip route add default via 192.168.201.1 dev eth1 table 100
       # 或者更简单的方式 – 许多 Clash 软件包在 TUN mode 下会自动处理这些
       ```

   - **Redirect / TProxy mode** (iptables/nftables 重定向)
     - 使用 Clash 内置的 redir-host 或 fake-ip + iptables REDIRECT 或 TPROXY 规则
     - 最用户友好的方式：许多用于 Linux 的 Clash Meta / Mihomo 软件包都包含用于此操作的辅助脚本

   **E. 让客户机使用你的笔记本作为 Gateway**
   - 将设备连接到 eth1 网络
   - 它们应该通过 DHCP 获取 IP (如果你运行了 dnsmasq)
   - 或者手动设置 Gateway = 192.168.201.1 和 DNS = 192.168.201.1 (如果你愿意，也可以是 8.8.8.8)

### 快速总结 – 2025/2026 年在旧硬件上最稳定的组合

- Clash Meta core (mihomo) 或 Clash Verge 服务，运行在 **TUN mode**
- 内置 eth0 = WAN (通过 Modem 的 DHCP 获取 Internet)
- USB-Ethernet = LAN (Static 192.168.201.1/24 或 dnsmasq)
- 在 eth0 上开启 IP forwarding + 简单的 Masquerade
- 客户端将 Gateway 指向 192.168.201.x 网段下的笔记本 IP

### 在旧 ThinkPad + Linux Mint 上需要注意的事项

- 非常旧的 Kernel 有时对 USB-Ethernet driver 的稳定性较差 → 尝试不同的 USB-Ethernet 芯片 (通常 AX88179, RTL8153 的支持最好)
- 在处理非常高的吞吐量时，旧硬件可能会在 Clash + Encryption 方面感到吃力
- 如果 RAM ≤ 4 GB，请使用轻量级的 Clash core，并避免使用消耗内存的 Clash Meta 插件

这套设置作为小型家庭全局 Proxy 路由器效果很好。

References:

- 此说明不需要特定参考资料 (常见的 Linux 连网 + Clash 知识)
