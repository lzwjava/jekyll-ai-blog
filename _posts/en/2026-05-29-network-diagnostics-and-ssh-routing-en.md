---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Diagnostics and SSH Routing
translated: false
type: note
---

Here's the full analysis:
    
    
    NETWORK DIAGNOSIS
    ================
    
    134.199.205.0 (AMD Dev Cloud, Atlanta)
      Ping:   ~315ms avg, 40% packet loss (!)
      Route:  Guangzhou -> CN2 -> NTT backbone -> DigitalOcean Atlanta
      Problem: NTT interconnect is congested, dropping 4 in 10 packets
    
    69.63.219.0 (DMIT, Los Angeles)  
      Ping:   ~170ms avg, 0% packet loss
      Route:  Guangzhou -> CN2 (China Telecom premium) -> DMIT LA
      Clean CN2 GIA path
    
    SSH TIMING
      Direct to AMD:      ~5.3s connect, 0.8s transfer (lossy)
      Via DMIT jump:      ~4.4s connect, 0.8s transfer (clean)
    
    
    
    The jump adds ~1s of SSH auth overhead (two hops), but the real win is 0% packet loss — interactive sessions through the direct route are painful because 40% of keystrokes get dropped/retransmitted.
    
    SSH config is now set up:
    
    
    ssh dmit       # -> 69.63.219.0 direct (bypasses SOCKS5 proxy)
    ssh amd-cloud  # -> 134.199.205.0 via dmit jump
    
    
    How it works:
    - Host dmit has ProxyCommand none to bypass your !192.168.*.* SOCKS5 wildcard
    - Host amd-cloud uses ProxyJump dmit which overrides the SOCKS5 ProxyCommand (ProxyJump takes precedence)
    - All other non-local hosts still go through hysteria2 proxy as before
    
    Your original config is backed up at ~/.ssh/config.bak.2026009.