---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 华为VRP命令行视图简介
translated: true
type: note
---

Question: Provide a comprehensive introduction to the different views in Huawei's Versatile Routing Platform (VRP).

Answer:

### Overview of Views in Huawei VRP

Huawei 的 Versatile Routing Platform (VRP) 是用于 Huawei 网络设备（如 routers 和 switches）的操作系统。它的特点是采用分层的 command-line interface (CLI) 结构，并组织成不同的 **views**。每个 view 提供了与特定任务相关的特定命令集，从而增强了安全性、组织性和管理便捷性。不同的 views 通过不同的 prompts 来标识（例如：User View 为 `< >`，System View 为 `[ ]`）。

在不同 views 之间导航需要使用特定命令（例如：使用 `system-view` 进入 System View），你可以通过 `return` 命令 (Ctrl+Z) 或 `quit` 返回到之前的 view。

### 1. User View (<Huawei>)

- **Prompt**: `< >` (例如：`<Huawei>`)
- **Access**: 这是登录成功后（通过 console、Telnet 或 SSH）默认进入的 view。
- **Purpose**: 主要用于 **monitoring**（监控）和 **basic operational tasks**（基础操作任务）。
- **Allowed Commands**:
  - Diagnostic tools: `ping`、`tracert`
  - Display commands: `display version`、`display current-configuration`、`display ip interface brief`
  - Basic operations: 重启 (`reboot`)、文件管理（有限权限）
- **Restrictions**: 不允许进行任何 configuration 修改。尝试输入配置命令会导致错误。
- **Use Case**: 快速检查设备状态、测试连通性，或在不冒修改配置风险的情况下查看信息。

### 2. System View ([Huawei])

- **Prompt**: `[ ]` (例如：`[Huawei]`)
- **Access**: 在 User View 中使用 `system-view` 命令进入。
- **Purpose**: **global and basic device configuration**（全局和基础设备配置）的主要 view。
- **Allowed Commands**:
  - System-wide settings: hostname (`sysname`)、时钟、语言
  - 用户管理和 AAA: local users、authentication 方式
  - VLAN configuration: `vlan batch`、`vlan 10`
  - 管理接口设置: 进入管理端口的 interface views
  - Protocol enabling: 开启 OSPF、BGP 等（全局范围）
  - 进入其他 specialized views: `interface GigabitEthernet 0/0/0`、`ospf 1` 等
- **Use Case**: 大多数常规配置任务都从这里开始，例如修改设备 hostname、创建 VLAN、配置管理 IP 或设置用户访问权限。
- **Note**: 这是通往几乎所有其他 configuration views 的入口。

### 3. Interface View

- **Prompt**: 通常为 `[Huawei-interface_type-number]` (例如：`[Huawei-GigabitEthernet0/0/1]`)
- **Access**: 在 System View 中使用 `interface <type> <number>` (例如：`interface GigabitEthernet 0/0/1`)。
- **Purpose**: 配置特定物理或逻辑接口的参数。
- **Allowed Commands**:
  - Port mode: `port link-type access/trunk/hybrid`
  - IP address assignment: `ip address 192.168.1.1 255.255.255.0`
  - Shutdown/no shutdown
  - Description、speed、duplex 设置
  - VLAN assignment（针对 access ports）: `port default vlan 10`
  - Subinterfaces: 针对 802.1Q VLAN tagging 的配置
- **Use Case**: 在路由端口上设置 IP 地址，配置交换机端口为 VLAN access/trunk 模式，或调整物理层参数。

### 4. Protocol View

- **Prompt**: 随协议而异（例如：OSPF process 1 为 `[Huawei-ospf-1]`，BGP 为 `[Huawei-bgp]`）
- **Access**: 在 System View 中输入协议命令（例如：`ospf 1`、`bgp 100`）。
- **Sub-levels**:
  - OSPF 的 Area view: `area 0` → `[Huawei-ospf-1-area-0.0.0.0]`
  - VPN instance 或其他子视图
- **Purpose**: 配置 dynamic routing protocol 参数。
- **Allowed Commands**:
  - OSPF: network statements、router ID、area types、authentication
  - BGP: neighbor statements、AS number、address families
  - 其他协议: RIP、ISIS 等
- **Use Case**: 启用和调优路由协议，以便与邻居交换路由信息。

### Additional Important Views (Commonly Used)

- **AAA View**: `[Huawei-aaa]` – 用于详细的 authentication、authorization 和 accounting 配置。
- **User-Interface View**: `[Huawei-ui-console0]` 或 `[Huawei-ui-vty0-4]` – 配置 console 或 VTY (Telnet/SSH) 线路设置。
- **Security View**: 用于防火墙策略、IPSec 等。
- **MPLS View**: 用于 MPLS 相关配置。

### Key Principles

- **Hierarchy**: User View → System View → Specialized Views (interface, protocol, etc.)。
- **Command Availability**: 命令具有上下文敏感性；每个 view 中仅提供相关的命令。
- **Safety**: 低层级 view 中的受限访问可以防止意外的配置更改。
- **Navigation Tips**:
  - `return` 或 Ctrl+Z: 从任何地方跳回 User View。
  - `quit`: 返回上级 view。
  - 所有 view 中都提供 Tab 键补全和 `?` 帮助。

理解这些 views 对于高效、安全地配置 Huawei 设备至关重要。初学者应在登录后进入 System View 开始配置，并在退出前始终使用 `commit`（在某些版本中）或 `save` 保存更改。
