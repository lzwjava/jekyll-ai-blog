---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 交换与路由技术考试题目
translated: true
type: note
---

问题：根据提供的《交换与路由技术》（课程代码：13833）教学大纲，生成 30 道单选题，且不显示正确答案。

回答：

以下是基于《交换与路由技术》教学大纲编写的 30 道单选题。每道题有 4 个选项（A–D）。

1. eNSP 模拟器的主要作用是什么？
   A) 模拟真实的硬件故障
   B) 为配置和测试虚拟网络提供平台
   C) 在生产环境中替代物理路由器
   D) 管理物理网络布线

2. eNSP 模拟器中的 Huawei 设备使用哪种操作系统？
   A) Cisco IOS
   B) Juniper JunOS
   C) VRP (Versatile Routing Platform)
   D) Linux

3. 交换机在进行基本转发时主要工作在 OSI 模型的哪一层？
   A) 第 1 层
   B) 第 2 层
   C) 第 3 层
   D) 第 4 层

4. VLAN 技术的主要目的是什么？
   A) 增加广播域
   B) 划分网络并隔离不同部门之间的流量
   C) 提高跨 WAN 的路由速度
   D) 加密数据包

5. 哪种类型的交换机端口允许通过多个 VLAN？
   A) Access 端口
   B) Trunk 端口
   C) Hybrid 端口
   D) Console 端口

6. Access 端口如何处理带有 VLAN tag 的数据帧？
   A) 原样转发
   B) 在转发前添加 VLAN tag
   C) 在转发前剥离 VLAN tag
   D) 丢弃所有带有 tag 的帧

7. 哪种技术可以使用单个路由器物理接口实现 VLAN 间通信？
   A) Link aggregation
   B) 单臂路由 (One-arm routing)
   C) Spanning Tree Protocol
   D) VRRP

8. Layer 3 交换机与传统路由器的主要区别在于：
   A) 使用基于硬件的快速转发进行路由
   B) 仅支持静态路由
   C) 无法执行 NAT
   D) 仅工作在 Layer 2

9. Link aggregation 的主要好处是什么？
   A) 防止网络环路
   B) 增加带宽并为骨干链路提供冗余
   C) 自动分配 IP 地址
   D) 加密交换机之间的流量

10. 哪种协议用于防止 Layer 2 交换环路？
    A) OSPF
    B) RIP
    C) Spanning Tree Protocol (STP) 或 Rapid STP (RSTP)
    D) VRRP

11. VRRP 在网络中提供什么功能？
    A) 动态路由更新
    B) 网关冗余和高可用性
    C) VLAN 隔离
    D) 地址转换

12. 哪种服务允许主机在网络中自动获取 IP 地址？
    A) NAT
    B) ACL
    C) DHCP
    D) OSPF

13. 在路由器上，哪种 DHCP 地址池类型使用接口所在的网段进行分配？
    A) 全局地址池 (Global address pool)
    B) 接口地址池 (Interface address pool)
    C) 静态地址池
    D) 中继池

14. 路由在网络中的主要功能是什么？
    A) 连接同一广播域内的设备
    B) 根据 IP 地址在不同网络之间转发数据包
    C) 根据 MAC 地址交换数据帧
    D) 提供无线连接

15. 哪种类型的路由需要管理员进行手动配置？
    A) 动态路由
    B) 默认路由
    C) 静态路由
    D) 浮动路由

16. 默认路由的作用是什么？
    A) 为特定的目的网络指定路径
    B) 为未知目的地充当最后求助网关
    C) 在多条链路上实现流量负载均衡
    D) 防止路由环路

17. 浮动静态路由主要用于：
    A) 更快的收敛
    B) 具有更高管理距离的备份路径
    C) 动态邻居发现
    D) VLAN 标记

18. 哪种路由协议使用距离矢量算法，并在第 2 版中支持无类路由？
    A) OSPF
    B) RIP (RIPv2)
    C) BGP
    D) EIGRP

19. OSPF 相比 RIP 的一个核心优势是：
    A) 使用跳数作为度量值
    B) 支持快速收敛和分层区域设计
    C) 每 30 秒广播一次更新
    D) 仅支持小型网络

20. 在 OSPF 中，所有其他区域必须连接到哪个区域？
    A) 末梢区域 (Stub area)
    B) 完全末梢区域 (Totally stubby area)
    C) 骨干区域 (Backbone area / Area 0)
    D) 普通区域

21. 网络地址转换 (NAT) 主要实现了什么？
    A) 防止广播风暴
    B) 允许私有 IP 地址使用公有 IP 访问 Internet
    C) 加密路由更新
    D) 阻断 VLAN 流量

22. 哪种技术用于根据允许或拒绝规则来控制网络流量？
    A) VLAN
    B) 访问控制列表 (ACL)
    C) STP
    D) DHCP

23. ACL 通常应用在哪些设备上以增强安全性？
    A) 集线器 (Hub)
    B) 交换机和路由器
    C) 仅无线接入点
    D) 终端用户 PC

24. 哪种 WAN 协议常用于串行链路上的身份验证和封装？
    A) RIP
    B) OSPF
    C) PPP
    D) VLAN

25. 在子网规划中，中型园区网的关键要素是什么？
    A) 仅使用公有 IP 地址
    B) 合理的 IP 地址子网划分与分配
    C) 为所有部门分配相同的子网
    D) 完全避免使用 VLAN

26. VRP 中的哪种视图用于基础配置任务？
    A) 用户视图 (User view)
    B) 系统视图 (System view)
    C) 接口视图 (Interface view)
    D) 协议视图

27. 远程管理交换机的常用方法是什么？
    A) 仅通过 Console 端口
    B) 在基础配置后使用 Telnet 或 SSH
    C) 直接 USB 连接
    D) 蓝牙

28. 通常在什么时候需要进行路由重发布 (Route redistribution)？
    A) 仅使用静态路由时
    B) 同一网络中运行多种路由协议时
    C) 配置 VLAN 时
    D) 设置 DHCP 时

29. 哪种工具或命令可用于追踪数据包在网络中经过的路径？
    A) Ping
    B) Tracert (Traceroute)
    C) Show ip route
    D) Display vlan

30. 根据教学大纲，本课程内容的主要组织方式是什么？
    A) 纯理论讲座
    B) 基于真实企业网络任务的项目任务体系
    C) 纯粹的命令记忆
    D) 仅侧重于 IPv6
