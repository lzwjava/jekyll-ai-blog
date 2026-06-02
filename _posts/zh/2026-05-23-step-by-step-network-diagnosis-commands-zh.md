---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分步网络诊断命令
translated: true
type: note
---

以下是诊断过程的逐步命令分解：

```
逐步网络诊断
===============================

1. 路由追踪（失败——跳点阻止了ICMP）
   $ traceroute -w 2 -m 10 192.168.1.36
   结果：全部超时（本地局域网路由器不响应路由追踪）

2. 对.36执行10次PING——检查一致性
   $ ping -c 10 192.168.1.36 | tail -5
   结果：最小/平均/最大 = 6.6/16.4/75.0ms，标准差19.7ms
   分析：范围很大（6ms到75ms）——这是WiFi抖动，而非路径延迟

3. 比较路由器与工作站（各5次PING）
   $ ping -c 5 192.168.1.1  | grep round-trip
   $ ping -c 5 192.168.1.36 | grep round-trip
   结果：路由器平均18.8ms，工作站平均25.0ms
   分析：路由器也有类似抖动——WiFi是共同的瓶颈

4. 检查哪个接口处于活动状态
   $ ifconfig en0 | grep -E "status|inet"
   结果：en0处于活动状态，IP为192.168.1.52——确认在WiFi上

5. 检查ARP表——查看邻居的MAC地址
   $ arp -a | grep "192.168.1\.(1|36)"
   结果：两者都在en0上（同一局域网），.36的MAC地址 = 4:7c:16:d9:54:5b
   分析：4:7c:16属于ASRock（你的工作站主板）

6. 检查WiFi硬件信息（尝试过，在较新的macOS上已弃用）
   $ /System/Library/PrivateFrameworks/Apple80211.framework/.../airport -I
   $ wdutil info
   结果：两者在macOS 14+上均失败/需要sudo权限

7. 对.36执行30次PING——更精准的统计
   $ ping -c 30 192.168.1.36 | grep round-trip
   结果：最小/平均/最大 = 4.4/12.4/69.5ms，标准差15.8ms
   分析：平均值仅为12ms——之前的92ms属于异常尖峰

命令汇总：
  ping -c N <host> | grep round-trip    ——延迟统计
  ping -c 10 <host> | tail -5           ——快速一致性检查
  ifconfig en0 | grep inet              ——确认你的IP/接口
  arp -a | grep <ip>                    ——查看MAC地址及对应接口
  traceroute <host>                     ——路径跳点（局域网中常被阻止）
  networksetup -listallhardwareports    ——列出所有接口
```

关键技巧：**将路由器PING与目标PING进行比较**。如果两者都显示相似的抖动，则瓶颈在于共享跳点（WiFi）。如果只有目标端慢，则额外路径（以太网/交换机）才是问题所在。
