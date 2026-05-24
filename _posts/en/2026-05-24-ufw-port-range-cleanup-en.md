---
audio: false
generated: true
image: false
lang: en
layout: post
title: UFW Port Range Cleanup
translated: false
type: note
---

Done. UFW is now clean:

  ✓ 13000-14000/tcp removed (IPv4 + IPv6)
  ✓ 13000-14000/udp removed (IPv4 + IPv6)
  ✓ All necessary rules intact (22, 80, 443)

Final firewall state:

  [1] 22/tcp    ALLOW   SSH
  [2] 22/udp    ALLOW   (SSH discovery)
  [3] 443/udp   ALLOW   Hysteria2
  [4] 80/tcp    ALLOW   ACME challenge
  [5-8]         Same rules, IPv6

Default: deny inbound, allow outbound. Minimal attack surface.