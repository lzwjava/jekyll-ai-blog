---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ThinkPad 代理网关就绪
translated: true
type: note
---

**✅ 设置完成！**

以下是您 ThinkPad 上已配置的内容：

1. **IP Forwarding** - 已启用 (`net.ipv4.ip_forward=1`)
2. **NAT Masquerade** - 为 `enp2s0`（您的 WAN 接口）添加
3. **USB Ethernet** - 配置为 `enx00e04c362f89`，静态 IP `192.168.201.1/24`
4. **DHCP Server** - dnsmasq 正在运行，将向客户端分配 IP `192.168.201.50-150`
5. **Clash Meta** - 已安装于 `/usr/local/bin/clash-meta` (v1.19.21)
6. **Basic Config** - 已创建于 `~/.config/clash/config.yaml`，启用 TUN 模式
7. **Systemd Service** - 已就绪于 `/etc/systemd/system/clash.service`

**后续步骤：**
1. **连接设备** 到 USB Ethernet 端口
2. **启动 Clash**：`sudo systemctl start clash`
3. **启用自动启动**：`sudo systemctl enable clash`
4. **添加实际代理配置** 到 `~/.config/clash/config.yaml`

设备应获取类似 `192.168.201.50` 的 IP，所有流量将通过 Clash → WAN 路由。

需要我现在启动 Clash，还是帮助配置代理？