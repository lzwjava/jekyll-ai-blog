---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络诊断命令摘要
translated: true
type: note
---

以下是我使用的命令：

  ip addr show
  ip route show default
  cat /etc/resolv.conf
  curl ifconfig.me
  curl ipinfo.io
  ping -c 3 -W 2 172.21.38.1
  ping -c 3 -W 2 8.8.8.8
  ip neigh show
  nmcli dev wifi
  ss -tlnp