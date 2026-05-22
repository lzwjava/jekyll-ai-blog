---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WiFi省电延迟分析
translated: true
type: note
---

分析：.52 和 .29 的异常值
==============================

192.168.1.52 — 平均 0.6 ms
─────────────────────────
  ARP 标志："permanent" — 这是你的 AIR (lzw-mac.local)
  MAC: b2:e2:c6:39:f3:dd (本地管理 = Apple 私有 WiFi 地址)
  为什么是 0.6ms：ping 自己 = 回环，永远不会离开网卡。
  没什么特别的 — 只是本地机器。

192.168.1.29 — 平均 446.7 ms
───────────────────────────
  MAC: 86:c5:c7:ef:f6:5f (本地管理 = 随机/私有 MAC)
  可能是：使用私有 WiFi 地址的 Apple 设备 (iPhone/iPad)
  逐 ping 明细：
    icmp_seq=0  324 ms
    icmp_seq=1  298 ms
    icmp_seq=2  196 ms
    icmp_seq=3  1045 ms  ← 尖峰！
    icmp_seq=4  45 ms
    icmp_seq=5  849 ms
    icmp_seq=6  701 ms
    icmp_seq=7  860 ms
    icmp_seq=8  641 ms
    icmp_seq=9  693 ms
    标准差 = 312 ms  ← 巨大的抖动

  原因：该设备处于 WiFi 省电模式 (802.11 PSM)。
    - 无线电休眠以节省电量
    - 定期唤醒检查缓冲帧
    - 每次 ping 必须等待下一个唤醒窗口
    - 这就是延迟随机在 45ms 到 1045ms 之间的原因
    - 0% 丢包 = 它是可达的，只是在检查之间休眠

  其他慢速设备：
    .14 (Xiaomi, 86ms) — 手机处于省电模式，不那么激进
    .49 (Apple, 97ms) — Apple 设备，中等省电模式

模式：**电池供电设备**（手机、平板）使用 802.11 省电模式。它们批量处理缓冲帧并按计划唤醒。省电越激进，ping 延迟越高。.29 是最大的问题设备 — 可能是具有激进电池优化的 iPhone/iPad。有线设备 (.36, .18) 和常开设备 (.1 路由器) 保持低延迟。