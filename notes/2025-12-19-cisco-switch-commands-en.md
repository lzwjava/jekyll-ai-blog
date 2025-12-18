---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Common Cisco Switch Commands
translated: false
type: note
---

Question: What are common commands in switches in networking?

Answer: 

In networking, **switches** are primarily Layer 2 devices that forward frames based on MAC addresses. The most common commands refer to the Command Line Interface (CLI) on managed switches, with **Cisco IOS** being the dominant platform due to its widespread use in enterprise networks. Many other vendors (e.g., Aruba, some Dell models) offer "Cisco-like" CLIs for compatibility, but syntax varies significantly on platforms like Juniper Junos or HP Comware.

Below is a categorized list of **common Cisco switch commands**, including their purpose and examples. These are essential for configuration, monitoring, and troubleshooting.

### CLI Modes
- `enable` — Enter privileged EXEC mode (from user EXEC).
- `configure terminal` (or `conf t`) — Enter global configuration mode.
- `exit` or `end` — Exit current mode.
- `interface <interface>` (e.g., `interface GigabitEthernet1/0/1`) — Enter interface configuration mode.
- `interface range <range>` (e.g., `interface range Gi1/0/1 - 24`) — Configure multiple ports at once.

### Basic Configuration and Management
- `hostname <name>` — Set the switch hostname.
- `enable secret <password>` — Set encrypted privileged mode password.
- `line console 0` → `password <pass>` → `login` — Secure console access.
- `line vty 0 15` → `password <pass>` or `login local` — Secure Telnet/SSH access.
- `service password-encryption` — Encrypt all plaintext passwords.
- `banner motd # <message> #` — Set Message of the Day banner.
- `ip default-gateway <ip>` — Set default gateway for management (Layer 2 switches).

### Management IP (for remote access)
- `interface vlan 1` (or other VLAN)
- `ip address <ip> <mask>`
- `no shutdown`

### VLAN Configuration
- `vlan <id>` — Create a VLAN (global config).
- `name <vlan-name>` — Name the VLAN.
- `interface <port>` → `switchport mode access` — Set port as access port.
- `switchport access vlan <id>` — Assign access VLAN.
- `interface <port>` → `switchport mode trunk` — Set port as trunk.
- `switchport trunk allowed vlan <list>` — Restrict allowed VLANs on trunk.
- `switchport trunk native vlan <id>` — Set native VLAN on trunk.

### Port Configuration and Security
- `interface <port>` → `description <text>` — Add port description.
- `interface <port>` → `shutdown` / `no shutdown` — Disable/enable port.
- `interface <port>` → `switchport port-security maximum <num>` — Limit MAC addresses.
- `switchport port-security violation {protect|restrict|shutdown}` — Action on violation.
- `switchport port-security mac-address sticky` — Learn MAC dynamically.

### Monitoring and Show Commands
- `show running-config` (or `sh run`) — Display current configuration.
- `show startup-config` — Display saved configuration.
- `show vlan brief` — List VLANs and assigned ports.
- `show interfaces status` — Port status summary.
- `show interfaces <port>` — Detailed port info.
- `show mac address-table` (or `show mac-address-table`) — MAC table entries.
- `show cdp neighbors` — Connected Cisco devices.
- `show version` — IOS version and hardware info.
- `show spanning-tree` — Spanning Tree Protocol status.

### Saving and Other Utilities
- `copy running-config startup-config` (or `wr`) — Save configuration.
- `reload` — Reboot the switch.
- `ping <ip>` — Test connectivity.
- `traceroute <ip>` — Trace path.

These commands form the foundation for most switch management tasks. For non-Cisco switches, concepts like VLANs and port modes are similar, but syntax differs (e.g., Juniper uses "set" commands in a hierarchical structure).

References:  

- [https://www.comparitech.com/net-admin/cisco-cli-switch-command-cheat-sheet/](https://www.comparitech.com/net-admin/cisco-cli-switch-command-cheat-sheet/)
- [https://netwrix.com/en/resources/guides/cisco-commands-cheat-sheet-for-device-configuration/](https://netwrix.com/en/resources/guides/cisco-commands-cheat-sheet-for-device-configuration/)
- [https://www.geeksforgeeks.org/computer-networks/cisco-switch-configuration-basic-commands/](https://www.geeksforgeeks.org/computer-networks/cisco-switch-configuration-basic-commands/)
- [https://www.networkstraining.com/cisco-show-commands/](https://www.networkstraining.com/cisco-show-commands/)
- [https://www.computernetworkingnotes.com/ccna-study-guide/basic-switch-configuration-guide-with-examples.html](https://www.computernetworkingnotes.com/ccna-study-guide/basic-switch-configuration-guide-with-examples.html)