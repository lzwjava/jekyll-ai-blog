---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 交换与路由考试题目
translated: true
type: note
---

以下是《13833 交换与路由技术》课程（中国高等教育自学考试广东省）的30道选择题，涵盖以太网交换、VLAN、生成树协议、IP路由、OSPF、BGP、IPv6、路由安全等核心知识点。题目采用英文表述（技术类内容标准形式）。

1. 二层交换机主要工作在OSI模型的哪一层？
A) 第一层
B) 第二层
C) 第三层
D) 第四层

2. 以太网中广播帧的目标MAC地址是什么？
A) 0000.0000.0000
B) FFFF.FFFF.FFFF
C) 0100.5E00.0000
D) 默认网关的MAC地址

3. 交换机MAC地址表中的“老化时间”指什么？
A) 端口保持转发状态的时间
B) 动态MAC表项被删除前的存活时间
C) VLAN保持激活状态的时间
D) ARP缓存过期时间

4. 在Cisco交换机接口上启用PortFast的命令是？
A) spanning-tree portfast
B) spanning-tree bpduguard enable
C) no spanning-tree uplinkfast
D) spanning-tree mode rapid-pvst

5. 交换网络中VLAN的主要作用是？
A) 扩大广播域范围
B) 分割二层广播域
C) 替代路由器功能
D) 提供三层加密

6. Cisco交换机默认的本征VLAN是？
A) VLAN 1
B) VLAN 1002
C) VLAN 0
D) VLAN 4094

7. 哪种协议用于防止二层交换环路？
A) VTP
B) DTP
C) STP
D) LACP

8. 在RSTP中，哪个端口角色等同于传统STP的阻塞端口？
A) 根端口
B) 指定端口
C) 替代端口
D) 边缘端口

9. 在Cisco交换机上配置VLAN 20接入端口的命令是？
A) switchport mode access vlan 20
B) switchport access vlan 20
C) switchport mode access
D) switchport trunk allowed vlan 20

10. 命令“switchport mode dynamic desirable”的作用是？
A) 强制开启中继
B) 强制设为接入模式
C) 主动尝试建立中继
D) 仅在对端发起时才接受中继

11. 哪种VTP模式不允许交换机创建或删除VLAN？
A) 服务器模式
B) 客户端模式
C) 透明模式
D) 关闭模式

12. 大多数Cisco交换机默认采用哪种以太通道负载均衡方式？
A) 源MAC
B) 目的MAC
C) 源-目的MAC
D) 源IP

13. 静态路由的默认管理距离是多少？
A) 0
B) 1
C) 5
D) 110

14. 哪种路由协议默认使用带宽和延迟作为度量值？
A) RIP
B) OSPF
C) EIGRP
D) IS-IS

15. OSPF中用于发现邻居的报文类型是？
A) Hello报文
B) DBD报文
C) LSR报文
D) LSU报文

16. OSPF默认的路由器ID选举顺序是？
A) 最高环回地址 > 最高物理地址
B) 最低环回地址 > 最低物理地址
C) 手动配置 > 最高环回地址 > 最高物理地址
D) 随机分配

17. 哪种EIGRP报文以单播发送且需要确认？
A) Hello报文
B) 更新报文
C) 查询报文
D) 应答报文

18. BGP路径选择过程中优先使用的属性是？
A) 本地优先级
B) AS路径
C) 权重
D) MED值

19. 哪个BGP邻居状态表示已完成TCP三次握手？
A) 空闲状态
B) 连接状态
C) 活跃状态
D) 已建立状态

20. 路由汇总的主要目的是？
A) 增加路由表规模
B) 减少路由表规模及更新流量
C) 加密路由更新
D) 优化路径优先级

21. 在Cisco路由器上启用IPv6路由的命令是？
A) ipv6 enable
B) ipv6 unicast-routing
C) ipv6 address autoconfig
D) ipv6 router ospf 1

22. IPv6环回地址是？
A) ::1
B) FE80::1
C) FF02::1
D) 2001::1

23. 哪种IPv6地址类型用于提供商无关寻址？
A) 链路本地地址
B) 唯一本地地址
C) 全局单播地址
D) 组播地址

24. 哪个协议是IPv6中相当于ARP的协议？
A) NDP
B) ICMPv6
C) DHCPv6
D) SLAAC

25. 配置到目的地2001:DB8::/32经下一跳2001:DB8:1::1的IPv6静态路由命令是？
A) ipv6 route 2001:DB8::/32 2001:DB8:1::1
B) ip route 2001:DB8::/32 2001:DB8:1::1
C) ipv6 route 2001:DB8::/32 serial0/0
D) route ipv6 2001:DB8::/32 2001:DB8:1::1

26. 第一跳冗余协议的主要目标是？
A) 在多链路上实现负载均衡
B) 提供默认网关冗余
C) 加密至网关的流量
D) 减少ARP广播

27. 哪种FHRP协议使用0000.0C9F.Fxxx格式的虚拟MAC地址？
A) HSRP
B) VRRP
C) GLBP
D) IRDP

28. 哪个特性可防止恶意设备成为生成树根桥？
A) BPDU防护
B) 根防护
C) 环路防护
D) UDLD

29. 命令“ip verify unicast source reachable-via rx”的功能是？
A) 启用单播反向路径转发
B) 启用IP源防护
C) 启用DHCP侦听
D) 启用动态ARP检测

30. 在路由过滤中，哪种Cisco访问列表类型可同时匹配前缀和前缀长度？
A) 标准访问列表
B) 扩展访问列表
C) 前缀列表
D) 路由映射

本组题目符合13833考试要求，覆盖教学大纲核心内容。祝学习顺利！
