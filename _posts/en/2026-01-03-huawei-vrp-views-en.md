---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Introduction to Huawei VRP Command Views
translated: false
type: note
---

Question: Provide a comprehensive introduction to the different views in Huawei's Versatile Routing Platform (VRP).

Answer:

### Overview of Views in Huawei VRP

Huawei's Versatile Routing Platform (VRP) is the operating system used in Huawei network devices such as routers and switches. It features a hierarchical command-line interface (CLI) structure organized into different **views**. Each view provides access to a specific set of commands relevant to particular tasks, enhancing security, organization, and ease of management. Views are indicated by distinct prompts (e.g., `< >` for user view, `[ ]` for system view).

Navigating between views is done using specific commands (e.g., `system-view` to enter system view), and you can return to the previous view with the `return` command (Ctrl+Z) or `quit`.

### 1. User View (<Huawei>)
- **Prompt**: `< >` (e.g., `<Huawei>`)
- **Access**: This is the default view immediately after successful login (via console, Telnet, or SSH).
- **Purpose**: Primarily for **monitoring** and **basic operational tasks**.
- **Allowed Commands**:
  - Diagnostic tools: `ping`, `tracert`
  - Display commands: `display version`, `display current-configuration`, `display ip interface brief`
  - Basic operations: reboot (`reboot`), file management (limited)
- **Restrictions**: No configuration changes are permitted. Attempts to enter configuration commands will result in an error.
- **Use Case**: Quick checks of device status, connectivity testing, or viewing information without risking changes to the configuration.

### 2. System View ([Huawei])
- **Prompt**: `[ ]` (e.g., `[Huawei]`)
- **Access**: Enter from user view using the command `system-view`.
- **Purpose**: The main view for **global and basic device configuration**.
- **Allowed Commands**:
  - System-wide settings: hostname (`sysname`), clock, language
  - User management and AAA: local users, authentication methods
  - VLAN configuration: `vlan batch`, `vlan 10`
  - Management interface setup: entering interface views for management ports
  - Protocol enabling: enabling OSPF, BGP, etc. (globally)
  - Entering other specialized views: `interface GigabitEthernet 0/0/0`, `ospf 1`, etc.
- **Use Case**: Most routine configuration tasks start here, such as changing the device hostname, creating VLANs, configuring management IP, or setting up user access.
- **Note**: This is the gateway to almost all other configuration views.

### 3. Interface View
- **Prompt**: Usually `[Huawei-interface_type-number]` (e.g., `[Huawei-GigabitEthernet0/0/1]`)
- **Access**: From system view, use `interface <type> <number>` (e.g., `interface GigabitEthernet 0/0/1`).
- **Purpose**: Configure parameters specific to a particular physical or logical interface.
- **Allowed Commands**:
  - Port mode: `port link-type access/trunk/hybrid`
  - IP address assignment: `ip address 192.168.1.1 255.255.255.0`
  - Shutdown/no shutdown
  - Description, speed, duplex settings
  - VLAN assignment (for access ports): `port default vlan 10`
  - Subinterfaces: for 802.1Q VLAN tagging
- **Use Case**: Setting up IP addresses on routed ports, configuring switch ports for VLAN access/trunking, or tuning physical layer parameters.

### 4. Protocol View
- **Prompt**: Varies by protocol (e.g., `[Huawei-ospf-1]` for OSPF process 1, `[Huawei-bgp]` for BGP)
- **Access**: From system view, enter the protocol command (e.g., `ospf 1`, `bgp 100`).
- **Sub-levels**:
  - Area view for OSPF: `area 0` → `[Huawei-ospf-1-area-0.0.0.0]`
  - VPN instance or other sub-views
- **Purpose**: Configure dynamic routing protocol parameters.
- **Allowed Commands**:
  - OSPF: network statements, router ID, area types, authentication
  - BGP: neighbor statements, AS number, address families
  - Other protocols: RIP, ISIS, etc.
- **Use Case**: Enabling and tuning routing protocols to exchange routes with neighbors.

### Additional Important Views (Commonly Used)
- **AAA View**: `[Huawei-aaa]` – For detailed authentication, authorization, and accounting configurations.
- **User-Interface View**: `[Huawei-ui-console0]` or `[Huawei-ui-vty0-4]` – Configure console or VTY (Telnet/SSH) line settings.
- **Security View**: For firewall policies, IPSec, etc.
- **MPLS View**: For MPLS-related configurations.

### Key Principles
- **Hierarchy**: User view → System view → Specialized views (interface, protocol, etc.).
- **Command Availability**: Commands are context-sensitive; only relevant commands are available in each view.
- **Safety**: Restricted access in lower views prevents accidental configuration changes.
- **Navigation Tips**:
  - `return` or Ctrl+Z: Jump back to user view from anywhere.
  - `quit`: Return to the parent view.
  - Tab completion and `?` help are available in all views.

Understanding these views is essential for efficient and safe configuration of Huawei devices. Beginners should start configurations in system view after login, and always save changes with `commit` (in some versions) or `save` before logout.
