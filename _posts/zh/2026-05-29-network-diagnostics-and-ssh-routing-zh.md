---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络诊断与SSH路由
translated: true
type: note
---

网络诊断
===============

134.199.205.0（AMD Dev Cloud，亚特兰大）
  延迟： ~315ms 平均，40% 丢包（！）
  路由： 广州 -> CN2 -> NTT 骨干网 -> DigitalOcean 亚特兰大
  问题： NTT 互联拥塞，每10个数据包丢弃4个

69.63.219.0（DMIT，洛杉矶）
  延迟： ~170ms 平均，0% 丢包
  路由： 广州 -> CN2（中国电信优质线路）-> DMIT 洛杉矶
  干净的 CN2 GIA 路径

SSH 计时
  直连 AMD： ~5.3s 连接，0.8s 传输（有丢包）
  通过 DMIT 跳转： ~4.4s 连接，0.8s 传输（无丢包）

跳转增加了约1秒的 SSH 认证开销（两跳），但真正的收益是0%丢包——通过直连路由进行交互式会话非常痛苦，因为40%的按键会被丢弃/重传。

SSH 配置现已设置：

ssh dmit       # -> 直接连接 69.63.219.0（绕过 SOCKS5 代理）
ssh amd-cloud  # -> 通过 dmit 跳转连接 134.199.205.0

工作原理：

- Host dmit 设置了 ProxyCommand none，以绕过你的 !192.168.*.* SOCKS5 通配符
- Host amd-cloud 使用 ProxyJump dmit，这会覆盖 SOCKS5 的 ProxyCommand（ProxyJump 优先级更高）
- 其他所有非本地主机仍像以前一样通过 hysteria2 代理

你的原始配置已备份至 ~/.ssh/config.bak.2026009。
