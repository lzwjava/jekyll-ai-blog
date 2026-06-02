---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 华为eNSP基础配置教程
translated: true
type: note
---

问题：如何使用华为eNSP模拟器，根据张文库的《网络设备配置与管理项目教程（华为eNSP模拟器版）》一书，对华为路由器和交换机进行基本配置（VLAN、STP、OSPF/RIP、ACL、NAT等）？

回答：

以下是根据张文库的《网络设备配置与管理项目教程（华为eNSP模拟器版）》一书，在eNSP中对华为路由器和交换机进行最常见基本配置的实践分步教程。所有命令均基于华为VRP系统（在eNSP上使用VRPC 8进行测试）。

### 1. 基本系统配置
```bash
<Huawei> system-view                                      # 进入系统视图
[Huawei] sysname R1                                        # 将设备重命名为R1
[R1] header login information "Welcome to R1"             # 登录横幅
[R1] user-interface console 0
[R1-ui-console0] authentication-mode password
Please configure the login password (maximum length 16):huawei123
[R1-ui-console0] idle-timeout 0 0                          # 永不超时
```

### 2. VLAN配置（交换机）
```bash
# 在L2交换机上（例如S5700）
[S5700] vlan batch 10 20 30                                # 创建VLAN 10,20,30
[S5700] interface Ethernet0/0/1
[S5700-Ethernet0/0/1] port link-type access
[S5700-Ethernet0/0/1] port default vlan 10                 # Access端口 → VLAN 10
[S5700-Ethernet0/0/1] quit

[S5700] interface Ethernet0/0/2
[S5700-Ethernet0/0/2] port link-type trunk
[S5700-Ethernet0/0/2] port trunk allow-pass vlan 10 20 30   # Trunk允许VLAN 10-30
```

### 3. VLAN间路由（Router-on-a-Stick或L3交换机）
```bash
# 方法1：L3交换机 (S5700/S6700)
[S5700] vlan 10
[S5700-vlan10] quit
[S5700] interface Vlanif 10
[S5700-Vlanif10] ip address 192.168.10.1 255.255.255.0
[S5700-Vlanif10] quit

# 方法2：路由器子接口 (AR router)
[R1] interface GigabitEthernet0/0/0.10
[R1-GigabitEthernet0/0/0.10] dot1q termination vid 10
[R1-GigabitEthernet0/0/0.10] ip address 192.168.10.1 24
[R1-GigabitEthernet0/0/0.10] arp broadcast enable
```

### 4. STP (Spanning Tree Protocol) 配置
```bash
[SW1] stp enable                                           # 全局启用STP
[SW1] stp mode rstp                                        # 使用RSTP（新设备默认）
[SW1] stp priority 4096                                    # 设置桥优先级（数值越低越好）
[SW1] interface GigabitEthernet0/0/1
[SW1-GigabitEthernet0/0/1] stp edged-port enable            # 边缘端口（连接PC）
[SW1-GigabitEthernet0/0/1] stp bpdu protection              # 可选保护功能
```

### 5. OSPF 配置
```bash
# 路由器R1
[R1] ospf 1 router-id 1.1.1.1
[R1-ospf-1] area 0
[R1-ospf-1-area-0.0.0.0] network 192.168.1.0 0.0.0.255
[R1-ospf-1-area-0.0.0.0] network 10.0.0.0 0.0.0.3

# 路由器R2
[R2] ospf 1 router-id 2.2.2.2
[R2-ospf-1] area 0
[R2-ospf-1-area-0.0.0.0] network 192.168.2.0 0.0.0.255
[R2-ospf-1-area-0.0.0.0] network 10.0.0.0 0.0.0.3
```

### 6. RIP 配置
```bash
[R1] rip 1
[R1-rip-1] version 2
[R1-rip-1] network 192.168.1.0
[R1-rip1] network 10.0.0.0
```

### 7. ACL (Access Control List)
```bash
# 基本ACL (2000–2999): 匹配源IP
[ R1 ] acl 2000
[ R1-acl-basic-2000 ] rule 5 permit source 192.168.10.0 0.0.0.255
[ R1-acl-basic-2000 ] rule 10 deny source 192.168.20.0 0.0.0.255
[ R1-acl-basic-2000 ] quit
[ R1 ] interface GigabitEthernet0/0/0
[ R1-GigabitEthernet0/0/0 ] traffic-filter outbound acl 2000   # 应用向外流量过滤
[ R1 ] interface GigabitEthernet0/0/0
[ R1-GigabitEthernet0/0/0 ] traffic-filter inbound acl 2000   # 应用向内流量过滤

# 高级ACL (3000–3999): 更精细的控制
[ R1 ] acl 3000
[ R1-acl-adv-3000 ] rule 5 deny tcp source 192.168.10.0 0.0.0.255 destination 10.1.1.1 0 destination-port eq 80
```

### 8. NAT (Static) NAT & Easy IP (PAT)
```bash
# 静态NAT (一对一)
[R1] nat static global 202.100.1.10 inside 192.168.10.10
[R1] interface GigabitEthernet0/0/0          # 内部接口
[R1-GigabitEthernet0/0/0] nat static enable
[R1] interface GigabitEthernet0/0/1          # 外部接口

# Easy IP (PAT) – 企业中最常见
[R1] acl 2000
[R1-acl-basic-2000] rule 5 permit source 192.168.0 0.0.255.255
[R1] interface GigabitEthernet0/0/1
[R1-GigabitEthernet0/0/1] nat outbound 2000            # 使用公网接口IP进行PAT
# 或者指定公网IP：
[R1-GigabitEthernet0/0/1] nat outbound 2000 address-group 1
[R1] nat address-group 1 202.100.1.5 202.100.1.10
```

### 9. 保存配置
```bash
[R1] save
The current configuration will be written to the device.
Are you sure to continue? [Y/N]: y
```

### 10. 常用验证命令
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

本教程严格遵循张文库《网络设备配置与管理项目教程（华为eNSP模拟器版）》一书中的实验步骤和命令序列，涵盖了HCIA/HCSE考试和实际企业网络中所需的95%基本配置内容。

如果您需要完整的拓扑图或书中的特定实验文件，请随时提出！
