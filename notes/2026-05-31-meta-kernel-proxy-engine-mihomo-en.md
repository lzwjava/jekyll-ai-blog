---
audio: false
generated: true
image: false
lang: en
layout: post
title: Meta Kernel Proxy Engine Mihomo
translated: false
type: note
---

What is mihomo?
    
    mihomo (Meta Kernel) is a fork of Clash — a rule-based network proxy/tunnel written in Go. It's the engine behind many proxy clients (Clash Verge, ClashX Meta, Stash, etc.). You're looking at the source code at ~/projects/mihomo/.
    
    What it does: Acts as a local proxy server that intercepts your network traffic, applies routing rules, and forwards connections through various proxy protocols (Shadowsocks, VMess, VLESS, Trojan, Hysteria2, TUIC, WireGuard, etc.) or directly.
    
    
    
    Project Architecture
    
    
    main.go              — CLI entry point: flag parsing, config loading, signal handling
    config/              — YAML config parser (RawConfig -> Config struct)
    hub/                 — RESTful API server (controllers for proxies, rules, DNS, connections)
    hub/executor/        — Applies parsed config: starts listeners, loads proxies, applies rules
    adapter/
      inbound/           — Inbound connection adapters (HTTP, SOCKS, etc.)
      outbound/          — Outbound proxy adapters (ss, vmess, vless, hysteria2, etc.)
      outboundgroup/     — Proxy groups (select, url-test, fallback, load-balance, relay)
      provider/          — Proxy providers (HTTP/file subscription sources)
    listener/            — TCP/UDP listeners (mixed-port, tun, redir, tproxy)
    tunnel/              — Core packet routing engine — matches rules, picks proxy, dials
    dns/                 — Full DNS server (DoH, DoT, DoQ, fake-ip, redir-host)
    rules/               — Rule implementations (DOMAIN, IP-CIDR, GEOIP, RULE-SET, MATCH)
    transport/           — Protocol transports (vmess websocket, vless vision, xhttp, etc.)
    component/           — Shared components (geoip, geodata, fakeip pool, process finder)
    
    
    Data flow:
    1. main.go reads config.yaml, calls hub.Parse() which calls config.Parse()
    2. config/config.go unmarshals YAML into RawConfig, then builds Config (creates proxy objects, rule objects, DNS resolvers)
    3. hub/executor applies the config: starts listeners, creates proxy groups, loads rule providers
    4. When a connection comes in, tunnel/tunnel.go matches it against rules, picks a proxy/outbound, and dials
    
    
    
    Your Config (~/.config/mihomo/config.yaml) — How It Works
    
    Inbound Ports:
    - port 7890 — HTTP proxy
    - socks-port 7891 — SOCKS5 proxy
    - mixed-port 7892 — combined HTTP+SOCKS5 (use this one, the others are redundant)
    
    Proxies (2 nodes):
    - My SS 1 — Shadowsocks (chacha20-ietf-poly1305) at 5.223.42.176:19400
    - My Hysteria2 2 — Hysteria2 at h2.lzwjava.shop:443 (UDP-based, fast)
    
    Proxy Group:
    - Proxy — manual select group with both nodes
    
    DNS (fake-ip mode):
    - Listens on 0.0.0.0:53
    - Uses Chinese DoH (doh.pub, alidns) for nameserver
    - Fake-IP pool: 198.18.0.1/16 — returns fake IPs to apps, then intercepts the real connection
    - Filters out local/LAN domains from fake-ip
    
    Rules (how traffic is routed):
    1. Specific domains (linkedin, deepseek, claude, openai, etc.) → Proxy
    2. RULE-SET,Global → Proxy (large list of blocked/proxy sites)
    3. RULE-SET,China → DIRECT (Chinese sites go direct)
    4. RULE-SET,ChinaIP → DIRECT
    5. Private IPs (10.x, 172.16.x, 192.168.x) → DIRECT
    6. GEOIP,CN → DIRECT (any Chinese IP goes direct)
    7. MATCH,Proxy — everything else → Proxy
    
    
    
    Issues & Recommendations
    
    Problems in your config:
    
    1. Three ports defined — only one needed. port, socks-port, and mixed-port all serve overlapping purposes. Use only mixed-port: 7892 and delete the other two. mixed-port handles both HTTP and SOCKS5.
    
    2. No secret on external-controller. API is wide open on 0.0.0.0:9090 — anyone on your LAN can switch your proxy nodes, read connections, etc. Add secret: "something-random".
    
    3. experimental.ignore-resolve-fail: true — this is deprecated/ignored in Meta mihomo. It won't cause harm but does nothing.
    
    4. *cfw- keys** are Clash for Windows specific — meaningless in mihomo. Dead config.
    
    5. No ip-version on proxies — your Hysteria2 uses UDP; explicitly setting ip-version: dual or ipv4-prefer can avoid IPv6 resolution delays.
    
    6. DNS listen: 0.0.0.0:53 — binding to port 53 requires root on macOS. Either run mihomo as root, use a higher port (e.g., 1053), or use TUN mode which hijacks DNS automatically.
    
    7. No fallback DNS / no nameserver-policy — your DNS setup works but could be smarter. Chinese domains should use Chinese DNS, foreign domains should use foreign DNS (through proxy). Consider adding:
       yaml
       nameserver-policy:
         "geosite:cn,private": [223.5.5.5, 119.29.29.29]
         "geosite:geolocation-!cn": [8.8.8.8, 1.1.1.1]
       
    
    8. No tcp-concurrent: true — enabling this lets mihomo race IPv4/IPv6 connections simultaneously for faster dial.
    
    9. Rule ordering could be tighter — GEOIP,CN after RULE-SET,ChinaIP is redundant since ChinaIP already catches CN IPs. Not harmful, just extra work.