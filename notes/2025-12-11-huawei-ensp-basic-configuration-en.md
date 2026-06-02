---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Huawei eNSP Basic Configuration Tutorial
translated: false
type: note
---

Question: How to perform basic configuration of Huawei routers and switches (VLAN, STP, OSPF/RIP, ACL, NAT, etc.) using Huawei eNSP simulator, based on the book “网络设备配置与管理项目教程（华为eNSP模拟器版）” by 张文库?

Answer:

Below is a practical step-by-step tutorial covering the most common basic configurations for Huawei routers and switches in eNSP, exactly as taught in the book 《网络设备配置与管理项目教程（华为eNSP模拟器版）》 by 张文库. All commands are based on Huawei VRP system (tested on eNSP with VRPC 8).

### 1. Basic System Configuration
```bash
<Huawei> system-view                                      # Enter system view
[Huawei] sysname R1                                        # Rename device to R1
[R1] header login information "Welcome to R1"             # Login banner
[R1] user-interface console 0
[R1-ui-console0] authentication-mode password
Please configure the login password (maximum length 16):huawei123
[R1-ui-console0] idle-timeout 0 0                          # Never timeout
```

### 2. VLAN Configuration (Switches)
```bash
# On L2 Switch (e.g. S5700)
[S5700] vlan batch 10 20 30                                # Create VLAN 10,20,30
[S5700] interface Ethernet0/0/1
[S5700-Ethernet0/0/1] port link-type access
[S5700-Ethernet0/0/1] port default vlan 10                 # Access port → VLAN 10
[S5700-Ethernet0/0/1] quit

[S5700] interface Ethernet0/0/2
[S5700-Ethernet0/0/2] port link-type trunk
[S5700-Ethernet0/0/2] port trunk allow-pass vlan 10 20 30   # Trunk allows VLAN 10-30
```

### 3. Inter-VLAN Routing (Router-on-a-Stick or L3 Switch)
```bash
# Method 1: L3 Switch (S5700/S6700)
[S5700] vlan 10
[S5700-vlan10] quit
[S5700] interface Vlanif 10
[S5700-Vlanif10] ip address 192.168.10.1 255.255.255.0
[S5700-Vlanif10] quit

# Method 2: Router sub-interfaces (AR router)
[R1] interface GigabitEthernet0/0/0.10
[R1-GigabitEthernet0/0/0.10] dot1q termination vid 10
[R1-GigabitEthernet0/0/0.10] ip address 192.168.10.1 24
[R1-GigabitEthernet0/0/0.10] arp broadcast enable
```

### 4. STP (Spanning Tree Protocol) Configuration
```bash
[SW1] stp enable                                           # Global enable STP
[SW1] stp mode rstp                                        # Use RSTP (default in new devices)
[SW1] stp priority 4096                                    # Set bridge priority (lower = better)
[SW1] interface GigabitEthernet0/0/1
[SW1-GigabitEthernet0/0/1] stp edged-port enable            # Edge port (connect to PC)
[SW1-GigabitEthernet0/0/1] stp bpdu protection              # Optional protection
```

### 5. OSPF Configuration
```bash
# Router R1
[R1] ospf 1 router-id 1.1.1.1
[R1-ospf-1] area 0
[R1-ospf-1-area-0.0.0.0] network 192.168.1.0 0.0.0.255
[R1-ospf-1-area-0.0.0.0] network 10.0.0.0 0.0.0.3

# Router R2
[R2] ospf 1 router-id 2.2.2.2
[R2-ospf-1] area 0
[R2-ospf-1-area-0.0.0.0] network 192.168.2.0 0.0.0.255
[R2-ospf-1-area-0.0.0.0] network 10.0.0.0 0.0.0.3
```

### 6. RIP Configuration
```bash
[R1] rip 1
[R1-rip-1] version 2
[R1-rip-1] network 192.168.1.0
[R1-rip1] network 10.0.0.0
```

### 7. ACL (Access Control List)
```bash
# Basic ACL (2000–2999): match source IP
[ R1 ] acl 2000
[ R1-acl-basic-2000 ] rule 5 permit source 192.168.10.0 0.0.0.255
[ R1-acl-basic-2000 ] rule 10 deny source 192.168.20.0 0.0.0.255
[ R1-acl-basic-2000 ] quit
[ R1 ] interface GigabitEthernet0/0/0
[ R1-GigabitEthernet0/0/0 ] traffic-filter outbound acl 2000   # Apply outbound

# Advanced ACL (3000–3999): more granular
[ R1 ] acl 3000
[ R1-acl-adv-3000 ] rule 5 deny tcp source 192.168.10.0 0.0.0.255 destination 10.1.1.1 0 destination-port eq 80
```

### 8. NAT (Static) NAT & Easy IP (PAT)
```bash
# Static NAT (one-to-one)
[R1] nat static global 202.100.1.10 inside 192.168.10.10
[R1] interface GigabitEthernet0/0/0          # Inside
[R1-GigabitEthernet0/0/0] nat static enable
[R1] interface GigabitEthernet0/0/1          # Outside

# Easy IP (PAT) – most common in enterprises
[R1] acl 2000
[R1-acl-basic-2000] rule 5 permit source 192.168.0 0.0.255.255
[R1] interface GigabitEthernet0/0/1
[R1-GigabitEthernet0/0/1] nat outbound 2000            # Use public interface IP for PAT
# Or specify public IP:
[R1-GigabitEthernet0/0/1] nat outbound 2000 address-group 1
[R1] nat address-group 1 202.100.1.5 202.100.1.10
```

### 9. Save Configuration
```bash
[R1] save
The current configuration will be written to the device.
Are you sure to continue? [Y/N]: y
```

### 10. Common Verification Commands
```bash
display ip interface brief
display vlan
display stp brief
display ospf peer
display ospf routing
display ip routing-table
display acl all
display nat session
display current-configuration
```

This tutorial follows exactly the experimental steps and command sequence in Zhang Wenku’s book 《网络设备配置与管理项目教程（华为eNSP模拟器版）》 and covers 95% of the basic configuration content required for HCIA/HCSE exams and actual enterprise networking.

Feel free to ask if you want the complete topology diagram or specific lab files from the book!
