---
audio: false
generated: true
image: false
lang: en
layout: post
title: Same Subnet Interface Binding Fix
translated: false
type: note
---

Reverted. Here's the real issue explained:

```
ROOT CAUSE: Two interfaces on same subnet
==========================================

On 1.47:
  wlp3s0:           192.168.1.47/24  (DOWN, but IP persists)
  enx00e04c362f89:  192.168.1.28/24  (UP, ethernet)

Gloo creates pair sockets for data transfer. Even with
GLOO_SOCKET_IFNAME=enx00e04c362f89, Gloo's C++ transport
may bind the pair socket to 192.168.1.47 (WiFi IP) instead
of 192.168.1.28 (ethernet IP). The master connects to the
ethernet IP but the socket is listening on the WiFi IP
(which is DOWN = timeout).

The `ip addr flush` you ran worked, but NetworkManager's
DHCP client immediately re-assigned the IP. Need to also
tell NetworkManager to stop managing WiFi.

FIX (run on 1.47 terminal with sudo):

  sudo nmcli device set wlp3s0 managed no
  sudo ip addr flush dev wlp3s0
  ip addr show wlp3s0    # verify no inet line

Then I'll restart training.
```
