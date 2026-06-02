---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中继器设置中的NAT与ARP更改
translated: true
type: note
---

```
网络拓扑 — 路由器 A 连接后
=============================================

BEFORE（单一路由器）：
  Internet → 路由器 B（中国电信网关，.1）→ 所有设备

NOW（中继模式）：
  Internet → 路由器 A（TP-LINK，.37）~无线中继~ 路由器 B（.1）→ 设备
                ↓                                            ↓
          路由器 A 下的设备                             路由器 B 的 WiFi 上的设备

ARP 表中的变化：

  .37 出现 — 路由器 A（TP-LINK）
    MAC：本地管理，“permanent”标志
    延迟：2ms（非常近——就是路由器本身）

  .36、.18、.19、.20 现在共享同一个 MAC 地址
    → 这些设备位于路由器 A 之下，通过它进行 NAT
    → 路由器 A 将它们各自的 MAC 重写为自己的 MAC

  .14、.21、.24、.26、.31、.50、.54 保留了原本的 MAC
    → 仍直接连接在路由器 B 的 WiFi 上

设备分类：

  路由器 A 下（TP-LINK，经过 NAT）：
    .36  工作站（ASRock，有线连接至路由器 A）
    .18  TP-LINK 设备（IoT/智能家居？）
    .19  未知
    .20  Intel 设备

  路由器 B 上（中国电信，直连）：
    .1   路由器 B 本身
    .14  小米
    .21  Apple 私人 WiFi
    .24  Apple 私人 WiFi
    .26  未知（50:8b:b9）
    .31  Apple 私人 WiFi
    .50  未知（34:55:06）
    .54  Apple 私人 WiFi

  消失的设备（原在路由器 B 上，现已不在）：
    .42、.49、.52、.53 — 手机/平板进入休眠
    .52 曾是您的 Air，但现在显示为 .37 的网络

  注意：您的 Air（.52）连接在路由器 B 的 WiFi 上
        但 ARP 表显示它通过路由器 A 的 MAC 通信
        → Air 在路由器 B 一侧，不在路由器 A 之后

```

中继器创建了两个逻辑区域。路由器 A 下的设备会经过 NAT（在 ARP 中显示相同 MAC）。路由器 B 上的设备保留其真实 MAC。您的工作站（.36）有线连接至路由器 A——这就是它显示为 NAT 状态的原因。
