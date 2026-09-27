---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 家庭实验室：为学习购买多台电脑
translated: true
type: note
---

Question: 互联网上有没有人这样做——买很多台电脑来搭建家庭实验室，用于学习/实验？

Answer: 有的，绝对有——这是一个规模非常大且相当成熟的爱好，有着活跃的社区。它通常被称为“**homelab**”。

**人们在哪里分享这些内容**

- **r/homelab**（Reddit）—— 这是一个大型社区（根据来源不同，大约有 45 万到 80 多万名成员），人们在这里分享自己的搭建方案，从小到一个树莓派（Raspberry Pi），大到整机柜服务器。这是一个面向 DevOps 工程师和程序员的在线社区，成立于 2012 年，既有论坛，也有通过关联的 Discord 服务器提供的实时聊天。
- **r/selfhosted** —— 更侧重于软件层面（自己运行服务，而不是使用云服务提供商）。
- **r/DataHoarder** —— 针对存储密集型方案（NAS、备份）。
- 许多个人博客和 YouTube 频道都会展示“homelab tours”（homelab 参观导览）。

**典型的 homelab 是什么样的**（来自一个用户公开分享的真实示例）
一位用户将他的方案描述为一个主要用于实验和学习新技术及网络概念的小型 homelab，机器大多来自翻新和二手机械——包括两台运行 Proxmox 和 Kubernetes 的 Dell 服务器、一台 Raspberry Pi、一台 Synology NAS 和一个 PiKVM。他在这上面自托管了 Pi-hole、用于监控的 Prometheus/Grafana、Home Assistant、一个媒体服务器，以及为家人和朋友提供的个人 VPN 服务。

**规模跨度很大**
正如一位社区成员总结的那样：homelab 可以简单到只有一个运行 Pi-hole 的 Raspberry Pi，或是一台运行媒体服务器的旧 PC——一直到拥有多台服务器、磁盘阵列、自定义路由器方案、基于 Docker 的完整媒体栈，甚至还有 AI 工作负载的完整机柜。资深成员的建议始终如一：你不需要带 UPS、配线架和 Cisco 路由器的昂贵企业机柜——你可以从一个小小的 Raspberry Pi 开始，甚至只用一台运行虚拟化软件的笔记本电脑，等真正需要时再扩展。

所以说，你的想法——买一堆便宜的/二手机器，不怕拆坏它们，然后边做边学（Docker、Kubernetes、OpenWrt 等）——恰恰就是这个社区中一大部分人的做法。

参考链接：

- [r/homelab 社区概述](https://thehiveindex.com/communities/r-homelab)
- [Homelab 用户搭建示例（Tildes）](https://tildes.net/user/oxtyped)
- [r/homelab “新手从这里开始”指南](https://nyc1.lr.ggtyler.dev/r/homelab/comments/15jt90s/new_rhomelab_users_start_here)
