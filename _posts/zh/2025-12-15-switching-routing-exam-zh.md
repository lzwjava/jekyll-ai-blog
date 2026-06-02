---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 交换与路由考试题
translated: true
type: note
---

问题：为课程 13833 交换和路由技术（中国全国高等教育自学考试，广东）提供 30 道多项选择题。

答案：

以下是 30 道多项选择题，涵盖了交换和路由技术中的关键主题，包括网络基础知识、以太网交换、VLAN、STP、路由协议（RIP、OSPF、BGP）、IPv6、网络安全和设备配置。

1. OSI 模型的哪一层负责逻辑寻址和路由？
   A) 物理层
   B) 数据链路层
   C) 网络层
   D) 传输层

2. 交换机在网络中的主要功能是什么？
   A) 在不同网络之间路由数据包
   B) 根据 MAC 地址转发帧
   C) 为主机提供 IP 地址
   D) 加密数据流量

3. 在以太网交换中，当交换机收到一个目标 MAC 地址不在其 MAC 地址表中的帧时，会发生什么？
   A) 丢弃该帧
   B) 将该帧泛洪到除入站端口之外的所有端口
   C) 将该帧发送到默认网关
   D) 无限期地缓冲该帧

4. VLAN 在交换网络中的目的是什么？
   A) 增加广播域
   B) 分段广播域并提高安全性
   C) 在交换机之间路由流量
   D) 动态分配 IP 地址

5. 以下哪种协议用于防止第二层网络中的环路？
   A) OSPF
   B) RIP
   C) Spanning Tree Protocol (STP)
   D) BGP

6. 在 STP 中，哪个端口状态会阻塞流量以防止环路？
   A) 侦听 (Listening)
   B) 学习 (Learning)
   C) 转发 (Forwarding)
   D) 阻塞 (Blocking)

7. STP 中交换机的默认优先级值是多少？
   A) 0
   B) 32768
   C) 61440
   D) 65535

8. 大多数交换机上的默认 VLAN 是哪个？
   A) VLAN 0
   B) VLAN 1
   C) VLAN 100
   D) VLAN 1001

9. 哪种类型的 VLAN 在交换机之间承载多个 VLAN 的流量？
   A) 接入 VLAN (Access VLAN)
   B) 本征 VLAN (Native VLAN)
   C) 中继 VLAN (Trunk VLAN)
   D) 语音 VLAN (Voice VLAN)

10. 在交换机上，哪个命令用于将端口配置为中继端口？
    A) switchport mode access
    B) switchport mode trunk
    C) switchport trunk encapsulation dot1q
    D) switchport access vlan 10

11. 静态路由的默认管理距离是多少？
    A) 0
    B) 1
    C) 110
    D) 120

12. 哪种路由协议使用跳数作为其度量标准？
    A) OSPF
    B) RIP
    C) BGP
    D) EIGRP

13. RIP 中的最大跳数是多少？
    A) 15
    B) 16
    C) 255
    D) 无限

14. OSPF 属于哪种类型的路由协议？
    A) 距离矢量 (Distance Vector)
    B) 链路状态 (Link State)
    C) 路径矢量 (Path Vector)
    D) 混合 (Hybrid)

15. 在 OSPF 中，router ID 的作用是什么？
    A) 识别区域
    B) 选举指定路由器 (DR)
    C) 计算度量标准
    D) 宣告路由

16. 哪种协议用于自治系统之间的外部网关路由？
    A) RIP
    B) OSPF
    C) BGP
    D) IS-IS

17. NAT 代表什么？
    A) Network Address Translation
    B) Network Access Terminal
    C) Node Address Table
    D) New Area Type

18. 哪种类型的 NAT 将多个私有 IP 映射到一个公共 IP？
    A) 静态 NAT (Static NAT)
    B) 动态 NAT (Dynamic NAT)
    C) PAT (Overload)
    D) 一对一 NAT (One-to-One NAT)

19. 访问控制列表 (ACL) 的作用是什么？
    A) 分配 IP 地址
    B) 根据规则过滤流量
    C) 配置 VLAN
    D) 启用路由

20. 在 IPv6 中，回环地址是什么？
    A) ::1
    B) FE80::1
    C) FF02::1
    D) 127.0.0.1

21. IPv6 地址有多少位？
    A) 32
    B) 64
    C) 128
    D) 256

22. 哪种协议用于 IPv6 中的无状态地址自动配置？
    A) DHCPv6
    B) SLAAC
    C) NAT66
    D) OSPFv3

23. 使用 DHCP 的主要好处是什么？
    A) 手动 IP 分配
    B) 自动 IP 地址分配
    C) 流量加密
    D) 环路预防

24. 哪个命令显示路由器上的路由表？
    A) show ip route
    B) show interfaces
    C) show vlan
    D) show mac address-table

25. ARP 的目的是什么？
    A) 将 IP 解析为 MAC 地址
    B) 将 MAC 解析为 IP 地址
    C) 路由数据包
    D) 加密数据

26. 在交换网络中，什么会导致广播风暴？
    A) 过多的单播帧
    B) 没有 STP 的网络环路
    C) VLAN 配置错误
    D) 高带宽使用率

27. 哪个端口安全功能限制端口上的 MAC 地址数量？
    A) Sticky MAC
    B) Violation Restrict
    C) Maximum MAC addresses
    D) Portfast

28. 现代交换机上 trunk 的默认封装方式是什么？
    A) ISL
    B) 802.1Q
    C) PPP
    D) HDLC

29. 哪种 OSPF 区域类型不允许外部路由？
    A) 骨干区域 (Backbone Area)
    B) 末梢区域 (Stub Area)
    C) 完全末梢区域 (Totally Stubby Area)
    D) NSSA

30. IPv4 中的组播地址范围是多少？
    A) 192.168.0.0/16
    B) 224.0.0.0 到 239.255.255.255
    C) 10.0.0.0/8
    D) 172.16.0.0/12

**正确答案：**

1. C
2. B
3. B
4. B
5. C
6. D
7. B
8. B
9. B（注意：中继端口承载多个 VLAN）
10. B
11. B
12. B
13. A
14. B
15. B
16. C
17. A
18. C
19. B
20. A
21. C
22. B
23. B
24. A
25. A
26. B
27. C
28. B
29. B
30. B

参考文献：

- [广东交换与路由技术自考考试大纲(13833免费下载)](https://www.zikaosw.cn/news/22147405.html)
- [路由交换技术及应用（第4版）图书内容概述](https://www.ryjiaoyu.com/book/details/47556)
- [路由交换技术复习题示例](https://blog.csdn.net/m0_64000952/article/details/139968916)
