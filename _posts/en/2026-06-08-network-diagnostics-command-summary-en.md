---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Diagnostics Command Summary
translated: false
type: note
---

Here are the commands I used:

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
