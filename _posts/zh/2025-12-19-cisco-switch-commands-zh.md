---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 常见思科交换机命令
translated: true
type: note
---

网络中交换机常用的命令有哪些？

在网络中，**交换机**主要是二层设备，根据MAC地址转发帧。最常用的命令是指受管交换机上的命令行界面（CLI），其中**Cisco IOS**是主导平台，因为它在企业网络中广泛使用。许多其他厂商（例如Aruba，一些Dell型号）提供“类Cisco”的CLI以实现兼容性，但在Juniper Junos或HP Comware等平台上的语法则有显著差异。

下面是**常用的Cisco交换机命令**的分类列表，包括其用途和示例。这些对于配置、监控和故障排除至关重要。

### CLI 模式

- `enable` — 进入特权EXEC模式（从用户EXEC模式）。
- `configure terminal` (或 `conf t`) — 进入全局配置模式。
- `exit` or `end` — 退出当前模式。
- `interface <interface>` (例如，`interface GigabitEthernet1/0/1`) — 进入接口配置模式。
- `interface range <range>` (例如，`interface range Gi1/0/1 - 24`) — 同时配置多个端口。

### 基本配置和管理

- `hostname <name>` — 设置交换机主机名。
- `enable secret <password>` — 设置加密的特权模式密码。
- `line console 0` → `password <pass>` → `login` — 保护控制台访问。
- `line vty 0 15` → `password <pass>` or `login local` — 保护Telnet/SSH访问。
- `service password-encryption` — 加密所有明文密码。
- `banner motd # <message> #` — 设置每日消息横幅。
- `ip default-gateway <ip>` — 设置管理默认网关（二层交换机）。

### 管理IP（用于远程访问）

- `interface vlan 1` (或其他VLAN)
- `ip address <ip> <mask>`
- `no shutdown`

### VLAN 配置

- `vlan <id>` — 创建VLAN（全局配置）。
- `name <vlan-name>` — 命名VLAN。
- `interface <port>` → `switchport mode access` — 将端口设置为接入端口。
- `switchport access vlan <id>` — 分配接入VLAN。
- `interface <port>` → `switchport mode trunk` — 将端口设置为中继端口。
- `switchport trunk allowed vlan <list>` — 限制中继上允许的VLAN。
- `switchport trunk native vlan <id>` — 设置中继上的本地VLAN。

### 端口配置和安全

- `interface <port>` → `description <text>` — 添加端口描述。
- `interface <port>` → `shutdown` / `no shutdown` — 禁用/启用端口。
- `interface <port>` → `switchport port-security maximum <num>` — 限制MAC地址数量。
- `switchport port-security violation {protect|restrict|shutdown}` — 违反安全策略时的动作。
- `switchport port-security mac-address sticky` — 动态学习MAC地址。

### 监控和显示命令

- `show running-config` (或 `sh run`) — 显示当前配置。
- `show startup-config` — 显示已保存的配置。
- `show vlan brief` — 列出VLAN和分配的端口。
- `show interfaces status` — 端口状态摘要。
- `show interfaces <port>` — 详细端口信息。
- `show mac address-table` (或 `show mac-address-table`) — MAC地址表条目。
- `show cdp neighbors` — 连接的Cisco设备。
- `show version` — IOS版本和硬件信息。
- `show spanning-tree` — 生成树协议状态。

### 保存和其他实用程序

- `copy running-config startup-config` (或 `wr`) — 保存配置。
- `reload` — 重启交换机。
- `ping <ip>` — 测试连接。
- `traceroute <ip>` — 跟踪路径。

这些命令构成了大多数交换机管理任务的基础。对于非Cisco交换机，VLAN和端口模式等概念相似，但语法不同（例如，Juniper使用分层结构中的“set”命令）。

参考资料：

- [https://www.comparitech.com/net-admin/cisco-cli-switch-command-cheat-sheet/](https://www.comparitech.com/net-admin/cisco-cli-switch-command-cheat-sheet/)
- [https://netwrix.com/en/resources/guides/cisco-commands-cheat-sheet-for-device-configuration/](https://netwrix.com/en/resources/guides/cisco-commands-cheat-sheet-for-device-configuration/)
- [https://www.geeksforgeeks.org/computer-networks/cisco-switch-configuration-basic-commands/](https://www.geeksforgeeks.org/computer-networks/cisco-switch-configuration-basic-commands/)
- [https://www.networkstraining.com/cisco-show-commands/](https://www.networkstraining.com/cisco-show-commands/)
- [https://www.computernetworkingnotes.com/ccna-study-guide/basic-switch-configuration-guide-with-examples.html](https://www.computernetworkingnotes.com/ccna-study-guide/basic-switch-configuration-guide-with-examples.html)
